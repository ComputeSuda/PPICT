# The cross-talk quantitative composition of protein pairs and the corresponding number of corresponding number of the Protein_num.txt file
# Generating adjacency matrices and adjacency tables
import xlrd

Cross_talk_file_path = '../Datasets/Cross-talk.xlsx'

Protein_num_file_path = './Protein_num.txt'

Protein_num = dict()
with open(Protein_num_file_path, 'r') as f1:
    lines = f1.readlines()
    for line in lines:
        Protein, num = line.strip('\n').split(' ')
        Protein_num[Protein] = num

print(Protein_num)

Cross_talk_workbook = xlrd.open_workbook(Cross_talk_file_path)
Cross_talk_pairs_sheet = Cross_talk_workbook.sheet_by_name('Inter Negative Proteins Pairs')

Cross_talk_pairs_rows = Cross_talk_pairs_sheet.nrows
Cross_talk_pairs_cols = Cross_talk_pairs_sheet.ncols

Cross_talk_pairs = []
Cross_talk_pairs_weights = []  # Adjacent table with weight
for Cross_talk_pairs_row in range(1, Cross_talk_pairs_rows):
    Pro1 = Cross_talk_pairs_sheet.row_values(Cross_talk_pairs_row)[2]
    Pro2 = Cross_talk_pairs_sheet.row_values(Cross_talk_pairs_row)[5]
    Pairs_num = Cross_talk_pairs_sheet.row_values(Cross_talk_pairs_row)[6]
    Cross_talk_pairs.append((Pro1, Pro2))
    Cross_talk_pairs_weights.append((Pro1, Pro2, Pairs_num))

with open('Negative_Nums_Edgelists.txt', 'w') as f2:
    for Cross_talk_pair in Cross_talk_pairs:
        p1_num = str(Protein_num[Cross_talk_pair[0]])
        p2_num = str(Protein_num[Cross_talk_pair[1]])
        f2.write(p1_num+' '+p2_num+'\n')

with open('Negative_Nums_Edgelists_weight.txt', 'w') as f3:
    for Cross_talk_pairs_weight in Cross_talk_pairs_weights:
        p1_num = str(Protein_num[Cross_talk_pairs_weight[0]])
        p2_num = str(Protein_num[Cross_talk_pairs_weight[1]])
        weight = str(int(Cross_talk_pairs_weight[2]))
        f3.write(p1_num + ' ' + p2_num + ' ' + weight + '\n')

import numpy as np

Matrix_Nums = np.zeros((86, 86), dtype='int32').tolist()
# print(Matrix_Nums[1][2])
for Cross_talk_pair in Cross_talk_pairs:
    p1_num = int(Protein_num[Cross_talk_pair[0]])
    p2_num = int(Protein_num[Cross_talk_pair[1]])
    Matrix_Nums[p1_num][p2_num] = 1

with open('./Negative_Matrix.txt', 'w') as f4:
    for i in range(len(Matrix_Nums)):
        f4.write(' '.join([str(item) for item in Matrix_Nums[i]]))
        f4.write('\n')
