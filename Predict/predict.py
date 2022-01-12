import time

from model.Rf_model import Rf_model

PPICT_Train_set_path = '..HRF/Samples/PPICT_Train'
PPICT_test_path = './PPICT_features.npy'


def predict(model, Train_samplepath, Test_samplepath, nums, outpath):
    pred_probs = [0]*17  # predict sample nums:17
    preds = [0]*17

    for num in range(nums):
        _, pred, pred_prob, _, _, _, _, _ = model(Train_samplepath + '/sample' + str(num) + '.npy',
                                                  Test_samplepath)

        def add_score(a, b):
            c = []
            for i in range(len(a)):
                c.append(a[i]+b[i])
            return c

        pred_probs = add_score(pred_probs, pred_prob.tolist())
        # preds += pred.tolist()

        def write_result(outpath, pred_probs):
            with open(outpath, 'w') as f:
                f.write(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + '\n')
                for i in range(len(pred_probs)):
                    f.write(str(i)+': '+str(round(pred_probs[i]/nums, 3))+'\t'+str(round(preds[i]/nums, 3))+'\n')
        if num == nums-1:
            write_result(outpath + 'PPICT_predict_scores.txt', pred_probs)


predict(Rf_model, PPICT_Train_set_path, PPICT_test_path, 50, './')

