from __future__ import division
from __future__ import print_function
from evaluation import get_roc_score, clustering_latent_space
from input_data import load_adj_feature
from kcore import compute_kcore, expand_embedding
from model import *
from optimizer import OptimizerAE, OptimizerVAE
from preprocessing import *
import numpy as np
import os
import scipy.sparse as sp
import tensorflow as tf
import time

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
# tf.compat.v1.logging.set_verbosity(tf.compat.v1.logging.ERROR)

flags = tf.app.flags
FLAGS = flags.FLAGS

# Select graph dataset
flags.DEFINE_string('dataset', 'Cross-talk', 'Name of the graph dataset')

# Select machine learning task to perform on graph
flags.DEFINE_string('task', 'link_prediction', 'Name of the learning task')

# Model
flags.DEFINE_string('model', 'linear_vae', 'Name of the model')


# Model parameters
flags.DEFINE_float('dropout', 0., 'Dropout rate (1 - keep probability).')
flags.DEFINE_integer('epochs', 1000, 'Number of epochs in training.')
flags.DEFINE_boolean('features', True, 'Include node features or not in encoder')
flags.DEFINE_float('learning_rate', 0.05, 'Initial learning rate (with Adam)')
flags.DEFINE_integer('hidden', 64, 'Number of units in GCN hidden layer(s).')
flags.DEFINE_integer('dimension', 128, 'Dimension of encoder output, i.e. \
                                       embedding dimension')

# Experimental setup parameters
flags.DEFINE_integer('nb_run', 1, 'Number of model run + test')
flags.DEFINE_float('prop_val', 5., 'Proportion of edges in validation set \
                                   (for Link Prediction task)')
flags.DEFINE_float('prop_test', 10., 'Proportion of edges in test set \
                                      (for Link Prediction task)')
flags.DEFINE_boolean('validation', False, 'Whether to report validation \
                                           results at each epoch (for \
                                           Link Prediction task)')
flags.DEFINE_boolean('verbose', True, 'Whether to print comments details.')

flags.DEFINE_boolean('kcore', False, 'Whether to run k-core decomposition \
                                      and use the framework. False = model \
                                      will be trained on the entire graph')
flags.DEFINE_integer('k', 2, 'Which k-core to use. Higher k => smaller graphs\
                              and faster (but maybe less accurate) training')
flags.DEFINE_integer('nb_iterations', 10, 'Number of fix point iterations in \
                                           algorithm 2 of IJCAI paper. See \
                                           kcore.py file for details')

# Lists to collect average results
if FLAGS.task == 'link_prediction':
    mean_roc = []
    mean_ap = []
if FLAGS.kcore:
    mean_time_kcore = []
    mean_time_train = []
    mean_time_expand = []
    mean_core_size = []
mean_time = []

# Load graph dataset
if FLAGS.verbose:
    print("Loading data...")
if FLAGS.dataset == 'Cross-talk':
    adj_init, features_init = load_adj_feature('../Cross-talk/Fegs_1.npy',
                                               '../Cross-talk/Cross-talk_Matrix.txt')
else:
    adj_init, features_init = load_data(FLAGS.dataset)

print(type(adj_init), type(features_init))

