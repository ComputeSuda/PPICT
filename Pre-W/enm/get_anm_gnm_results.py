import numpy as np
import os

'''
get Anm and gnm results

'''


def get_cc_results(ori_path, result_path):
    files = os.listdir(ori_path)
    for file in files:
        print(file)
        ori_file = ori_path + '\\' + file
        cc = np.load(ori_file)
        # print(cc.shape)  # matrix
        for i in range(cc.shape[0]):  # Turn negative into positive
            for j in range(cc.shape[1]):
                if cc[i, j] < 0:
                    cc[i, j] = -cc[i, j]

        # cc_mean = cc.mean(axis=1)  # Average of each row
        # print(cc_mean)
        site_cc = {}
        for i in range(len(cc)):
            site_cc[i] = cc[i].tolist()
        # print(len(site_mean))

        file_name = file[:file.index('.')]
        # print(file_name)

        result_file = result_path + '\\' + file_name + '.txt'
        with open(result_file, 'w') as f:
            for k, v in site_cc.items():
                f.write(str(k + 1) + ':' + str(v) + '\n')

    # break


def get_sq_results(ori_path, result_path):
    files = os.listdir(ori_path)
    for file in files:
        print(file)
        ori_file = ori_path + '\\' + file
        sq = np.load(ori_file)
        # print(sq.shape)  # (111, )
        site_sq = {}
        for i in range(len(sq)):
            site_sq[i] = sq[i].tolist()

        file_name = file[:file.index('.')]
        # print(file_name)  # 1a4m_anm_sq_all

        result_file = result_path + '\\' + file_name + '.txt'
        with open(result_file, 'w') as f:
            for k, v in site_sq.items():
                f.write(str(k + 1) + ':' + str(v) + '\n')

    # break


def get_prs_results(ori_path, result_path):
    files = os.listdir(ori_path)
    for file in files:
        print(file)
        ori_file = ori_path + '\\' + file
        if file.find('prs') != -1:  # If the file name is prs, it means the matrix
            prs = np.load(ori_file)
            # print(prs.shape)  # (349,349)
            # break
            for i in range(prs.shape[0]):  # Turn negative into positive
                for j in range(prs.shape[1]):
                    if prs[i, j] < 0:
                        prs[i, j] = -prs[i, j]

            # prs_mean = prs.mean(axis=1)  # Average of each row

            site_prs = {}
            for i in range(len(prs)):
                site_prs[i] = prs[i].tolist()
            # print(len(site_mean))

            file_name = file[:file.index('.')]
            # print(file_name)

            result_file = result_path + '\\' + file_name + '.txt'
            with open(result_file, 'w') as f:
                for k, v in site_prs.items():
                    f.write(str(k + 1) + ':' + str(v) + '\n')
        elif file.find('effectiveness') != -1:
            effectiveness = np.load(ori_file)
            # print(effectiveness.shape)  # (349,)
            # break
            site_effectiveness = {}
            for i in range(len(effectiveness)):
                site_effectiveness[i] = effectiveness[i]

            file_name = file[:file.index('.')]
            # print(file_name)  # 1a4m_anm_effectiveness_all

            result_file = result_path + '\\' + file_name + '.txt'
            with open(result_file, 'w') as f:
                for k, v in site_effectiveness.items():
                    f.write(str(k + 1) + ':' + str(v) + '\n')
        elif file.find('sensitivity') != -1:
            sensitivity = np.load(ori_file)
            # print(sensitivity.shape)  # (349, )

            site_sensitivity = {}
            for i in range(len(sensitivity)):
                site_sensitivity[i] = sensitivity[i]

            file_name = file[:file.index('.')]
            # print(file_name)  # 1a4m_anm_sensitivity_all
            # break
            result_file = result_path + '\\' + file_name + '.txt'
            with open(result_file, 'w') as f:
                for k, v in site_sensitivity.items():
                    f.write(str(k + 1) + ':' + str(v) + '\n')

    # break


def get_eigenvectors_results(ori_path, result_path):
    files = os.listdir(ori_path)
    for file in files:
        print(file)
        ori_file = ori_path + '\\' + file
        eig = np.load(ori_file)
        # print(eig.shape)  # 1a4m_gnm_eigenvectors_20.npy    (349, 20)
        for i in range(eig.shape[0]):  # Turn negative into positive
            for j in range(eig.shape[1]):
                if eig[i, j] < 0:
                    eig[i, j] = -eig[i, j]

        eig_mean = eig.mean(axis=1)  # 求每行的平均值

        site_eig = {}
        for i in range(len(eig_mean)):
            site_eig[i] = eig_mean[i]
        # print(len(site_mean))

        file_name = file[:file.index('.')]
        print(file_name)

        result_file = result_path + '\\' + file_name + '.txt'
        with open(result_file, 'w') as f:
            for k, v in site_eig.items():
                f.write(str(k + 1) + ':' + str(v) + '\n')


def get_stiffness_results(ori_path, result_path):
    files = os.listdir(ori_path)
    for file in files:
        print(file)
        ori_file = ori_path + '\\' + file
        sti = np.load(ori_file, encoding='bytes', allow_pickle=True)
        # print(sti.shape)  # 1a4m_anm_stiffness.npy    (349, 349) symmetric matrix

        # sti_mean = sti.mean(axis=1)  # Average of each row

        site_sti = {}
        for i in range(len(sti)):
            site_sti[i] = sti[i].tolist()
        # print(len(site_mean))

        file_name = file[:file.index('.')]
        # print(file_name)

        result_file = result_path + '\\' + file_name + '.txt'
        with open(result_file, 'w') as f:
            for k, v in site_sti.items():
                f.write(str(k + 1) + ':' + str(v) + '\n')


if __name__ == '__main__':
    # get cc matrix results
    cc_matrix_anm_path = r'.\anm\cc'
    cc_matrix_gnm_path = r'.\gnm\cc'

    cc_matrix_anm_results = r'.\results\anm\cc'
    cc_matrix_gnm_results = r'.\results\gnm\cc'

    get_cc_results(cc_matrix_anm_path, cc_matrix_anm_results)
    get_cc_results(cc_matrix_gnm_path, cc_matrix_gnm_results)

    # get sq results
    sq_anm_path = r'.\anm\sq'
    sq_gnm_path = r'.\gnm\sq'

    sq_anm_results = r'.\results\anm\sq'
    sq_gnm_results = r'.\results\gnm\sq'

    get_sq_results(sq_anm_path, sq_anm_results)
    get_sq_results(sq_gnm_path, sq_gnm_results)

    # get prs、effectiveness、sensitivity results
    prs_anm_path = r'.\anm\prs'
    prs_gnm_path = r'C.\gnm\prs'

    prs_anm_results = r'.\results\anm\prs'
    prs_gnm_results = r'.\results\gnm\prs'

    get_prs_results(prs_anm_path, prs_anm_results)
    get_prs_results(prs_gnm_path, prs_gnm_results)

    # get eigenvector results
    eigenvector_gnm_path = r'.\gnm\eigenvector'
    eigenvector_gnm_results = r'.\results\gnm\eigenvector'
    get_eigenvectors_results(eigenvector_gnm_path, eigenvector_gnm_results)

    # get stiffness results
    stiffness_anm_path = r'.\anm\stiffness'
    stiffness_anm_results = r'.\results\anm\stiffness'
    get_stiffness_results(stiffness_anm_path, stiffness_anm_results)
