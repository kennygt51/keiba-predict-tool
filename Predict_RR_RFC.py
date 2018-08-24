import os, sys
root_dir = os.path.abspath(os.path.dirname(__file__))

import HorseTable
import RankResultDfCreate
import pandas as pd
import numpy as np
import sys
import sklearn.preprocessing as sp
import sqlalchemy as sa
from sklearn.model_selection import train_test_split,cross_val_score
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, roc_auc_score, precision_recall_curve, auc, roc_curve

def predict_rr_rfc(racekey_list):
    # モデル生成用説明変数読み込み
    Fit_X = pd.read_csv(root_dir + "/fitcsv/fitrrdfX.csv").as_matrix()
    # モデル生成用目的変数読み込み
    Fit_Y = np.loadtxt(root_dir + "/fitcsv/fitrrdfY.csv",delimiter=",")

    # 決定木の数を指定
    #estimators=1
    estimators=1500
    # RandomForest分類器生成
    rfc = RandomForestClassifier(n_estimators=estimators,random_state=0)

    # 精度チェック 
    ## 学習用データ分割
    X_train, X_test, y_train, y_test = train_test_split(Fit_X, Fit_Y, random_state=0)
    ## モデル生成
    clf = rfc.fit(X_train,y_train)
    y_pred = clf.predict(X_test)
    y_pred_prob = clf.predict_proba(X_test)[:,1]


    for racekey in racekey_list:
        ### 予測
        # 予測対象レースのDataFrame生成
        print(racekey)
        predictdf = RankResultDfCreate.RankResultPredictDf(racekey)
        #print(predictdf)
        # 予測対象レースにおける説明変数DataFrame生成
        sample = predictdf.create_predict_rrdf_X()
        # 予測対象レースの目的変数を予測(0or1)
        #print("---sample---")
        #print(sample)
        y_predict = clf.predict(sample)
        # 予測した結果の所属しているクラスの確率を取得
        clf_probability = clf.predict_proba(sample)[:,1]

        ### 予測結果出力処理
        X_df = predictdf.MasterDf[['Umaban','Bamei']]
        Y_df = pd.DataFrame({'Predicted':np.array(clf_probability) * 100})
        Result_df = X_df.join(Y_df.round(2)).sort_values(by=["Predicted"],ascending=False)
        print("-------GOOD LUCK!!-------")
        print(Result_df)


if __name__ == '__main__':
    racekey_list = sys.argv[1:]
    predict_rr_rfc(racekey_list)
