# -*- coding: utf-8 -*-
"""
Created on Thu Oct 31 19:40:29 2019

@author: DELL
"""

import sys, os

import prody
from prody import *
from pylab import *
from matplotlib.pylab import *
import math
import numpy as np
import pandas as pd
import xlrd

# ZERO = 1e-6
ioff()

# list_file = 'pdb_list.txt'
rcsb_pdb_path = '../PDB/RCSB'
alphafold_pdb_path = '../PDB/Alphafold'
rcsb_pdb_file_name_list = os.listdir(rcsb_pdb_path)
alphafold_pdb_file_name_list = os.listdir(alphafold_pdb_path)
pdb_file_name_list = rcsb_pdb_file_name_list+alphafold_pdb_file_name_list
print(len(pdb_file_name_list))
# sys.exit()
gnm_cc_out_path = r'.\gnm\cc'
anm_cc_out_path = r'.\anm\cc'
gnm_prs_out_path = r'.\gnm\prs'
anm_prs_out_path = r'.\anm\prs'
gnm_sq_out_path = r'.\gnm\sq'
anm_sq_out_path = r'.\anm\sq'
gnm_eigenvectors_out_path = r'.\gnm\eigenvector'
anm_stiffness_out_path = r'.\anm\stiffness'

slow_num = 20

print("""Usage:
./enm_batch [list_file] [pdb_path] [out_path]

This program read pdb file list from a text file as input. 
Outputs:
GNM defined eigenvectors and squared fluctuations for slow modes;
GNM defined PRS and Cross-Correlations;
ANM defined PRS;
Tittint and commute time.""")

rcsb_pdb_name_list = []
alphafold_pdb_name_list = []
for rcsb_pdb_name in rcsb_pdb_file_name_list:
    rcsb_pdb_name_list.append(rcsb_pdb_name[:4])
for alphafold_pdb_name in alphafold_pdb_name_list:
    alphafold_pdb_name_list.append(alphafold_pdb_name[:6])

print(len(rcsb_pdb_name_list), len(alphafold_pdb_name_list))
rcsb_pdb_chain = dict()
alphafold_pdb_chain = dict()

rcsb_df = open('../Datasets/PDB/sel_pdbchains.txt', 'r')
rcsb_data = rcsb_df.readlines()
alphafold_data = ['P51451_A', 'Q9UKX2_A', 'P42229_A', 'O75528_A', 'Q05513_A', 'Q9UKI8_A', 'P09769_A', 'O43561_A']  # Using UniprotId instead of pdb, the PDB structure file downloaded in Alphafold has only A chain.
print(len(rcsb_data), len(alphafold_data))
# print(type(data))
# print('1l1f' in pdb_name_list)
for rcsb_d in rcsb_data:
    # print(d[0], d[1])
    rcsb_pdb = rcsb_d.strip('\n').split('_')[0].lower()
    # print(type(pdb))
    rcsb_pdb_chain[rcsb_pdb] = rcsb_d.strip('\n').split('_')[1]

for alphafold_d in alphafold_data:
    alphafold_pdb = alphafold_d.split('_')[0]
    alphafold_pdb_chain[alphafold_pdb] = 'A'
print(len(rcsb_pdb_chain.keys()), len(alphafold_pdb_chain.keys()))
# print(pdb_chain['1a4y'])
# count = 0
# for key, value in pdb_chain.items():
#     count += len(value)
# print(len(pdb_chain)) # 934
# print(pdb_chain)
# print(count) # 964
# print(pdb_chain['1a31'])  # C


# try:
# 	f_list = open(list_file, 'r')
# except IOError:
# 	raise IOError('failed to open ' + list_file + '.')

# pdb_alls = {'3l3x', '3q05', '3wtp', '1io4', '1ubd', '3h1z', '6u04', '3swr', '4e3c', '2l43', '1ee4', '2w4o', '2k86', '1olg', '3pe4', '1sp2', '1jwh', '1h88', '6l9z', '1kbh', '4iqr', '5ydx', '3q95', '3kys', '1ikn', '6g0q', '1pjm', '3mhr', '1qz7', '1am9', '2qdj', '3sqd', '6muo', '3q06', '1sp1', '6uyr', '7bwn', '6k1k', '5u2b', '4djc', '3ifq', '3ts8', '3uvw', '6a6j', '5hhe', '4wxx', '4zn9', '4gu0', '1t2k', '1mk2', '1nfi', '2mux', '1u7f', '3e00', '4cri', '6uyo', '4mdj', '1xj7', '6s9w', '5i50', '1mv0', '3brt', '2ldu', '5hhw', '5kgf', '5vfw', '4ddp', '2p1l', '2aff', '3q26', '4yoc', '1qku', '5u4k', '2ro1', '1pzl', '4kik', '6hok', '1hcp', '1g5j', '1jsu', '3qkm', '4p4h', '2aze', '4gqb', '6qvw', '6m93', '4xlv', '1n4m', '1va1', '2uzk', '2lwd', '6t58', '2knc', '3btr', '5jjy', '1yvl', '1o9k', '1ul1', '1cws', '2z6h', '4ued', '2ka6', '5hou', '5f9f', '1bf5', '4elj', '6uyv', '6m91', '1xq8', '2o61', '4ell', '1ain', '6o9b', '6atf', '2kwo'}


