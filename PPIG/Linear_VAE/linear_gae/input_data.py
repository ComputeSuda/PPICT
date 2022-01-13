import networkx as nx
import numpy as np
import pickle as pkl
import scipy.sparse as sp
import sys

'''
Disclaimer: the functions from this file come from tkipf/gae
original repository on Graph Autoencoders
'''


def parse_index_file(filename):
    index = []
    for line in open(filename):
        index.append(int(line.strip()))
    return index


def load_adj_feature(Features_file, Matrix_file):
    """ Load datasets from tkipf/gae input files
        :param dataset: 'Cross-talk' graph dataset.
        :return: n*n sparse adjacency matrix and n*f node features matrix
    """
    Features_np = np.load(Features_file)
    Features = sp.csr_matrix(Features_np)
    # print(Features_np.shape)
    matrix = np.zeros((Features_np.shape[0], Features_np.shape[0])).tolist()
    with open(Matrix_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        for i in range(len(lines)):
            items = lines[i].strip('\n').split(' ')
            for j in range(len(items)):
                matrix[i][j] = int(items[j])
    Matrix = np.array(matrix)
    Matrix = sp.lil_matrix(Matrix)
    # print(Matrix.shape)
    return Matrix, Features


# adj, features = load_adj_feature('../Cross-talk/SDNE_128.npy', '../Cross-talk/Cross-talk_Matrix.txt')
# print(adj)
#
# adj, features = load_data('cora')
# print(type(features), type(adj))