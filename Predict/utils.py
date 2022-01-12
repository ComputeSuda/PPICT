import random

import xlrd
import numpy as np


# from model.MLP_Pre import MLP_pre_net


def get_features(Cross_talk_features_path):
    Cross_talk_features_workbook = xlrd.open_workbook(Cross_talk_features_path)

    Cross_talk_features_sheet = Cross_talk_features_workbook.sheet_by_name('Sheet1')
    nums = Cross_talk_features_sheet.nrows
    nums = [i for i in range(1, nums)]

    Cross_talk_gcn_features_file_path = '../Dataset/Protein_pair_features/Cross_talk_gcn_features128.npy'
    Negative_gcn_features_file_path = '../Dataset/Protein_pair_features/Cross_talk_gcn_features128.npy'
    Cross_talk_gcn_features, Negative_gcn_features = load_gcn_features(Cross_talk_gcn_features_file_path,
                                                                       Negative_gcn_features_file_path)

    # print(Cross_talk_gcn_features[1])
    Protein_number = dict()

    with open('../PPIG/PPI_graph/Protein_num.txt', 'r') as f1:
        lines = f1.readlines()
        for line in lines:
            Protein_number[line.strip('\n').split(' ')[0]] = int(line.strip('\n').split(' ')[1])

    def merge_features(nums, Cross_talk_gcn_features, Negative_gcn_features):

        Samples = []

        for num in nums:
            Po_P1 = Cross_talk_features_sheet.row_values(num)[1]
            Po_P2 = Cross_talk_features_sheet.row_values(num)[7]
            if num <= 5:
                Po_Gcn_features = np.concatenate((Cross_talk_gcn_features[Protein_number[Po_P1]],
                                              Cross_talk_gcn_features[Protein_number[Po_P2]]))
            else:
                Po_Gcn_features = np.concatenate((Negative_gcn_features[Protein_number[Po_P1]],
                                              Negative_gcn_features[Protein_number[Po_P2]]))
            # print(Po_Gcn_features.shape)
            Po_PPI_features = [Cross_talk_features_sheet.row_values(num)[12]]
            if 'None' in Cross_talk_features_sheet.row_values(num)[13:41]:
                Po_str_features = [0.] * 28
            else:
                Po_str_features = Cross_talk_features_sheet.row_values(num)[13:41]
            Po_seq_features = Cross_talk_features_sheet.row_values(num)[41:]
            Po_W_features = Po_PPI_features + Po_str_features + Po_seq_features
            Po_W_features = np.array(Po_W_features, dtype='float32').reshape(-1, 1)
            Po_Gcn_features = Po_Gcn_features.reshape(1, -1)
            # Po_Features = np.concatenate((Po_W_features.reshape(-1), Po_Gcn_features.reshape(-1)), axis=0)
            # print(Po_Features.shape)
            Po_Features = Po_W_features.dot(Po_Gcn_features).reshape(-1)
            # print(Po_Features.shape)
            # Po_W_features = np.array(Po_W_features, dtype='float32').tolist()
            # Samples.append([1] + Po_W_features)
            if num <= 5:
                Samples.append([1] + Po_Features.tolist())
            else:
                Samples.append([0] + Po_Features.tolist())
        Samples_np = np.array(Samples)
        # print(Samples_np.shape)
        # Samples_np = MLP_pre_net(Samples_np)
        # print(Samples_np.shape)
        np.save('PPICT_features.npy', Samples_np)
        print(Samples_np.shape)

    merge_features(nums, Cross_talk_gcn_features, Negative_gcn_features)


def load_gcn_features(Cross_talk_Features_path, Negative_Features_path):
    Cross_talk_Features = np.load(Cross_talk_Features_path)
    Negative_Features = np.load(Negative_Features_path)
    return Cross_talk_Features, Negative_Features


Test_features_path = './test_features.xlsx'
get_features(Test_features_path)