def anm_gnm(pdb_file_name_list, pdb_chain, pdb_path):
    for file in pdb_file_name_list:
        pdb_name = file
        # pdb_name = '2y1n.pdb'
        pdb_file = pdb_path + os.sep + pdb_name
        try:
            pdb_name = pdb_name[:pdb_name.rindex('.')]
        except:
            pass
        print(pdb_name)  # 2y1n
        for chain in pdb_chain[pdb_name]:
            print(chain)
            structure = parsePDB(pdb_file)
            # calphas = structure.select('calpha')
            choose = 'not ion and name CA and chain ' + chain
            # print(choose)
            calphas = structure.select(choose)
            print(str(calphas.numAtoms()) + ' nodes are selected.')
            # break
            gnm = GNM(pdb_name)
            # print(type(gnm))
            gnm.buildKirchhoff(calphas, cutoff=10.0, gamma=1)

            resnum = gnm.numAtoms()

            # n_modes_n = 20
            n_modes_n = None  # Set None to calculate all models

            gnm.calcModes(n_modes=n_modes_n)
            n_modes = gnm._n_modes
            # print('n_modes', n_modes, type(n_modes))
            # print(int(int(n_modes) * 0.05))
            CC_gnm_top_3 = calcCrossCorr(gnm[0:3])
            if int(n_modes * 0.05) >= 1:
                CC_gnm_5_per = calcCrossCorr(gnm[0:int(n_modes * 0.05)])
            else:
                CC_gnm_5_per = calcCrossCorr(gnm[0:1])
            if int(n_modes * 0.2) >= 1:
                CC_gnm_5_per_20_per = calcCrossCorr(gnm[int(n_modes * 0.05):int(n_modes * 0.2)])
            else:
                CC_gnm_5_per_20_per = calcCrossCorr(gnm[0:1])
            if int(n_modes * 0.5) >= 1:
                CC_gnm_20_per_50_per = calcCrossCorr(gnm[int(n_modes * 0.2):int(n_modes * 0.5)])
            else:
                CC_gnm_20_per_50_per = calcCrossCorr(gnm[0:1])
            CC_gnm_greater_60_per = calcCrossCorr(gnm[int(n_modes * 0.6):])

            gnm_sq_all = calcSqFlucts(gnm)
            gnm_prs_all, gnm_effectiveness_all, gnm_sensitivity_all = calcPerturbResponse(gnm)

            gnm_eig_all = gnm.getEigvecs()  # (349, n_modes)
            gnm_eig_20 = gnm[:20].getEigvecs()
            gnm_eig_top3 = gnm[:3].getEigvecs()

            f_out_name = gnm_cc_out_path + os.sep + pdb_name + '_' + chain + '_gnm_cc_top3.npy'
            np.save(f_out_name, CC_gnm_top_3)

            f_out_name = gnm_cc_out_path + os.sep + pdb_name + '_' + chain + '_gnm_cc_5_per.npy'
            np.save(f_out_name, CC_gnm_5_per)

            f_out_name = gnm_cc_out_path + os.sep + pdb_name + '_' + chain + '_gnm_cc_5_per_20_per.npy'
            np.save(f_out_name, CC_gnm_5_per_20_per)

            f_out_name = gnm_cc_out_path + os.sep + pdb_name + '_' + chain + '_gnm_cc_20_per_50_per.npy'
            np.save(f_out_name, CC_gnm_20_per_50_per)

            f_out_name = gnm_cc_out_path + os.sep + pdb_name + '_' + chain + '_gnm_cc_greater_60_per.npy'
            np.save(f_out_name, CC_gnm_greater_60_per)

            f_out_name = gnm_sq_out_path + os.sep + pdb_name + '_' + chain + '_gnm_sq_all.npy'
            np.save(f_out_name, gnm_sq_all)

            f_out_name = gnm_prs_out_path + os.sep + pdb_name + '_' + chain + '_gnm_prs_all.npy'
            np.save(f_out_name, gnm_prs_all)

            f_out_name = gnm_prs_out_path + os.sep + pdb_name + '_' + chain + '_gnm_effectiveness_all.npy'
            np.save(f_out_name, gnm_effectiveness_all)

            f_out_name = gnm_prs_out_path + os.sep + pdb_name + '_' + chain + '_gnm_sensitivity_all.npy'
            np.save(f_out_name, gnm_sensitivity_all)

            f_out_name = gnm_eigenvectors_out_path + os.sep + pdb_name + '_' + chain + '_gnm_eigenvectors_all.npy'
            np.save(f_out_name, gnm_eig_all)

            f_out_name = gnm_eigenvectors_out_path + os.sep + pdb_name + '_' + chain + '_gnm_eigenvectors_20.npy'
            np.save(f_out_name, gnm_eig_20)

            f_out_name = gnm_eigenvectors_out_path + os.sep + pdb_name + '_' + chain + '_gnm_eigenvectors_top3.npy'
            np.save(f_out_name, gnm_eig_top3)

            # run ANM model
            anm = ANM(pdb_name)
            anm.buildHessian(calphas, cutoff=15.0, gamma=1)
            anm.calcModes(n_modes=n_modes_n)
            n_modes = anm._n_modes

            anm_Eigvecs_slow = anm[0:slow_num].getEigvecs()
            anm_Eigvecs_all = anm.getEigvecs()
            sqFlucts_all_anm = calcSqFlucts(anm)

            CC_anm_top_3 = calcCrossCorr(anm[0:3])
            print(CC_anm_top_3)
            if int(n_modes * 0.05) >= 1:
                CC_anm_5_per = calcCrossCorr(anm[0:int(n_modes * 0.05)])
            else:
                CC_anm_5_per = calcCrossCorr(anm[0:1])
            if int(n_modes * 0.2) >= 1:
                CC_anm_5_per_20_per = calcCrossCorr(anm[int(n_modes * 0.05):int(n_modes * 0.2)])
            else:
                CC_anm_5_per_20_per = calcCrossCorr(anm[0:1])
            if int(n_modes * 0.5) >= 1:
                CC_anm_20_per_50_per = calcCrossCorr(anm[int(n_modes * 0.2):int(n_modes * 0.5)])
            else:
                CC_anm_20_per_50_per = calcCrossCorr(anm[0:1])
            CC_anm_greater_60_per = calcCrossCorr(anm[int(n_modes * 0.6):])

            anm_sq_all = calcSqFlucts(anm)
            anm_prs_all, anm_effectiveness_all, anm_sensitivity_all = calcPerturbResponse(anm)

            anm_sti = calcMechStiff(anm, calphas)  # (349, 349)

            f_out_name = anm_cc_out_path + os.sep + pdb_name + '_' + chain + '_anm_cc_top3.npy'
            np.save(f_out_name, CC_anm_top_3)

            f_out_name = anm_cc_out_path + os.sep + pdb_name + '_' + chain + '_anm_cc_5_per.npy'
            np.save(f_out_name, CC_anm_5_per)

            f_out_name = anm_cc_out_path + os.sep + pdb_name + '_' + chain + '_anm_cc_5_per_20_per.npy'
            np.save(f_out_name, CC_anm_5_per_20_per)

            f_out_name = anm_cc_out_path + os.sep + pdb_name + '_' + chain + '_anm_cc_20_per_50_per.npy'
            np.save(f_out_name, CC_anm_20_per_50_per)

            f_out_name = anm_cc_out_path + os.sep + pdb_name + '_' + chain + '_anm_cc_greater_60_per.npy'
            np.save(f_out_name, CC_anm_greater_60_per)

            f_out_name = anm_sq_out_path + os.sep + pdb_name + '_' + chain + '_anm_sq_all.npy'
            np.save(f_out_name, anm_sq_all)

            f_out_name = anm_prs_out_path + os.sep + pdb_name + '_' + chain + '_anm_prs_all.npy'
            np.save(f_out_name, anm_prs_all)

            f_out_name = anm_prs_out_path + os.sep + pdb_name + '_' + chain + '_anm_effectiveness_all.npy'
            np.save(f_out_name, anm_effectiveness_all)

            f_out_name = anm_prs_out_path + os.sep + pdb_name + '_' + chain + '_anm_sensitivity_all.npy'
            np.save(f_out_name, anm_sensitivity_all)

            f_out_name = anm_stiffness_out_path + os.sep + pdb_name + '_' + chain + '_anm_stiffness.npy'
            np.save(f_out_name, anm_sti)

            # if n_modes < 100:
            #     CC_anm_top_100 = calcCrossCorr(anm[0:n_modes])
            # else:
            #     CC_anm_top_100 = calcCrossCorr(anm[0:100])

            close()


anm_gnm(rcsb_pdb_file_name_list, rcsb_pdb_chain, rcsb_pdb_path)
anm_gnm(alphafold_pdb_file_name_list, alphafold_pdb_chain, alphafold_pdb_path)






# f_list.close();

