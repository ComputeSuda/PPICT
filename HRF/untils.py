# Sample the dataset to generate 50 training sets and 10 test sets, each containing 100 positive samples and 100 negative samples, and the test set containing 99 positive samples and 99 negative samples
# Loading pre-processed weight features and protein features extracted by Linear_VAE
import random

import xlrd
import numpy as np


# from model.MLP_Pre import MLP_pre_net


def generate_samples(Cross_talk_features_path, Negative_features_path, Train_Sample_nums, Test_Sample_nums):  # sampling
    Cross_talk_features_workbook = xlrd.open_workbook(Cross_talk_features_path)
    Negative_features_workbook = xlrd.open_workbook(Negative_features_path)

    Cross_talk_features_sheet = Cross_talk_features_workbook.sheet_by_name('Sheet1')
    Negative_features_sheet = Negative_features_workbook.sheet_by_name('Sheet1')
    Po_nums = Cross_talk_features_sheet.nrows
    Ne_nums = Negative_features_sheet.nrows
    Po_nums = [i for i in range(1, Po_nums)]
    Ne_nums = [i for i in range(1, Ne_nums)]
    random.shuffle(Ne_nums)
    random.shuffle(Po_nums)
    print(Po_nums)
    print(len(Ne_nums))

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

    def merge_features(Sample_nums, Nums, flag):  # po:50, 100, True; Ne:10, 100, False

        for Sample_num in range(Sample_nums):
            Samples = []
            if flag:  # Half the training set test set in advance and then sample from it
                Po_samples_numbers = random.sample(Po_nums[:100], Nums)
                Ne_samples_numbers = random.sample(Ne_nums[:(len(Ne_nums) // 2)], Nums)
            else:
                Po_samples_numbers = random.sample(Po_nums[100:], Nums)
                Ne_samples_numbers = random.sample(Ne_nums[(len(Ne_nums) // 2):], Nums)

            print(Ne_samples_numbers)
            for Po_num in Po_samples_numbers:
                Po_P1 = Cross_talk_features_sheet.row_values(Po_num)[1]
                Po_P2 = Cross_talk_features_sheet.row_values(Po_num)[7]
                Po_Gcn_features = np.concatenate((Cross_talk_gcn_features[Protein_number[Po_P1]],
                                                  Cross_talk_gcn_features[Protein_number[Po_P2]]))
                # print(Po_Gcn_features.shape)
                Po_PPI_features = [Cross_talk_features_sheet.row_values(Po_num)[12]]
                if 'None' in Cross_talk_features_sheet.row_values(Po_num)[13:41]:
                    Po_str_features = [0.] * 28
                else:
                    Po_str_features = Cross_talk_features_sheet.row_values(Po_num)[13:41]
                Po_seq_features = Cross_talk_features_sheet.row_values(Po_num)[41:]
                Po_W_features = Po_PPI_features + Po_str_features + Po_seq_features
                Po_W_features = np.array(Po_W_features, dtype='float32').reshape(-1, 1)
                Po_Gcn_features = Po_Gcn_features.reshape(1, -1)
                # if + not × : PPICT*
                # Po_Features = np.concatenate((Po_W_features.reshape(-1), Po_Gcn_features.reshape(-1)), axis=0)
                # print(Po_Features.shape)
                Po_Features = Po_W_features.dot(Po_Gcn_features).reshape(-1)
                # print(Po_Features.shape)
                # Po_W_features = np.array(Po_W_features, dtype='float32').tolist()
                # Samples.append([1] + Po_W_features)
                Samples.append([1] + Po_Features.tolist())
            for Ne_num in Ne_samples_numbers:
                Ne_P1 = Negative_features_sheet.row_values(Ne_num)[1]
                Ne_P2 = Negative_features_sheet.row_values(Ne_num)[7]
                Ne_Gcn_features = np.concatenate(
                    (Negative_gcn_features[Protein_number[Ne_P1]], Negative_gcn_features[Protein_number[Ne_P2]]))
                # print(Ne_Gcn_features.shape)
                Ne_PPI_features = [Negative_features_sheet.row_values(Ne_num)[12]]
                if 'None' in Negative_features_sheet.row_values(Ne_num)[13:41]:
                    Ne_str_features = [0.] * 28
                else:
                    Ne_str_features = Negative_features_sheet.row_values(Ne_num)[13:41]
                Ne_seq_features = Negative_features_sheet.row_values(Ne_num)[41:]
                Ne_W_features = Ne_PPI_features + Ne_str_features + Ne_seq_features
                Ne_W_features = np.array(Ne_W_features, dtype='float32').reshape(-1, 1)
                Ne_Gcn_features = Ne_Gcn_features.reshape(1, -1)
                # if + not × : PPICT*
                # Ne_Features = np.concatenate((Ne_W_features.reshape(-1), Ne_Gcn_features.reshape(-1)), axis=0)
                Ne_Features = Ne_W_features.dot(Ne_Gcn_features).reshape(-1)
                # print(Ne_Features.shape)
                Samples.append([0] + Ne_Features.tolist())
                # Ne_W_features = np.array(Ne_W_features, dtype='float32').tolist()
                # Samples.append([0] + Ne_W_features)
            # with open('../Datasets/Samples/Cancer_Train/sample' + str(Train_Sample_num) + '.txt', 'w') as f1:
            #     for Train_Sample in Train_Samples:
            #         f1.writelines(' '.join(Train_Sample) + '\n')
            Samples_np = np.array(Samples)
            # print(Samples_np.shape)
            # Samples_np = MLP_pre_net(Samples_np)
            # print(Samples_np.shape)
            if flag:
                np.save('./Samples/PPICT_Train/sample' + str(Sample_num) + '.npy', Samples_np)
            else:
                np.save('./Samples/PPICT_Test/sample' + str(Sample_num) + '.npy', Samples_np)

    merge_features(Train_Sample_nums, 50, True)
    merge_features(Test_Sample_nums, 10, False)


def load_gcn_features(Cross_talk_Features_path, Negative_Features_path):  # extract protein features
    Cross_talk_Features = np.load(Cross_talk_Features_path)
    Negative_Features = np.load(Negative_Features_path)
    return Cross_talk_Features, Negative_Features


# Cross_talk_features_path = '../Dataset/W_features/Positive_features.xls'
# Negative_features_path = '../Dataset/W_features/Negative_features.xls'
# generate_samples(Cross_talk_features_path, Negative_features_path, 50, 10)

