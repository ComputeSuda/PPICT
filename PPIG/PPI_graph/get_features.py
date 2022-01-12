# Features of each protein calculated by FEGS are 578 dimensions 86 * 578

import scipy.io as scio
import os

Proteins_file_path = '../Datasets/Proteins/inter_cross_talk_proteins(dul).txt'
Proteins_fasta_path = '../Datasets/fasta/uniprot_fastas'

Protein_ID_num = dict()  # The protein number stored to represent edge nodes

with open(Proteins_file_path, 'r', encoding='utf-8') as f1:
    lines = [item.strip('\n') for item in f1.readlines()]
    i = 0
    for line in lines[1:]:
        Protein_ID_num[line] = i  # 'P06400': '0'
        i += 1

print(Protein_ID_num)

Proteins_nums = [(item.split('.')[0], Protein_ID_num[item.split('.')[0]]) for item in os.listdir(Proteins_fasta_path)]
print(Proteins_nums)
Proteins_nums_dict = dict()
for Protein, num in Proteins_nums:
    Proteins_nums_dict[Protein] = num
print(Proteins_nums_dict)
Features = []  # To store sequential node features (numbered by side nodes)

dataFile = './PPIs.mat'  # Sequence characteristics calculated by FEGS (578 dimensions)
datas = scio.loadmat(dataFile)['ans']

Edges_node_proteins_sorts = list(Protein_ID_num.keys())  # Protein sequence sorted by node number
print(Edges_node_proteins_sorts)

# with open('./Protein_num.txt', 'a') as f2:
#     for i, p in enumerate(Edges_node_proteins_sorts):
#         f2.write(str(p)+' '+str(i)+'\n')

for Edges_node_proteins_sort in Edges_node_proteins_sorts:
    num = Proteins_nums_dict[Edges_node_proteins_sort]
    Features.append(datas[num])

print(len(Features))
# with open('./PPIs_features.txt', 'a') as f1:
#     for num, feature in enumerate(Features):
#         f1.write(str(num)+' '+' '.join([str(item) for item in feature])+'\n')



