import xlrd
import xlwt
import itertools

UniprotId_all_file_path = '../Datasets/Proteins/inter_cross_talk_proteins(dul).txt'
with open(UniprotId_all_file_path, 'r', encoding='utf-8') as f1:
    uniprotIds = [item.strip('\n') for item in f1.readlines()[1:]]

print(len(uniprotIds))


PTM_Name = {'p': 'Phosphorylation', 'ac': 'Acetylation', 'm': 'Methylation', 'ga': 'O-GalNAc',
            'ub': 'Ubiquitination', 'sm': 'Sumoylation', 'gl': 'O-GlcNAc', 'pa': 'Palmitoylation',
            'ng': 'N-linkedGlycosylation', 'sc': 'Succinylation'}

# supply_dataset_file_path = '../Ptm-site/Supply.xlsx'
#
# supply_dataset_workbook = xlrd.open_workbook(supply_dataset_file_path)
# supply_dataset_workbook_sheet = supply_dataset_workbook.sheet_by_name('Sheet1')
# ptm_sites_list = supply_dataset_workbook_sheet.col_values(2)
# print(len(ptm_sites_list))
# ptm_sites_type_list = []
#
# for ptm_site in ptm_sites_list:
#     name = ptm_site.split('-')[1]
#     if name[0] == 'm':
#         name = 'm'
#     ptm_sites_type_list.append((ptm_site, PTM_Name[name]))
#
# work_book = xlwt.Workbook(encoding='utf-8')
# sheet = work_book.add_sheet('Sheet1')
# len_dic = len(ptm_sites_type_list)
# c = 0
# for items in ptm_sites_type_list:
#     sheet.write(c, 0, items[0])
#     sheet.write(c, 1, items[1])
#     c += 1
#
# work_book.save('./ptm_site_name.xlsx')


Inter_Cross_talk_path = '../Datasets/Cross-talk.xlsx'

Inter_Cross_talk_workbook = xlrd.open_workbook(Inter_Cross_talk_path)
# print(Ptm_site_workbook.sheet_names())
Inter_Cross_talk_Proteins_Pairs_workbook_sheet = Inter_Cross_talk_workbook.sheet_by_name('Inter Cross-talk Proteins Pairs')
Inter_Cross_talk_Proteins_Pairs_workbook_sheet_cols = Inter_Cross_talk_Proteins_Pairs_workbook_sheet.ncols
Inter_Cross_talk_Proteins_Pairs_workbook_sheet_rows = Inter_Cross_talk_Proteins_Pairs_workbook_sheet.nrows

Inter_Cross_talk_Proteins_Pairs = []

for row in range(1, Inter_Cross_talk_Proteins_Pairs_workbook_sheet_rows):
    uniprotId1 = Inter_Cross_talk_Proteins_Pairs_workbook_sheet.row_values(row)[2]
    uniprotId2 = Inter_Cross_talk_Proteins_Pairs_workbook_sheet.row_values(row)[5]
    if (uniprotId1, uniprotId2) not in Inter_Cross_talk_Proteins_Pairs:
        Inter_Cross_talk_Proteins_Pairs.append((uniprotId1, uniprotId2))

print(len(set(Inter_Cross_talk_Proteins_Pairs)))

# with open('../Datasets/Proteins/inter_cross_talk_proteins_pairs.txt', 'a') as f2:
#     for item in Inter_Cross_talk_Proteins_Pairs:
#         f2.write(item[0]+'\t'+item[1]+'\n')


Ptm_site_all_file_path = './Ptm_site_all.xlsx'
Ptm_site_Ltp_file_path = './PTM_LTP.xlsx'


# All low-flux PTM sites for 86 proteins, excluding high-flux
# Ptm_site_workbook = xlrd.open_workbook(Ptm_site_Ltp_file_path)
# # print(Ptm_site_workbook.sheet_names())
# ptm_site_workbook_sheet = Ptm_site_workbook.sheet_by_name('Sheet1')
#
# ptm_site_cols = ptm_site_workbook_sheet.ncols
# ptm_site_rows = ptm_site_workbook_sheet.nrows
#
# uniprotId_sites_ltp_dic = dict()
#
# # for uniprotId in uniprotIds:
# #     uniprotId_sites_ltp_dic[uniprotId] = set()
#
# for row in range(1, ptm_site_rows):
#     protein_name = ptm_site_workbook_sheet.row_values(row)[0]
#     uniprotId = ptm_site_workbook_sheet.row_values(row)[1]
#     # print(uniprotId)
#     site = ptm_site_workbook_sheet.row_values(row)[2]
#     ptm_type = ptm_site_workbook_sheet.row_values(row)[3]
#     if uniprotId in uniprotIds:
#         if (protein_name, uniprotId) not in uniprotId_sites_ltp_dic.keys():
#             uniprotId_sites_ltp_dic[(protein_name, uniprotId)] = set()
#         uniprotId_sites_ltp_dic[(protein_name, uniprotId)].add((site.split('-')[0], ptm_type))
#
# print(len(uniprotId_sites_all_dic.keys()))
# uniprotId_site_all = [item[1] for item in uniprotId_sites_ltp_dic.keys()]
# for uniprotId in uniprotIds:
#     if uniprotId not in uniprotId_site_all:
#         print(uniprotId)
# with open('./uniprotId_sites_Ltp.txt', 'w') as f2:
#     for key, values in uniprotId_sites_ltp_dic.items():
#         f2.write(str(key)+':\t')
#         for value in values:
#             f2.write(str(value)+'\t')
#         else:
#             f2.write('\n')

