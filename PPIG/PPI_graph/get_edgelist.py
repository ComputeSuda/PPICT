# 获取86个蛋白质的PPI网络结构图
# 将86个蛋白质按顺序编号成0-85，再找出所有链接的边

import xlrd

Cross_talk_file_path = '../Datasets/Cross-talk.xlsx'
String_ppis_file_path = '../Datasets/String_ppi_86.xlsx'
Proteins_file_path = '../Datasets/Proteins/inter_cross_talk_proteins(dul).txt'

Cross_talk_workbook = xlrd.open_workbook(Cross_talk_file_path)
String_ppis_workbook = xlrd.open_workbook(String_ppis_file_path)

Inter_Cross_talk_proteins_sheet = Cross_talk_workbook.sheet_by_name('Inter Cross-talk Proteins')
String_ppis_86_short_sheet = String_ppis_workbook.sheet_by_name('String_ppi_86_short')

Protein_ID_Names = dict()  # 用来存蛋白质ID对用的Gene name
Protein_ID_num = dict()  # 用来存蛋白质ID对应的编号
Protein_Name_num = dict()  # 用来存储Gene name对应的编号
Edgelists = []  # 用来存储PPIs的边(num1(p1), num2(p2))

with open(Proteins_file_path, 'r', encoding='utf-8') as f1:
    lines = [item.strip('\n') for item in f1.readlines()]
    i = 0
    for line in lines[1:]:
        Protein_ID_num[line] = i  # 'P06400': '0'
        i += 1

print(Protein_ID_num)

Inter_Cross_talk_proteins_sheet_rows = Inter_Cross_talk_proteins_sheet.nrows
Inter_Cross_talk_proteins_sheet_cols = Inter_Cross_talk_proteins_sheet.ncols
String_ppis_86_short_rows = String_ppis_86_short_sheet.nrows
String_ppis_86_short_cols = String_ppis_86_short_sheet.ncols

for row in range(1, Inter_Cross_talk_proteins_sheet_rows):
    Gene_name = Inter_Cross_talk_proteins_sheet.row_values(row)[1]
    UniprotId = Inter_Cross_talk_proteins_sheet.row_values(row)[2]
    if UniprotId not in Protein_ID_Names.keys():
        Protein_ID_Names[Gene_name] = UniprotId

print(Protein_ID_Names)

for Gene, ID in Protein_ID_Names.items():
    # print(Gene, ID)
    gene_items = Gene.split(';')  # 因为Gene name可能会出现多个
    for gene_item in gene_items:
        Protein_Name_num[gene_item] = Protein_ID_num[ID]

print(Protein_Name_num)


for row in range(1, String_ppis_86_short_rows):
    node1 = String_ppis_86_short_sheet.row_values(row)[0]
    node2 = String_ppis_86_short_sheet.row_values(row)[1]
    Edgelists.append(tuple([Protein_Name_num[node1], Protein_Name_num[node2]]))

print(Edgelists)
Edgelists.sort(key=lambda x: (x[0], x[1]))
print(len(Edgelists))

with open('./PPIs_Edgelists_86.txt', 'a') as f2:
    for Edgelist in Edgelists:
        items = [str(item) for item in Edgelist]
        f2.write(' '.join(items) + '\n')
