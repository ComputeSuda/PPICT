from collections import Counter

from sklearn.model_selection import train_test_split, GridSearchCV, cross_val_score
from sklearn.ensemble import RandomForestClassifier

from cal_metric import cal_two_class_metric
from cal_metric import cal_two_class_roc
from Generate_sample import read_samples_1d

import numpy as np


def Rf_model(train_path, test_path):  # flag:True(seq), False(str)
    train_data, train_label = read_samples_1d(train_path)
    test_data, test_label = read_samples_1d(test_path)
    # print(np.isnan(train_data).any())
    print(train_data.shape, test_data.shape, Counter(train_label))
    # print(train_test_split(read_samples_1d(train_path, flag), test_size=0.3))
    # train_data, test_data, train_label, test_label = train_test_split(test_data, test_label, test_size=0.3)
    print(train_data.shape, test_data.shape, Counter(train_label))
    rf = RandomForestClassifier(n_estimators=500, max_depth=26, random_state=90)
    # rf = RandomForestClassifier(n_estimators=500)
    rf.fit(train_data, train_label)
    score_pre = cross_val_score(rf, train_data, train_label, cv=10).mean()  # cv:fold
    print(score_pre)
    pred_prob = rf.predict_proba(test_data)[:, 1]  # (1167,)
    pred = rf.predict(test_data)
    matrix, metric = cal_two_class_metric(test_label, pred_prob)

    fpr, tpr, threshold = cal_two_class_roc(test_label, pred_prob)

    print(matrix)
    print(metric)
    return test_label, pred, pred_prob, matrix, metric, fpr, tpr, threshold


# for i in range(5):
#     print('i:', i)
#     Rf_model('../Datasets/Samples/W_Struc2vec_Train/sample' + str(i) + '.npy', '../Datasets/Samples/W_Struc2vec_Test/sample' + str(i % 5) + '.npy')