uniprot_ptm_sites_cross_list = []


def get_protein_name_ptms(uniprotId, dict_all):
    for key, values in dict_all.items():
        if uniprotId in key:
            return key, values
#
#
# for uniprotId1, uniprotId2 in Inter_Cross_talk_Proteins_Pairs:
#     uniprotId1_name, uniprotId1_ptms = get_protein_name_ptms(uniprotId1, uniprotId_sites_all_dic)
#     uniprotId2_name, uniprotId2_ptms = get_protein_name_ptms(uniprotId2, uniprotId_sites_all_dic)
#     # print(values)
#     print(uniprotId1, uniprotId2)
#     # print(list(itertools.product([1, 2, 3], [5, 6, 7])))
#     for item in list(itertools.product(uniprotId1_ptms, uniprotId2_ptms)):
#         with open('./neagtive_Ltp.txt', 'a') as f3:
#             f3.write(uniprotId1_name[0]+'\t'+uniprotId1_name[1]+'\t'+item[0][0]+'\t'+item[0][1]+'\t'
#                      +uniprotId2_name[0]+'\t'+uniprotId2_name[1]+'\t'+item[1][0]+'\t'+item[1][1]+'\n')

# All PTM sites of 86 proteins, including low and high fluxes, are counted below
# Ptm_site_workbook = xlrd.open_workbook(Ptm_site_all_file_path)
# # print(Ptm_site_workbook.sheet_names())
# ptm_site_workbook_sheet = Ptm_site_workbook.sheet_by_name('HumanPtm')
#
# ptm_site_cols = ptm_site_workbook_sheet.ncols
# ptm_site_rows = ptm_site_workbook_sheet.nrows
#
# uniprotId_sites_all_dic = dict()
#
# # for uniprotId in uniprotIds:
# #     uniprotId_sites_all_dic[uniprotId] = set()
#
# for row in range(1, ptm_site_rows):
#     protein_name = ptm_site_workbook_sheet.row_values(row)[1]
#     uniprotId = ptm_site_workbook_sheet.row_values(row)[2]
#     # print(uniprotId)
#     site = ptm_site_workbook_sheet.row_values(row)[3]
#     ptm_type = ptm_site_workbook_sheet.row_values(row)[4]
#     if uniprotId in uniprotIds:
#         if (protein_name, uniprotId) not in uniprotId_sites_all_dic.keys():
#             uniprotId_sites_all_dic[(protein_name, uniprotId)] = set()
#         uniprotId_sites_all_dic[(protein_name, uniprotId)].add((site.split('-')[0], ptm_type))
#
# print(len(uniprotId_sites_all_dic.keys()))
# uniprotId_site_all = [item[1] for item in uniprotId_sites_all_dic.keys()]
# for uniprotId in uniprotIds:
#     if uniprotId not in uniprotId_site_all:
#         print(uniprotId)
# # with open('./uniprotId_sites_all.txt', 'w') as f2:
# #     for key, values in uniprotId_sites_all_dic.items():
# #         f2.write(str(key)+':\t')
# #         for value in values:
# #             f2.write(str(value)+'\t')
# #         else:
# #             f2.write('\n')
#
#
# for uniprotId1, uniprotId2 in Inter_Cross_talk_Proteins_Pairs:
#     uniprotId1_name, uniprotId1_ptms = get_protein_name_ptms(uniprotId1, uniprotId_sites_all_dic)
#     uniprotId2_name, uniprotId2_ptms = get_protein_name_ptms(uniprotId2, uniprotId_sites_all_dic)
#     # print(values)
#     print(uniprotId1, uniprotId2)
#     # print(list(itertools.product([1, 2, 3], [5, 6, 7])))
#     for item in list(itertools.product(uniprotId1_ptms, uniprotId2_ptms)):
#         with open('./neagtive_all.txt', 'a') as f3:
#             f3.write(uniprotId1_name[0]+'\t'+uniprotId1_name[1]+'\t'+item[0][0]+'\t'+item[0][1]+'\t'
#                      +uniprotId2_name[0]+'\t'+uniprotId2_name[1]+'\t'+item[1][0]+'\t'+item[1][1]+'\n')
#


