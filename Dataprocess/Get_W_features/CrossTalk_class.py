import os


class InterCrossTalk:
    def __init__(self, Pro_name1, UniprotId1, Site1, Site1Type, PdbChain1, PdbSite1,
                 Pro_name2, UniprotId2, Site2, Site2Type, PdbChain2, PdbSite2, PPI_flag):
        self.Pro_name1 = Pro_name1
        self.UniprotId1 = UniprotId1
        self.UniprotSite1 = int(Site1[1:])
        self.UniprotSite1Type = Site1Type
        self.PdbChain1 = PdbChain1
        self.PdbSite1 = PdbSite1
        self.Pro_name2 = Pro_name2
        self.UniprotId2 = UniprotId2
        self.UniprotSite2 = int(Site2[1:])
        self.UniprotSite2Type = Site2Type
        self.PdbChain2 = PdbChain2
        self.PdbSite2 = PdbSite2
        self.PPI_flag = PPI_flag
        self.uniprot1_pdbchain_feature = dict()
        self.uniprot1_uniprot_feature = dict()
        self.uniprot2_pdbchain_feature = dict()
        self.uniprot2_uniprot_feature = dict()
        self.features = dict()
        self.alphafold_pdbs = ['P51451_A', 'Q9UKX2_A', 'P42229_A', 'O75528_A', 'Q05513_A', 'Q9UKI8_A', 'P09769_A',
                               'O43561_A']
        # print(type(self.uniprot1_pdbchain_feature))
        if self.PdbChain1.upper() in self.alphafold_pdbs:
            self.PdbChain1 = self.PdbChain1.upper()
        if self.PdbChain2.upper() in self.alphafold_pdbs:
            self.PdbChain2 = self.PdbChain2.upper()

    '''
    Str features
    pdbchain_files(pdb, chain, pdbsite):
    # cij(betweenness, clossness, degree, cluster, diversity, eccentricity, strength, eigen_centrality, page_rank)
    cij(betweenness, closeness, degree, cluster, eccentricity, eigen_centrality)
    
    anm_cc(5_per, 5_per_20_per, 20_per_50_per, greater_60_per, top3)
    anm_prs(effectiveness, prs, sensitivity)
    anm_sq(sq)
    anm_stiffness(stiffness)
    gnm_cc(5_per, 5_per_20_per, 20_per_50_per, greater_60_per, top3)
    gnm_eigenvector(eigenvector_20, eigenvector_all, eigenvector_top3)
    gnm_prs(effectiveness, prs, sensitivity)
    gnm_sq(sq)
    '''

    def pdbchain_feature_cij(self, pdbchain_cij_path):
        files = os.listdir(pdbchain_cij_path)
        PdbChain1 = self.PdbChain1
        PdbChain2 = self.PdbChain2
        PdbSite1 = self.PdbSite1
        PdbSite2 = self.PdbSite2
        pdbChain1_files = []
        pdbChain2_files = []
        features_1 = ['betweenness', 'closeness', 'degree', 'cluster', 'eccentricity', 'eigen_centrality']
        if PdbSite1 == 'None' and PdbSite2 == 'None':
            for feature_1 in features_1:
                feature_name = feature_1 + '_cij'
                self.uniprot1_pdbchain_feature[feature_name] = 'None'
                self.uniprot2_pdbchain_feature[feature_name] = 'None'
                self.features[feature_name] = 'None'
        elif PdbSite1 != 'None' and PdbSite2 == 'None':
            for file in files:
                if PdbChain1 in file:
                    pdbChain1_files.append(file)
            for pdbChain1_file in pdbChain1_files:
                print(pdbChain1_file)
                with open(pdbchain_cij_path + '\\' + pdbChain1_file, 'r') as f:
                    datas = f.readlines()
                    feature_name = '_'.join(pdbChain1_file.split('_')[2:-1]) + '_cij'
                    self.uniprot1_pdbchain_feature[feature_name] = str(datas[PdbSite1 - 1].strip('\n').split(':')[1])
                    if self.uniprot1_pdbchain_feature[feature_name] != 'NA':
                        self.uniprot1_pdbchain_feature[feature_name] = str(
                            datas[PdbSite1 - 1].strip('\n').split(':')[1])
                        self.features[feature_name] = str(datas[PdbSite1 - 1].strip('\n').split(':')[1])
                    else:
                        self.uniprot1_pdbchain_feature[feature_name] = 0
                        self.features[feature_name] = str(0)
                    self.uniprot2_pdbchain_feature[feature_name] = 'None'
        elif PdbSite1 == 'None' and PdbSite2 != 'None':
            for file in files:
                if PdbChain2 in file:
                    pdbChain2_files.append(file)
            for pdbChain2_file in pdbChain2_files:
                print(pdbChain2_file)
                with open(pdbchain_cij_path + '\\' + pdbChain2_file, 'r') as f:
                    datas = f.readlines()
                    feature_name = '_'.join(pdbChain2_file.split('_')[2:-1]) + '_cij'
                    self.uniprot2_pdbchain_feature[feature_name] = str(datas[PdbSite2 - 1].strip('\n').split(':')[1])
                    if self.uniprot2_pdbchain_feature[feature_name] != 'NA':
                        self.uniprot2_pdbchain_feature[feature_name] = str(
                            datas[PdbSite2 - 1].strip('\n').split(':')[1])
                        self.features[feature_name] = str(datas[PdbSite2 - 1].strip('\n').split(':')[1])
                    else:
                        self.uniprot2_pdbchain_feature[feature_name] = str(0)
                        self.features[feature_name] = str(0)
                    self.uniprot1_pdbchain_feature[feature_name] = 'None'
        else:
            for file in files:
                if PdbChain1 in file:
                    pdbChain1_files.append(file)
                if PdbChain2 in file:
                    pdbChain2_files.append(file)
            for i in range(len(pdbChain1_files)):
                print(pdbChain1_files[i], pdbChain2_files[i])
                feature_name = '_'.join(pdbChain1_files[i].split('_')[2:-1]) + '_cij'
                with open(pdbchain_cij_path + '\\' + pdbChain1_files[i], 'r') as f1:
                    datas1 = f1.readlines()
                    if datas1[PdbSite1 - 1].strip('\n').split(':')[1] == 'NA':
                        self.uniprot1_pdbchain_feature[feature_name] = 0
                    else:
                        self.uniprot1_pdbchain_feature[feature_name] = float(
                            datas1[self.PdbSite1 - 1].strip('\n').split(':')[1])
                with open(pdbchain_cij_path + '\\' + pdbChain2_files[i], 'r') as f2:
                    datas2 = f2.readlines()
                    if datas2[PdbSite2 - 1].strip('\n').split(':')[1] == 'NA':
                        self.uniprot2_pdbchain_feature[feature_name] = 0
                    else:
                        self.uniprot2_pdbchain_feature[feature_name] = float(
                            datas2[PdbSite2 - 1].strip('\n').split(':')[1])
                self.features[feature_name] = str(
                    (self.uniprot1_pdbchain_feature[feature_name] + self.uniprot2_pdbchain_feature[feature_name]) / 2)

    def pdbchain_feature_anm_cc(self, anm_cc_path):
        files = os.listdir(anm_cc_path)
        PdbChain1 = self.PdbChain1
        PdbChain2 = self.PdbChain2
        PdbSite1 = self.PdbSite1
        PdbSite2 = self.PdbSite2
        pdbChain1_files = []
        pdbChain2_files = []
        features_1 = ['5_per', '5_per_20_per', '20_per_50_per', 'greater_60_per', 'top3']
        if PdbSite1 == 'None' and PdbSite2 == 'None':
            for feature_1 in features_1:
                feature_name = 'anm_cc_' + feature_1
                self.uniprot1_pdbchain_feature[feature_name] = 'None'
                self.uniprot2_pdbchain_feature[feature_name] = 'None'
                self.features[feature_name] = 'None'
        elif PdbSite1 != 'None' and PdbSite2 == 'None':
            for file in files:
                if PdbChain1 in file:
                    pdbChain1_files.append(file)
            for pdbChain1_file in pdbChain1_files:
                print(pdbChain1_file)
                with open(anm_cc_path + '\\' + pdbChain1_file, 'r') as f:
                    datas = f.readlines()
                    feature_name = '_'.join(pdbChain1_file.split('.')[0].split('_')[2:])
                    self.uniprot1_pdbchain_feature[feature_name] = str(
                        datas[PdbSite1 - 1].strip('\n').split(':')[1].strip('[]').split(',')
                        [PdbSite1 - 1].strip())
                    self.uniprot2_pdbchain_feature[feature_name] = 'None'
                    self.features[feature_name] = str(
                        datas[PdbSite1 - 1].strip('\n').split(':')[1].strip('[]').split(',')
                        [PdbSite1 - 1].strip())
        elif PdbSite1 == 'None' and PdbSite2 != 'None':
            for file in files:
                if PdbChain2 in file:
                    pdbChain2_files.append(file)
            for pdbChain2_file in pdbChain2_files:
                print(pdbChain2_file)
                with open(anm_cc_path + '\\' + pdbChain2_file, 'r') as f:
                    datas = f.readlines()
                    feature_name = '_'.join(pdbChain2_file.split('.')[0].split('_')[2:])
                    self.uniprot2_pdbchain_feature[feature_name] = str(
                        datas[PdbSite2 - 1].strip('\n').split(':')[1].strip('[]').split(',')
                        [PdbSite2 - 1].strip())
                    self.features[feature_name] = str(
                        datas[PdbSite2 - 1].strip('\n').split(':')[1].strip('[]').split(',')
                        [PdbSite2 - 1].strip())
                    self.uniprot1_pdbchain_feature[feature_name] = 'None'
        else:
            for file in files:
                if PdbChain1 in file:
                    pdbChain1_files.append(file)
                if PdbChain2 in file:
                    pdbChain2_files.append(file)
            for i in range(len(pdbChain1_files)):
                print(pdbChain1_files[i], pdbChain2_files[i])
                feature_name = '_'.join(pdbChain1_files[i].split('.')[0].split('_')[2:])
                with open(anm_cc_path + '\\' + pdbChain1_files[i], 'r') as f:
                    datas = f.readlines()
                    self.uniprot1_pdbchain_feature[feature_name] = \
                        float(datas[PdbSite1 - 1].strip('\n').split(':')[1].strip('[]').split(',')[
                                  PdbSite1 - 1].strip())
                with open(anm_cc_path + '\\' + pdbChain2_files[i], 'r') as f2:
                    datas = f2.readlines()
                    self.uniprot2_pdbchain_feature[feature_name] = \
                        float(datas[PdbSite2 - 1].strip('\n').split(':')[1].strip('[]').split(',')[
                                  PdbSite2 - 1].strip())
                self.features[feature_name] = str(
                    (self.uniprot1_pdbchain_feature[feature_name] + self.uniprot2_pdbchain_feature[feature_name]) / 2)

    def pdbchain_feature_anm_prs(self, anm_prs_path):
        files = os.listdir(anm_prs_path)
        PdbChain1 = self.PdbChain1
        PdbChain2 = self.PdbChain2
        PdbSite1 = self.PdbSite1
        PdbSite2 = self.PdbSite2
        pdbChain1_files = []
        pdbChain2_files = []
        features_1 = ['effectiveness_all', 'sensitivity_all']
        features_2 = ['prs_all']
        if PdbSite1 == 'None' and PdbSite2 == 'None':
            for feature_1 in features_1:
                feature_name = 'anm_' + feature_1
                self.uniprot1_pdbchain_feature[feature_name] = 'None'
                self.uniprot2_pdbchain_feature[feature_name] = 'None'
                self.features[feature_name] = 'None'
            for feature_2 in features_2:
                feature_name = 'anm_' + feature_2
                self.uniprot1_pdbchain_feature[feature_name] = 'None'
                self.uniprot2_pdbchain_feature[feature_name] = 'None'
                self.features[feature_name] = 'None'
        elif PdbSite1 != 'None' and PdbSite2 == 'None':
            for file in files:
                if PdbChain1 in file:
                    pdbChain1_files.append(file)
            for pdbChain1_file in pdbChain1_files:
                print(pdbChain1_file)
                if 'prs' in pdbChain1_file:
                    with open(anm_prs_path + '\\' + pdbChain1_file, 'r') as f:
                        datas = f.readlines()
                        feature_name = '_'.join(pdbChain1_file.split('.')[0].split('_')[2:])
                        self.uniprot2_pdbchain_feature[feature_name] = 'None'
                        self.uniprot1_pdbchain_feature[feature_name] = str(
                            datas[PdbSite1 - 1].strip('\n').split(':')[1].strip('[]').split(',')
                            [PdbSite1 - 1].strip())
                        self.features[feature_name] = str(
                            datas[PdbSite1 - 1].strip('\n').split(':')[1].strip('[]').split(',')
                            [PdbSite1 - 1].strip())
                elif 'effectiveness' in pdbChain1_file:
                    with open(anm_prs_path + '\\' + pdbChain1_file, 'r') as f:
                        datas = f.readlines()
                        feature_name = '_'.join(pdbChain1_file.split('.')[0].split('_')[2:])
                        self.uniprot2_pdbchain_feature[feature_name] = 'None'
                        self.uniprot1_pdbchain_feature[feature_name] = str(
                            datas[PdbSite1 - 1].strip('\n').split(':')[1])
                        self.features[feature_name] = str(datas[PdbSite1 - 1].strip('\n').split(':')[1])
                elif 'sensitivity' in pdbChain1_file:
                    with open(anm_prs_path + '\\' + pdbChain1_file, 'r') as f:
                        datas = f.readlines()
                        feature_name = '_'.join(pdbChain1_file.split('.')[0].split('_')[2:])
                        self.uniprot2_pdbchain_feature[feature_name] = 'None'
                        self.uniprot1_pdbchain_feature[feature_name] = str(
                            datas[PdbSite1 - 1].strip('\n').split(':')[1])
                        self.features[feature_name] = str(datas[PdbSite1 - 1].strip('\n').split(':')[1])
        elif PdbSite1 == 'None' and PdbSite2 != 'None':
            for file in files:
                if PdbChain2 in file:
                    pdbChain2_files.append(file)
            for pdbChain2_file in pdbChain2_files:
                print(pdbChain2_file)
                if 'prs' in pdbChain2_file:
                    with open(anm_prs_path + '\\' + pdbChain2_file, 'r') as f:
                        datas = f.readlines()
                        feature_name = '_'.join(pdbChain2_file.split('.')[0].split('_')[2:])
                        # matrixs = [float(item.strip()) for item in datas[PdbSite2 - 1].strip('\n').split(':')[1].strip('[]').split(',')]
                        self.uniprot1_pdbchain_feature[feature_name] = 'None'
                        self.uniprot2_pdbchain_feature[feature_name] = str(
                            datas[PdbSite2 - 1].strip('\n').split(':')[1].strip('[]').split(',')
                            [PdbSite2 - 1].strip())
                        self.features[feature_name] = str(
                            datas[PdbSite2 - 1].strip('\n').split(':')[1].strip('[]').split(',')
                            [PdbSite2 - 1].strip())
                elif 'effectiveness' in pdbChain2_file:
                    with open(anm_prs_path + '\\' + pdbChain2_file, 'r') as f:
                        datas = f.readlines()
                        feature_name = '_'.join(pdbChain2_file.split('.')[0].split('_')[2:])
                        self.uniprot1_pdbchain_feature[feature_name] = 'None'
                        self.uniprot2_pdbchain_feature[feature_name] = str(
                            datas[PdbSite2 - 1].strip('\n').split(':')[1])
                        self.features[feature_name] = str(datas[PdbSite2 - 1].strip('\n').split(':')[1])
                elif 'sensitivity' in pdbChain2_file:
                    with open(anm_prs_path + '\\' + pdbChain2_file, 'r') as f:
                        datas = f.readlines()
                        feature_name = '_'.join(pdbChain2_file.split('.')[0].split('_')[2:])
                        self.uniprot1_pdbchain_feature[feature_name] = 'None'
                        self.uniprot2_pdbchain_feature[feature_name] = datas[PdbSite2 - 1].strip('\n').split(':')[1]
                        self.features[feature_name] = str(datas[PdbSite2 - 1].strip('\n').split(':')[1])
        else:
            for file in files:
                if PdbChain1 in file:
                    pdbChain1_files.append(file)
                if PdbChain2 in file:
                    pdbChain2_files.append(file)
            for i in range(len(pdbChain1_files)):
                feature_name = '_'.join(pdbChain1_files[i].split('.')[0].split('_')[2:])
                print(pdbChain1_files[i], pdbChain2_files[2])
                if 'prs' in feature_name:
                    with open(anm_prs_path + '\\' + pdbChain1_files[i], 'r') as f1:
                        datas1 = f1.readlines()
                        # matrixs1 = [float(item.strip()) for item in
                        #             datas1[PdbSite1 - 1].strip('\n').split(':')[1].strip('[]').split(',')]
                        self.uniprot1_pdbchain_feature[feature_name] = str(
                            datas1[PdbSite1 - 1].strip('\n').split(':')[1].strip('[]').split(',')
                            [PdbSite1 - 1].strip())
                    with open(anm_prs_path + '\\' + pdbChain2_files[i], 'r') as f2:
                        datas2 = f2.readlines()
                        # matrixs2 = [float(item.strip()) for item in
                        #             datas2[PdbSite2 - 1].strip('\n').split(':')[1].strip('[]').split(',')]
                        self.uniprot2_pdbchain_feature[feature_name] = str(
                            datas2[PdbSite2 - 1].strip('\n').split(':')[1].strip('[]').split(',')
                            [PdbSite2 - 1].strip())
                    self.features[feature_name] = str((float(self.uniprot1_pdbchain_feature[feature_name]) + float(
                        self.uniprot2_pdbchain_feature[feature_name])) / 2)
                elif 'effectiveness' in feature_name:
                    with open(anm_prs_path + '\\' + pdbChain1_files[i], 'r') as f1:
                        datas1 = f1.readlines()
                        self.uniprot1_pdbchain_feature[feature_name] = str(
                            datas1[PdbSite1 - 1].strip('\n').split(':')[1])
                    with open(anm_prs_path + '\\' + pdbChain2_files[i], 'r') as f2:
                        datas2 = f2.readlines()
                        self.uniprot2_pdbchain_feature[feature_name] = str(
                            datas2[PdbSite2 - 1].strip('\n').split(':')[1])
                    self.features[feature_name] = str((float(self.uniprot1_pdbchain_feature[feature_name]) + float(
                        self.uniprot2_pdbchain_feature[feature_name])) / 2)
                elif 'sensitivity' in feature_name:
                    with open(anm_prs_path + '\\' + pdbChain1_files[i], 'r') as f1:
                        datas1 = f1.readlines()
                        self.uniprot1_pdbchain_feature[feature_name] = str(
                            datas1[PdbSite1 - 1].strip('\n').split(':')[1])
                    with open(anm_prs_path + '\\' + pdbChain2_files[i], 'r') as f2:
                        datas2 = f2.readlines()
                        self.uniprot2_pdbchain_feature[feature_name] = str(
                            datas2[PdbSite2 - 1].strip('\n').split(':')[1])
                    self.features[feature_name] = str((float(self.uniprot1_pdbchain_feature[feature_name]) + float(
                        self.uniprot2_pdbchain_feature[feature_name])) / 2)

    def pdbchain_feature_anm_sq(self, anm_sq_path):
        files = os.listdir(anm_sq_path)
        PdbChain1 = self.PdbChain1
        PdbChain2 = self.PdbChain2
        PdbSite1 = self.PdbSite1
        PdbSite2 = self.PdbSite2
        pdbChain1_files = []
        pdbChain2_files = []
        features_1 = ['sq_all']
        if PdbSite1 == 'None' and PdbSite2 == 'None':
            for feature_1 in features_1:
                feature_name = 'anm_' + feature_1
                self.uniprot1_pdbchain_feature[feature_name] = 'None'
                self.uniprot2_pdbchain_feature[feature_name] = 'None'
                self.features[feature_name] = 'None'
        elif PdbSite1 != 'None' and PdbSite2 == 'None':
            for file in files:
                if PdbChain1 in file:
                    pdbChain1_files.append(file)
            for pdbChain1_file in pdbChain1_files:
                print(pdbChain1_file)
                with open(anm_sq_path + '\\' + pdbChain1_file, 'r') as f:
                    datas = f.readlines()
                    feature_name = '_'.join(pdbChain1_file.split('.')[0].split('_')[2:])
                    self.uniprot1_pdbchain_feature[feature_name] = str(
                        datas[PdbSite1 - 1].strip('\n').split(':')[1])
                    self.uniprot2_pdbchain_feature[feature_name] = 'None'
                    self.features[feature_name] = str(
                        datas[PdbSite1 - 1].strip('\n').split(':')[1])
        elif PdbSite1 == 'None' and PdbSite2 != 'None':
            for file in files:
                if PdbChain2 in file:
                    pdbChain2_files.append(file)
            for pdbChain2_file in pdbChain2_files:
                print(pdbChain2_file)
                with open(anm_sq_path + '\\' + pdbChain2_file, 'r') as f:
                    datas = f.readlines()
                    feature_name = '_'.join(pdbChain2_file.split('.')[0].split('_')[2:])
                    self.uniprot2_pdbchain_feature[feature_name] = str(
                        datas[self.PdbSite2 - 1].strip('\n').split(':')[1])
                    self.uniprot1_pdbchain_feature[feature_name] = 'None'
                    self.features[feature_name] = str(datas[self.PdbSite2 - 1].strip('\n').split(':')[1])
        else:
            for file in files:
                if PdbChain1 in file:
                    pdbChain1_files.append(file)
                if PdbChain2 in file:
                    pdbChain2_files.append(file)
            for i in range(len(pdbChain1_files)):
                print(pdbChain1_files[i], pdbChain2_files[i])
                feature_name = '_'.join(pdbChain1_files[i].split('.')[0].split('_')[2:])
                with open(anm_sq_path + '\\' + pdbChain1_files[i], 'r') as f1:
                    datas1 = f1.readlines()
                    self.uniprot1_pdbchain_feature[feature_name] = str(
                        datas1[self.PdbSite1 - 1].strip('\n').split(':')[1])
                with open(anm_sq_path + '\\' + pdbChain2_files[i], 'r') as f2:
                    datas2 = f2.readlines()
                    self.uniprot2_pdbchain_feature[feature_name] = str(
                        datas2[self.PdbSite2 - 1].strip('\n').split(':')[1])
                self.features[feature_name] = str(
                    (float(self.uniprot1_pdbchain_feature[feature_name]) + float(
                        self.uniprot2_pdbchain_feature[feature_name])) / 2)

    def pdbchain_feature_anm_stiffness(self, anm_stiffness_path):
        files = os.listdir(anm_stiffness_path)
        features_1 = ['stiffness']
        PdbChain1 = self.PdbChain1
        PdbChain2 = self.PdbChain2
        PdbSite1 = self.PdbSite1
        PdbSite2 = self.PdbSite2
        pdbChain1_files = []
        pdbChain2_files = []
        if PdbSite1 == 'None' and PdbSite2 == 'None':
            for feature_1 in features_1:
                feature_name = 'anm_' + feature_1
                self.uniprot1_pdbchain_feature[feature_name] = 'None'
                self.uniprot2_pdbchain_feature[feature_name] = 'None'
                self.features[feature_name] = 'None'
        elif PdbSite1 != 'None' and PdbSite2 == 'None':
            for file in files:
                if PdbChain1 in file:
                    pdbChain1_files.append(file)
            for pdbChain1_file in pdbChain1_files:
                print(pdbChain1_file)
                with open(anm_stiffness_path + '\\' + pdbChain1_file, 'r') as f:
                    datas = f.readlines()
                    feature_name = '_'.join(pdbChain1_file.split('.')[0].split('_')[2:])
                    self.uniprot1_pdbchain_feature[feature_name] = str(
                        datas[self.PdbSite1 - 1].strip('\n').split(':')[1].strip('[]').split(',')
                        [self.PdbSite1 - 1].strip())
                    self.uniprot2_pdbchain_feature[feature_name] = 'None'
                    self.features[feature_name] = str(
                        datas[self.PdbSite1 - 1].strip('\n').split(':')[1].strip('[]').split(',')
                        [self.PdbSite1 - 1].strip())
        elif PdbSite1 == 'None' and PdbSite2 != 'None':
            for file in files:
                if PdbChain2 in file:
                    pdbChain2_files.append(file)
            for pdbChain2_file in pdbChain2_files:
                print(pdbChain2_file)
                with open(anm_stiffness_path + '\\' + pdbChain2_file, 'r') as f:
                    datas = f.readlines()
                    feature_name = '_'.join(pdbChain2_file.split('.')[0].split('_')[2:])
                    self.uniprot1_pdbchain_feature[feature_name] = 'None'
                    self.uniprot2_pdbchain_feature[feature_name] = str(
                        datas[self.PdbSite2 - 1].strip('\n').split(':')[1].strip('[]').split(',')
                        [self.PdbSite2 - 1].strip())
                    self.features[feature_name] = str(
                        datas[self.PdbSite2 - 1].strip('\n').split(':')[1].strip('[]').split(',')
                        [self.PdbSite2 - 1].strip())
        else:
            for file in files:
                if PdbChain1 in file:
                    pdbChain1_files.append(file)
                if PdbChain2 in file:
                    pdbChain2_files.append(file)
            for i in range(len(pdbChain1_files)):
                print(pdbChain1_files[i], pdbChain2_files[i])
                feature_name = '_'.join(pdbChain1_files[i].split('.')[0].split('_')[2:])
                with open(anm_stiffness_path + '\\' + pdbChain1_files[i], 'r') as f:
                    datas = f.readlines()
                    self.uniprot1_pdbchain_feature[feature_name] = \
                        str(datas[self.PdbSite1 - 1].strip('\n').split(':')[1].strip('[]').split(',')[
                                self.PdbSite1 - 1].strip())
                with open(anm_stiffness_path + '\\' + pdbChain2_files[i], 'r') as f2:
                    datas = f2.readlines()
                    self.uniprot2_pdbchain_feature[feature_name] = \
                        str(datas[self.PdbSite2 - 1].strip('\n').split(':')[1].strip('[]').split(',')[
                                self.PdbSite2 - 1].strip())
                self.features[feature_name] = str(
                    (float(self.uniprot1_pdbchain_feature[feature_name]) + float(
                        self.uniprot2_pdbchain_feature[feature_name])) / 2)

    def pdbchain_feature_gnm_cc(self, gnm_cc_path):
        files = os.listdir(gnm_cc_path)
        PdbChain1 = self.PdbChain1
        PdbChain2 = self.PdbChain2
        PdbSite1 = self.PdbSite1
        PdbSite2 = self.PdbSite2
        pdbChain1_files = []
        pdbChain2_files = []
        features_1 = ['5_per', '5_per_20_per', '20_per_50_per', 'greater_60_per', 'top3']
        if PdbSite1 == 'None' and PdbSite2 == 'None':
            for feature_1 in features_1:
                feature_name = 'gnm_cc_' + feature_1
                self.uniprot1_pdbchain_feature[feature_name] = 'None'
                self.uniprot2_pdbchain_feature[feature_name] = 'None'
                self.features[feature_name] = 'None'
        elif PdbSite1 != 'None' and PdbSite2 == 'None':
            for file in files:
                if PdbChain1 in file:
                    pdbChain1_files.append(file)
            for pdbChain1_file in pdbChain1_files:
                print(pdbChain1_file)
                with open(gnm_cc_path + '\\' + pdbChain1_file, 'r') as f:
                    datas = f.readlines()
                    feature_name = '_'.join(pdbChain1_file.split('.')[0].split('_')[2:])
                    self.uniprot1_pdbchain_feature[feature_name] = str(
                        datas[PdbSite1 - 1].strip('\n').split(':')[1].strip('[]').split(',')
                        [PdbSite1 - 1].strip())
                    self.uniprot2_pdbchain_feature[feature_name] = 'None'
                    self.features[feature_name] = str(
                        datas[PdbSite1 - 1].strip('\n').split(':')[1].strip('[]').split(',')
                        [PdbSite1 - 1].strip())
        elif PdbSite1 == 'None' and PdbSite2 != 'None':
            for file in files:
                if PdbChain2 in file:
                    pdbChain2_files.append(file)
            for pdbChain2_file in pdbChain2_files:
                print(pdbChain2_file)
                with open(gnm_cc_path + '\\' + pdbChain2_file, 'r') as f:
                    datas = f.readlines()
                    feature_name = '_'.join(pdbChain2_file.split('.')[0].split('_')[2:])
                    self.uniprot1_pdbchain_feature[feature_name] = 'None'
                    self.uniprot2_pdbchain_feature[feature_name] = str(
                        datas[PdbSite2 - 1].strip('\n').split(':')[1].strip('[]').split(',')
                        [PdbSite2 - 1].strip())
                    self.features[feature_name] = str(
                        datas[PdbSite2 - 1].strip('\n').split(':')[1].strip('[]').split(',')
                        [PdbSite2 - 1].strip())
        else:
            for file in files:
                if PdbChain1 in file:
                    pdbChain1_files.append(file)
                if PdbChain2 in file:
                    pdbChain2_files.append(file)
            for i in range(len(pdbChain1_files)):
                print(pdbChain1_files[i], pdbChain2_files[i])
                feature_name = '_'.join(pdbChain1_files[i].split('.')[0].split('_')[2:])
                with open(gnm_cc_path + '\\' + pdbChain1_files[i], 'r') as f:
                    datas = f.readlines()
                    self.uniprot1_pdbchain_feature[feature_name] = \
                        float(datas[PdbSite1 - 1].strip('\n').split(':')[1].strip('[]').split(',')[
                                  PdbSite1 - 1].strip())
                with open(gnm_cc_path + '\\' + pdbChain2_files[i], 'r') as f2:
                    datas = f2.readlines()
                    self.uniprot2_pdbchain_feature[feature_name] = \
                        float(datas[PdbSite2 - 1].strip('\n').split(':')[1].strip('[]').split(',')[
                                  PdbSite2 - 1].strip())
                self.features[feature_name] = str(
                    (self.uniprot1_pdbchain_feature[feature_name] + self.uniprot2_pdbchain_feature[feature_name]) / 2)

    def pdbchain_feature_gnm_eigenvector(self, gnm_eigenvector_path):
        files = os.listdir(gnm_eigenvector_path)
        PdbChain1 = self.PdbChain1
        PdbChain2 = self.PdbChain2
        PdbSite1 = self.PdbSite1
        PdbSite2 = self.PdbSite2
        pdbChain1_files = []
        pdbChain2_files = []
        features_1 = ['eigenvectors_20', 'eigenvectors_all', 'eigenvectors_top3']
        if PdbSite1 == 'None' and PdbSite2 == 'None':
            for feature_1 in features_1:
                feature_name = 'gnm_' + feature_1
                self.uniprot1_pdbchain_feature[feature_name] = 'None'
                self.uniprot2_pdbchain_feature[feature_name] = 'None'
                self.features[feature_name] = 'None'
        elif PdbSite1 != 'None' and PdbSite2 == 'None':
            for file in files:
                if PdbChain1 in file:
                    pdbChain1_files.append(file)
            for pdbChain1_file in pdbChain1_files:
                print(pdbChain1_file)
                with open(gnm_eigenvector_path + '\\' + pdbChain1_file, 'r') as f:
                    datas = f.readlines()
                    feature_name = '_'.join(pdbChain1_file.split('.')[0].split('_')[2:])
                    self.uniprot1_pdbchain_feature[feature_name] = str(
                        datas[PdbSite1 - 1].strip('\n').split(':')[1])
                    self.uniprot2_pdbchain_feature[feature_name] = 'None'
                    self.features[feature_name] = str(
                        datas[PdbSite1 - 1].strip('\n').split(':')[1])
        elif PdbSite1 == 'None' and PdbSite2 != 'None':
            for file in files:
                if PdbChain2 in file:
                    pdbChain2_files.append(file)
            for pdbChain2_file in pdbChain2_files:
                print(pdbChain2_file)
                with open(gnm_eigenvector_path + '\\' + pdbChain2_file, 'r') as f:
                    datas = f.readlines()
                    feature_name = '_'.join(pdbChain2_file.split('.')[0].split('_')[2:])
                    self.uniprot1_pdbchain_feature[feature_name] = 'None'
                    self.uniprot2_pdbchain_feature[feature_name] = str(datas[PdbSite2 - 1].strip('\n').split(':')[1])
                    self.features[feature_name] = str(datas[PdbSite2 - 1].strip('\n').split(':')[1])
        else:
            for file in files:
                if PdbChain1 in file:
                    pdbChain1_files.append(file)
                if PdbChain2 in file:
                    pdbChain2_files.append(file)
            for i in range(len(pdbChain1_files)):
                print(pdbChain1_files[i], pdbChain2_files[i])
                feature_name = '_'.join(pdbChain1_files[i].split('.')[0].split('_')[2:])
                with open(gnm_eigenvector_path + '\\' + pdbChain1_files[i], 'r') as f1:
                    datas1 = f1.readlines()
                    self.uniprot1_pdbchain_feature[feature_name] = str(datas1[PdbSite1 - 1].strip('\n').split(':')[1])
                with open(gnm_eigenvector_path + '\\' + pdbChain2_files[i], 'r') as f2:
                    datas2 = f2.readlines()
                    self.uniprot2_pdbchain_feature[feature_name] = str(datas2[PdbSite2 - 1].strip('\n').split(':')[1])
                self.features[feature_name] = str(
                    (float(self.uniprot1_pdbchain_feature[feature_name]) + float(
                        self.uniprot2_pdbchain_feature[feature_name])) / 2)

    def pdbchain_feature_gnm_prs(self, gnm_prs_path):
        files = os.listdir(gnm_prs_path)
        PdbChain1 = self.PdbChain1
        PdbChain2 = self.PdbChain2
        PdbSite1 = self.PdbSite1
        PdbSite2 = self.PdbSite2
        pdbChain1_files = []
        pdbChain2_files = []
        features_1 = ['effectiveness_all', 'sensitivity_all']
        features_2 = ['prs_all']
        if PdbSite1 == 'None' and PdbSite2 == 'None':
            for feature_1 in features_1:
                feature_name = 'gnm_' + feature_1
                self.uniprot1_pdbchain_feature[feature_name] = 'None'
                self.uniprot2_pdbchain_feature[feature_name] = 'None'
                self.features[feature_name] = 'None'
            for feature_2 in features_2:
                feature_name = 'gnm_' + feature_2
                self.uniprot1_pdbchain_feature[feature_name] = 'None'
                self.uniprot2_pdbchain_feature[feature_name] = 'None'
                self.features[feature_name] = 'None'
        elif PdbSite1 != 'None' and PdbSite2 == 'None':
            for file in files:
                if PdbChain1 in file:
                    pdbChain1_files.append(file)
            for pdbChain1_file in pdbChain1_files:
                print(pdbChain1_file)
                if 'prs' in pdbChain1_file:
                    with open(gnm_prs_path + '\\' + pdbChain1_file, 'r') as f:
                        datas = f.readlines()
                        feature_name = '_'.join(pdbChain1_file.split('.')[0].split('_')[2:])
                        # matrixs = [float(item.strip(' ')) for item in
                        #            datas[PdbSite1 - 1].strip('\n').split(':')[1].strip('[]').split(',')]
                        # print(feature_name)
                        # print(self.uniprot1_pdbchain_feature[feature_name])
                        # print(self.uniprot1_pdbchain_feature)
                        self.uniprot1_pdbchain_feature[feature_name] = str(
                            datas[PdbSite1 - 1].strip('\n').split(':')[1].strip('[]').split(',')
                            [PdbSite1 - 1].strip())
                        self.uniprot2_pdbchain_feature[feature_name] = 'None'
                        self.features[feature_name] = str(
                            datas[PdbSite1 - 1].strip('\n').split(':')[1].strip('[]').split(',')
                            [PdbSite1 - 1].strip())
                elif 'effectiveness' in pdbChain1_file:
                    with open(gnm_prs_path + '\\' + pdbChain1_file, 'r') as f:
                        datas = f.readlines()
                        feature_name = '_'.join(pdbChain1_file.split('.')[0].split('_')[2:])
                        self.uniprot1_pdbchain_feature[feature_name] = str(
                            datas[PdbSite1 - 1].strip('\n').split(':')[1])
                        self.uniprot2_pdbchain_feature[feature_name] = 'None'
                        self.features[feature_name] = str(datas[PdbSite1 - 1].strip('\n').split(':')[1])
                elif 'sensitivity' in pdbChain1_file:
                    with open(gnm_prs_path + '\\' + pdbChain1_file, 'r') as f:
                        datas = f.readlines()
                        feature_name = '_'.join(pdbChain1_file.split('.')[0].split('_')[2:])
                        self.uniprot1_pdbchain_feature[feature_name] = str(
                            datas[PdbSite1 - 1].strip('\n').split(':')[1])
                        self.uniprot2_pdbchain_feature[feature_name] = 'None'
                        self.features[feature_name] = str(datas[PdbSite1 - 1].strip('\n').split(':')[1])
        elif PdbSite1 == 'None' and PdbSite2 != 'None':
            for file in files:
                if PdbChain2 in file:
                    pdbChain2_files.append(file)
            for pdbChain2_file in pdbChain2_files:
                print(pdbChain2_file)
                if 'prs' in pdbChain2_file:
                    with open(gnm_prs_path + '\\' + pdbChain2_file, 'r') as f:
                        datas = f.readlines()
                        feature_name = '_'.join(pdbChain2_file.split('.')[0].split('_')[2:])
                        # matrixs = [float(item.strip(' ')) for item in
                        #            datas[PdbSite2 - 1].strip('\n').split(':')[1].strip('[]').split(',')]
                        self.uniprot1_pdbchain_feature[feature_name] = 'None'
                        self.uniprot2_pdbchain_feature[feature_name] = str(datas[PdbSite2 - 1].strip('\n').split(':')[1].strip('[]').split(',')
                        [PdbSite2 - 1].strip())
                        self.features[feature_name] = str(datas[PdbSite2 - 1].strip('\n').split(':')[1].strip('[]').split(',')
                        [PdbSite2 - 1].strip())
                elif 'effectiveness' in pdbChain2_file:
                    with open(gnm_prs_path + '\\' + pdbChain2_file, 'r') as f:
                        datas = f.readlines()
                        feature_name = '_'.join(pdbChain2_file.split('.')[0].split('_')[2:])
                        self.uniprot1_pdbchain_feature[feature_name] = 'None'
                        self.uniprot2_pdbchain_feature[feature_name] = str(
                            datas[PdbSite2 - 1].strip('\n').split(':')[1])
                        self.features[feature_name] = str(datas[PdbSite2 - 1].strip('\n').split(':')[1])
                elif 'sensitivity' in pdbChain2_file:
                    with open(gnm_prs_path + '\\' + pdbChain2_file, 'r') as f:
                        datas = f.readlines()
                        feature_name = '_'.join(pdbChain2_file.split('.')[0].split('_')[2:])
                        self.uniprot1_pdbchain_feature[feature_name] = 'None'
                        self.uniprot2_pdbchain_feature[feature_name] = datas[PdbSite2 - 1].strip('\n').split(':')[1]
                        self.features[feature_name] = str(datas[PdbSite2 - 1].strip('\n').split(':')[1])
        else:
            for file in files:
                if PdbChain1 in file:
                    pdbChain1_files.append(file)
                if PdbChain2 in file:
                    pdbChain2_files.append(file)
            for i in range(len(pdbChain1_files)):
                feature_name = '_'.join(pdbChain1_files[i].split('.')[0].split('_')[2:])
                print(pdbChain1_files[i], pdbChain2_files[2])
                if 'prs' in feature_name:
                    with open(gnm_prs_path + '\\' + pdbChain1_files[i], 'r') as f1:
                        datas1 = f1.readlines()
                        # matrixs1 = [float(item.strip()) for item in
                        #             datas1[PdbSite1 - 1].strip('\n').split(':')[1].strip('[]').split(',')]
                        self.uniprot1_pdbchain_feature[feature_name] = str(datas1[PdbSite1 - 1].strip('\n').split(':')[1].strip('[]').split(',')
                        [PdbSite1 - 1].strip())
                    with open(gnm_prs_path + '\\' + pdbChain2_files[i], 'r') as f2:
                        datas2 = f2.readlines()
                        # matrixs2 = [float(item.strip()) for item in
                        #             datas2[PdbSite2 - 1].strip('\n').split(':')[1].strip('[]').split(',')]
                        self.uniprot2_pdbchain_feature[feature_name] = str(datas2[PdbSite2 - 1].strip('\n').split(':')[1].strip('[]').split(',')
                        [PdbSite2 - 1].strip())
                    self.features[feature_name] = str((float(self.uniprot1_pdbchain_feature[feature_name]) + float(
                        self.uniprot2_pdbchain_feature[feature_name])) / 2)
                elif 'effectiveness' in feature_name:
                    with open(gnm_prs_path + '\\' + pdbChain1_files[i], 'r') as f1:
                        datas1 = f1.readlines()
                        self.uniprot1_pdbchain_feature[feature_name] = str(
                            datas1[PdbSite1 - 1].strip('\n').split(':')[1])
                    with open(gnm_prs_path + '\\' + pdbChain2_files[i], 'r') as f2:
                        datas2 = f2.readlines()
                        self.uniprot2_pdbchain_feature[feature_name] = str(
                            datas2[PdbSite2 - 1].strip('\n').split(':')[1])
                    self.features[feature_name] = str((float(self.uniprot1_pdbchain_feature[feature_name]) + float(
                        self.uniprot2_pdbchain_feature[feature_name])) / 2)
                elif 'sensitivity' in feature_name:
                    with open(gnm_prs_path + '\\' + pdbChain1_files[i], 'r') as f1:
                        datas1 = f1.readlines()
                        self.uniprot1_pdbchain_feature[feature_name] = str(
                            datas1[PdbSite1 - 1].strip('\n').split(':')[1])
                    with open(gnm_prs_path + '\\' + pdbChain2_files[i], 'r') as f2:
                        datas2 = f2.readlines()
                        self.uniprot2_pdbchain_feature[feature_name] = str(
                            datas2[PdbSite2 - 1].strip('\n').split(':')[1])
                    self.features[feature_name] = str((float(self.uniprot1_pdbchain_feature[feature_name]) + float(
                        self.uniprot2_pdbchain_feature[feature_name])) / 2)

    def pdbchain_feature_gnm_sq(self, gnm_sq_path):
        files = os.listdir(gnm_sq_path)
        PdbChain1 = self.PdbChain1
        PdbChain2 = self.PdbChain2
        PdbSite1 = self.PdbSite1
        PdbSite2 = self.PdbSite2
        pdbChain1_files = []
        pdbChain2_files = []
        features_1 = ['sq_all']
        if PdbSite1 == 'None' and PdbSite2 == 'None':
            for feature_1 in features_1:
                feature_name = 'gnm_' + feature_1
                self.uniprot1_pdbchain_feature[feature_name] = 'None'
                self.uniprot2_pdbchain_feature[feature_name] = 'None'
                self.features[feature_name] = 'None'
        elif PdbSite1 != 'None' and PdbSite2 == 'None':
            for file in files:
                if PdbChain1 in file:
                    pdbChain1_files.append(file)
            for pdbChain1_file in pdbChain1_files:
                print(pdbChain1_file)
                with open(gnm_sq_path + '\\' + pdbChain1_file, 'r') as f:
                    datas = f.readlines()
                    feature_name = '_'.join(pdbChain1_file.split('.')[0].split('_')[2:])
                    # print(datas[PdbSite1 - 1].strip('\n').split(':'))
                    # print(self.uniprot1_pdbchain_feature[feature_name])
                    self.uniprot1_pdbchain_feature[feature_name] = str(datas[PdbSite1 - 1].strip('\n').split(':')[1])
                    self.uniprot2_pdbchain_feature[feature_name] = 'None'
                    self.features[feature_name] = str(
                        datas[PdbSite1 - 1].strip('\n').split(':')[1])
        elif PdbSite1 == 'None' and PdbSite2 != 'None':
            for file in files:
                if PdbChain2 in file:
                    pdbChain2_files.append(file)
            for pdbChain2_file in pdbChain2_files:
                print(pdbChain2_file)
                with open(gnm_sq_path + '\\' + pdbChain2_file, 'r') as f:
                    datas = f.readlines()
                    feature_name = '_'.join(pdbChain2_file.split('.')[0].split('_')[2:])
                    self.uniprot1_pdbchain_feature[feature_name] = 'None'
                    self.uniprot2_pdbchain_feature[feature_name] = str(
                        datas[self.PdbSite2 - 1].strip('\n').split(':')[1])
                    self.features[feature_name] = str(datas[self.PdbSite2 - 1].strip('\n').split(':')[1])
        else:
            for file in files:
                if PdbChain1 in file:
                    pdbChain1_files.append(file)
                if PdbChain2 in file:
                    pdbChain2_files.append(file)
            for i in range(len(pdbChain1_files)):
                print(pdbChain1_files[i], pdbChain2_files[i])
                feature_name = '_'.join(pdbChain1_files[i].split('.')[0].split('_')[2:])
                with open(gnm_sq_path + '\\' + pdbChain1_files[i], 'r') as f1:
                    datas1 = f1.readlines()
                    self.uniprot1_pdbchain_feature[feature_name] = str(
                        datas1[self.PdbSite1 - 1].strip('\n').split(':')[1])
                with open(gnm_sq_path + '\\' + pdbChain2_files[i], 'r') as f2:
                    datas2 = f2.readlines()
                    self.uniprot2_pdbchain_feature[feature_name] = str(
                        datas2[self.PdbSite2 - 1].strip('\n').split(':')[1])
                self.features[feature_name] = str(
                    (float(self.uniprot1_pdbchain_feature[feature_name]) + float(
                        self.uniprot2_pdbchain_feature[feature_name])) / 2)

    '''
        Seq features
        uniprot_files(evol, uniprot, uniprotsite):
        dirinfo(M*N)
        entropy()
        mifc(M*N)
        mifn(M*N)
        mutinfo(M*N)
        occupancy()
        omes(M*N)
        sca(M*N)
    '''

    def uninprot_feature_evol_dirinfo(self, evol_dirinfo_path):
        files = os.listdir(evol_dirinfo_path)
        UniprotId1 = self.UniprotId1
        UniprotId2 = self.UniprotId2
        p1 = self.UniprotSite1
        p2 = self.UniprotSite2
        feature_name = 'evol_dirinfo'
        for file in files:
            if UniprotId1 == file[:6]:
                print(file)
                with open(evol_dirinfo_path + '\\' + file, 'r') as f1:
                    datas1 = f1.readlines()
                    matrixs1 = [float(item.strip(' ')) for item in
                                datas1[p1 - 1].strip('\n').split(' ')]
                    self.uniprot1_uniprot_feature[feature_name] = str(sum(matrixs1) / len(matrixs1))
            if UniprotId2 == file[:6]:
                print(file)
                with open(evol_dirinfo_path + '\\' + file, 'r') as f2:
                    datas2 = f2.readlines()
                    matrixs2 = [float(item.strip(' ')) for item in
                                datas2[p2 - 1].strip('\n').split(' ')]
                    self.uniprot2_uniprot_feature[feature_name] = str(sum(matrixs2) / len(matrixs2))
        self.features[feature_name] = str((float(self.uniprot1_uniprot_feature[feature_name]) + float(
            self.uniprot2_uniprot_feature[feature_name])) / 2)

    def uninprot_feature_evol_entropy(self, evol_entropy_path):
        files = os.listdir(evol_entropy_path)
        UniprotId1 = self.UniprotId1
        UniprotId2 = self.UniprotId2
        p1 = self.UniprotSite1
        p2 = self.UniprotSite2
        feature_name = 'evol_entropy'
        for file in files:
            if UniprotId1 == file[:6]:
                print(file)
                with open(evol_entropy_path + '\\' + file, 'r') as f1:
                    datas1 = f1.readlines()
                    if datas1[p1 - 1].strip('\n') == 'NA':
                        self.uniprot1_uniprot_feature[feature_name] = str(0)
                    else:
                        self.uniprot1_uniprot_feature[feature_name] = str(datas1[p1 - 1].strip('\n'))
            if UniprotId2 == file[:6]:
                with open(evol_entropy_path + '\\' + file, 'r') as f2:
                    datas2 = f2.readlines()
                    if datas2[p2 - 1].strip('\n') == 'NA':
                        self.uniprot2_uniprot_feature[feature_name] = str(0)
                    else:
                        self.uniprot2_uniprot_feature[feature_name] = str(datas2[p2 - 1].strip('\n'))
        self.features[feature_name] = str((float(self.uniprot1_uniprot_feature[feature_name]) + float(
            self.uniprot2_uniprot_feature[feature_name])) / 2)

    def uninprot_feature_evol_mifc(self, evol_mifc_path):
        files = os.listdir(evol_mifc_path)
        UniprotId1 = self.UniprotId1
        UniprotId2 = self.UniprotId2
        p1 = self.UniprotSite1
        p2 = self.UniprotSite2
        feature_name = 'evol_mifc'
        for file in files:
            if UniprotId1 == file[:6]:
                print(file)
                with open(evol_mifc_path + '\\' + file, 'r') as f1:
                    datas1 = f1.readlines()
                    matrixs1 = [float(item.strip(' ')) for item in
                                datas1[p1 - 1].strip('\n').split(' ')]
                    self.uniprot1_uniprot_feature[feature_name] = str(sum(matrixs1) / len(matrixs1))
            if UniprotId2 == file[:6]:
                print(file)
                with open(evol_mifc_path + '\\' + file, 'r') as f2:
                    datas2 = f2.readlines()
                    matrixs2 = [float(item.strip(' ')) for item in
                                datas2[p2 - 1].strip('\n').split(' ')]
                    self.uniprot2_uniprot_feature[feature_name] = str(sum(matrixs2) / len(matrixs2))
        self.features[feature_name] = str((float(self.uniprot1_uniprot_feature[feature_name]) + float(
            self.uniprot2_uniprot_feature[feature_name])) / 2)

    def uninprot_feature_evol_mifn(self, evol_mifn_path):
        files = os.listdir(evol_mifn_path)
        UniprotId1 = self.UniprotId1
        UniprotId2 = self.UniprotId2
        p1 = self.UniprotSite1
        p2 = self.UniprotSite2
        feature_name = 'evol_mifn'
        for file in files:
            if UniprotId1 == file[:6]:
                print(file)
                with open(evol_mifn_path + '\\' + file, 'r') as f1:
                    datas1 = f1.readlines()
                    matrixs1 = [float(item.strip(' ')) for item in
                                datas1[p1 - 1].strip('\n').split(' ')]
                    self.uniprot1_uniprot_feature[feature_name] = str(sum(matrixs1) / len(matrixs1))
            if UniprotId2 == file[:6]:
                print(file)
                with open(evol_mifn_path + '\\' + file, 'r') as f2:
                    datas2 = f2.readlines()
                    matrixs2 = [float(item.strip(' ')) for item in
                                datas2[p2 - 1].strip('\n').split(' ')]
                    self.uniprot2_uniprot_feature[feature_name] = str(sum(matrixs2) / len(matrixs2))
        self.features[feature_name] = str((float(self.uniprot1_uniprot_feature[feature_name]) + float(
            self.uniprot2_uniprot_feature[feature_name])) / 2)

    def uninprot_feature_evol_mutinfo(self, evol_mutinfo_path):
        files = os.listdir(evol_mutinfo_path)
        UniprotId1 = self.UniprotId1
        UniprotId2 = self.UniprotId2
        p1 = self.UniprotSite1
        p2 = self.UniprotSite2
        feature_name = 'evol_mutinfo'
        for file in files:
            if UniprotId1 == file[:6]:
                print(file)
                with open(evol_mutinfo_path + '\\' + file, 'r') as f1:
                    datas1 = f1.readlines()
                    matrixs1 = [float(item.strip(' ')) for item in
                                datas1[p1 - 1].strip('\n').split(' ')]
                    self.uniprot1_uniprot_feature[feature_name] = str(sum(matrixs1) / len(matrixs1))
            if UniprotId2 == file[:6]:
                print(file)
                with open(evol_mutinfo_path + '\\' + file, 'r') as f2:
                    datas2 = f2.readlines()
                    matrixs2 = [float(item.strip(' ')) for item in
                                datas2[p2 - 1].strip('\n').split(' ')]
                    self.uniprot2_uniprot_feature[feature_name] = str(sum(matrixs2) / len(matrixs2))
        self.features[feature_name] = str((float(self.uniprot1_uniprot_feature[feature_name]) + float(
            self.uniprot2_uniprot_feature[feature_name])) / 2)

    def uninprot_feature_evol_occupancy(self, evol_occupancy_path):
        files = os.listdir(evol_occupancy_path)
        UniprotId1 = self.UniprotId1
        UniprotId2 = self.UniprotId2
        p1 = self.UniprotSite1
        p2 = self.UniprotSite2
        feature_name = 'evol_occupancy'
        for file in files:
            if UniprotId1 == file[:6]:
                print(file)
                with open(evol_occupancy_path + '\\' + file, 'r') as f1:
                    datas1 = f1.readlines()
                    if datas1[p1 - 1].strip('\n') == 'NA':
                        self.uniprot1_uniprot_feature[feature_name] = str(0)
                    else:
                        self.uniprot1_uniprot_feature[feature_name] = str(datas1[p1 - 1].strip('\n'))
            if UniprotId2 == file[:6]:
                with open(evol_occupancy_path + '\\' + file, 'r') as f2:
                    datas2 = f2.readlines()
                    if datas2[p2 - 1].strip('\n') == 'NA':
                        self.uniprot2_uniprot_feature[feature_name] = str(0)
                    else:
                        self.uniprot2_uniprot_feature[feature_name] = str(datas2[p2 - 1].strip('\n'))
        self.features[feature_name] = str((float(self.uniprot1_uniprot_feature[feature_name]) + float(
            self.uniprot2_uniprot_feature[feature_name])) / 2)

    def uninprot_feature_evol_omes(self, evol_omes_path):
        files = os.listdir(evol_omes_path)
        UniprotId1 = self.UniprotId1
        UniprotId2 = self.UniprotId2
        p1 = self.UniprotSite1
        p2 = self.UniprotSite2
        feature_name = 'evol_omes'
        for file in files:
            if UniprotId1 == file[:6]:
                print(file)
                with open(evol_omes_path + '\\' + file, 'r') as f1:
                    datas1 = f1.readlines()
                    matrixs1 = [float(item.strip(' ')) for item in
                                datas1[p1 - 1].strip('\n').split(' ')]
                    self.uniprot1_uniprot_feature[feature_name] = str(sum(matrixs1) / len(matrixs1))
            if UniprotId2 == file[:6]:
                print(file)
                with open(evol_omes_path + '\\' + file, 'r') as f2:
                    datas2 = f2.readlines()
                    matrixs2 = [float(item.strip(' ')) for item in
                                datas2[p2 - 1].strip('\n').split(' ')]
                    self.uniprot2_uniprot_feature[feature_name] = str(sum(matrixs2) / len(matrixs2))
        self.features[feature_name] = str((float(self.uniprot1_uniprot_feature[feature_name]) + float(
            self.uniprot2_uniprot_feature[feature_name])) / 2)

    def uninprot_feature_evol_sca(self, evol_sca_path):
        files = os.listdir(evol_sca_path)
        UniprotId1 = self.UniprotId1
        UniprotId2 = self.UniprotId2
        p1 = self.UniprotSite1
        p2 = self.UniprotSite2
        feature_name = 'evol_sca'
        for file in files:
            if UniprotId1 == file[:6]:
                print(file)
                with open(evol_sca_path + '\\' + file, 'r') as f1:
                    datas1 = f1.readlines()
                    matrixs1 = [float(item.strip(' ')) for item in
                                datas1[p1 - 1].strip('\n').split(' ')]
                    self.uniprot1_uniprot_feature[feature_name] = str(sum(matrixs1) / len(matrixs1))
            if UniprotId2 == file[:6]:
                print(file)
                with open(evol_sca_path + '\\' + file, 'r') as f2:
                    datas2 = f2.readlines()
                    matrixs2 = [float(item.strip(' ')) for item in
                                datas2[p2 - 1].strip('\n').split(' ')]
                    self.uniprot2_uniprot_feature[feature_name] = str(sum(matrixs2) / len(matrixs2))
        self.features[feature_name] = str((float(self.uniprot1_uniprot_feature[feature_name]) + float(
            self.uniprot2_uniprot_feature[feature_name])) / 2)