# The entire training+test process is repeated FLAGS.nb_run times
for i in range(FLAGS.nb_run):

    if FLAGS.task == 'link_prediction':
        if FLAGS.verbose:
            print("Masking test edges...")
        # Edge Masking for Link Prediction: compute Train/Validation/Test set
        adj, val_edges, val_edges_false, test_edges, test_edges_false = \
            mask_test_edges(adj_init, FLAGS.prop_test, FLAGS.prop_val)
    elif FLAGS.task == 'node_clustering':
        adj_tri = sp.triu(adj_init)
        adj = adj_tri + adj_tri.T
    else:
        raise ValueError('Undefined task!')

    # Start computation of running times
    t_start = time.time()

    # Degeneracy Framework / K-Core Decomposition
    if FLAGS.kcore:
        if FLAGS.verbose:
            print("Starting k-core decomposition of the graph")
        # Save adjacency matrix of un-decomposed graph
        # (needed to embed nodes that are not in k-core, after GAE training)
        adj_orig = adj
        # Get the (smaller) adjacency matrix of the k-core subgraph,
        # and the corresponding nodes
        adj, nodes_kcore = compute_kcore(adj, FLAGS.k)
        # Get the (smaller) feature matrix of the nb_core graph
        if FLAGS.features:
            features = features_init[nodes_kcore, :]
        # Flag to compute k-core decomposition's running time
        t_core = time.time()
    elif FLAGS.features:
        features = features_init

    # Preprocessing and initialization
    if FLAGS.verbose:
        print("Preprocessing and Initializing...")
    # Compute number of nodes
    num_nodes = adj.shape[0]
    # If features are not used, replace feature matrix by identity matrix
    if not FLAGS.features:
        features = sp.identity(adj.shape[0])
    # Preprocessing on node features
    features = sparse_to_tuple(features)
    num_features = features[2][1]
    features_nonzero = features[1].shape[0]

    # Define placeholders
    placeholders = {
        'features': tf.sparse_placeholder(tf.float32),
        'adj': tf.sparse_placeholder(tf.float32),
        'adj_orig': tf.sparse_placeholder(tf.float32),
        'dropout': tf.placeholder_with_default(0., shape=())
    }

    # Create model
    model = None
    # Linear Graph Variational Autoencoder
    model = LinearModelVAE(placeholders, num_features, num_nodes,
                               features_nonzero)

    # Optimizer
    pos_weight = float(adj.shape[0] * adj.shape[0] - adj.sum()) / adj.sum()
    norm = adj.shape[0] * adj.shape[0] / float((adj.shape[0] * adj.shape[0]
                                                - adj.sum()) * 2)
    with tf.name_scope('optimizer'):
        # Optimizer for Non-Variational Autoencoders
        opt = OptimizerVAE(preds=model.reconstructions,
                           labels=tf.reshape(tf.sparse_tensor_to_dense(placeholders['adj_orig'],
                                                                       validate_indices=False), [-1]),
                           model=model,
                           num_nodes=num_nodes,
                           pos_weight=pos_weight,
                           norm=norm)

    # Normalization and preprocessing on adjacency matrix
    adj_norm = preprocess_graph(adj)
    adj_label = sparse_to_tuple(adj + sp.eye(adj.shape[0]))

    # Initialize TF session
    sess = tf.Session()
    sess.run(tf.global_variables_initializer())

    # Model training
    if FLAGS.verbose:
        print("Training...")

    for epoch in range(FLAGS.epochs):
        # Flag to compute running time for each epoch
        t = time.time()
        # Construct feed dictionary
        feed_dict = construct_feed_dict(adj_norm, adj_label, features,
                                        placeholders)
        feed_dict.update({placeholders['dropout']: FLAGS.dropout})
        # Weights update
        outs = sess.run([opt.opt_op, opt.cost, opt.accuracy],
                        feed_dict=feed_dict)
        # Compute average loss
        avg_cost = outs[1]
        if FLAGS.verbose:
            # Display epoch information
            print("Epoch:", '%04d' % (epoch + 1), "train_loss=", "{:.5f}".format(avg_cost),
                  "time=", "{:.5f}".format(time.time() - t))
            # Validation, for Link Prediction
            if not FLAGS.kcore and FLAGS.validation and FLAGS.task == 'link_prediction':
                feed_dict.update({placeholders['dropout']: 0})
                emb = sess.run(model.z_mean, feed_dict=feed_dict)
                feed_dict.update({placeholders['dropout']: FLAGS.dropout})
                val_roc, val_ap = get_roc_score(val_edges, val_edges_false, emb)
                print("val_roc=", "{:.5f}".format(val_roc), "val_ap=", "{:.5f}".format(val_ap))

    # Flag to compute Graph AE/VAE training time
    t_model = time.time()

    # Compute embedding

    # Get embedding from model
    emb = sess.run(model.z_mean, feed_dict=feed_dict)

    # If k-core is used, only part of the nodes from the original
    # graph are embedded. The remaining ones are projected in the
    # latent space via the expand_embedding heuristic
    if FLAGS.kcore:
        if FLAGS.verbose:
            print("Propagation to remaining nodes...")
        # Project remaining nodes in latent space
        emb = expand_embedding(adj_orig, emb, nodes_kcore, FLAGS.nb_iterations)
        # Compute mean running times for K-Core, GAE Train and Propagation steps
        mean_time_expand.append(time.time() - t_model)
        mean_time_train.append(t_model - t_core)
        mean_time_kcore.append(t_core - t_start)
        # Compute mean size of K-Core graph
        # Note: size is fixed if task is node clustering, but will vary if
        # task is link prediction due to edge masking
        mean_core_size.append(len(nodes_kcore))

    # Compute mean total running time
    mean_time.append(time.time() - t_start)

    print(type(emb))
    np.save('../Cross-talk/Cross_talk_gcn_features128_FEGS.npy', emb)

    # Test model
    if FLAGS.verbose:
        print("Testing model...")
    # Link Prediction: classification edges/non-edges
    # Get ROC and AP scores
    roc_score, ap_score = get_roc_score(test_edges, test_edges_false, emb)
    # Report scores
    mean_roc.append(roc_score)
    mean_ap.append(ap_score)

###### Report Final Results ######

# Report final results
print("\nTest results for", FLAGS.model,
      "model on", FLAGS.dataset, "on", FLAGS.task, "\n",
      "___________________________________________________\n")

if FLAGS.task == 'link_prediction':
    print("AUC scores\n", mean_roc)
    print("Mean AUC score: ", np.mean(mean_roc),
          "\nStd of AUC scores: ", np.std(mean_roc), "\n \n")

    print("AP scores\n", mean_ap)
    print("Mean AP score: ", np.mean(mean_ap),
          "\nStd of AP scores: ", np.std(mean_ap), "\n \n")

else:
    print("Adjusted MI scores\n", mean_mutual_info)
    print("Mean Adjusted MI score: ", np.mean(mean_mutual_info),
          "\nStd of Adjusted MI scores: ", np.std(mean_mutual_info), "\n \n")

print("Total Running times\n", mean_time)
print("Mean total running time: ", np.mean(mean_time),
      "\nStd of total running time: ", np.std(mean_time), "\n \n")
