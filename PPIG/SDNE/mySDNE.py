import sys
path_result = "./Latent_Representation/"
from Model_SDNE import *
from Metrics import *
from Data_Process import *
from sklearn.cluster import KMeans
import numpy as np
import torch
import time

import warnings
warnings.filterwarnings('ignore')

Dataset = 'PPIs'
Classification = True
Clustering = False

if (Dataset is "PPIs"):
    load_data = Load_Data(Dataset)
    # Features, Labels, Adjacency_Matrix = load_data.Graph()
    Features, Adjacency_Matrix = load_data.graph_no_label()
    Features = torch.Tensor(Features)
    Adjacency_Matrix = torch.Tensor(Adjacency_Matrix)
else:
    load_data = Load_Data(Dataset)
    Features, Labels = load_data.CPU()
    Features = torch.Tensor(Features)

if('Adjacency_Matrix' in vars()):
    print('Adjacency matrix is raw')
    pass
else:
    print('Adjacency matrix is caculated by KNN')
    graph = Graph_Construction(Features)
    Adjacency_Matrix = graph.KNN()

convolution_kernel = Convolution_Kernel(Adjacency_Matrix)
Laplacian_Convolution = convolution_kernel.Laplacian_Convolution()

Epoch_Num = 3000
Learning_Rate = 1e-3
Lambda = 1

Input_Dim = Adjacency_Matrix.shape[0]
Hidden_Layer_1 = 1024
Hidden_Layer_2 = 578

B = Adjacency_Matrix * (20 - 1) + 1

ACC_SDNE_total = []
NMI_SDNE_total = []
PUR_SDNE_total = []

ACC_SDNE_total_STD = []
NMI_SDNE_total_STD = []
PUR_SDNE_total_STD = []

F1_score = []

mse_loss = torch.nn.MSELoss(size_average=False)
model_SDNE = mySDNE(Input_Dim, Hidden_Layer_1, Hidden_Layer_2)
optimzer = torch.optim.Adam(model_SDNE.parameters(), lr=Learning_Rate)

for epoch in range(Epoch_Num):
    Latent_Representation, Graph_Reconstrction = model_SDNE(Adjacency_Matrix)
    loss_1st = torch.norm((Graph_Reconstrction - Adjacency_Matrix)*B, p='fro')
    loss_2st = torch.trace((Latent_Representation.T).mm(Laplacian_Convolution).mm(Latent_Representation))
    loss = loss_1st + Lambda * loss_2st

    optimzer.zero_grad()
    loss.backward()
    optimzer.step()

    Latent_Representation = Latent_Representation.cpu().detach().numpy()

    if Classification and (epoch + 1) % 50 == 0:
        print("Epoch:{},Loss:{:.4f}".format(epoch + 1, loss.item()))
        # score = myRF(Latent_Representation, Labels, scale=0.3)
        # print("Epoch[{}/{}], score = {}".format(epoch + 1, Epoch_Num, score))
        # F1_score.append(score)
    if epoch == Epoch_Num-1:
        np.save(path_result + "{}_{}.npy".format('PPIs', Epoch_Num), Latent_Representation)
