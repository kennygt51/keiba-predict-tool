import os, sys
sys.path.append(os.getcwd())

import HorseTable
import RankResultDfCreate
import sklearn.preprocessing as sp
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
import pandas as pd
import numpy as np

fitdf = RankResultDfCreate.RankResultFitDf(1)

## デバッグ出力
print("------------------------------ MasterDf ------------------------------")
print(fitdf.MasterDf)
print("----------------------------------------------------------------------")

print("------------------------------ Fit_X_Df ------------------------------")
print(fitdf.create_fit_rrdf_X().dtypes)
print(fitdf.create_fit_rrdf_X())
print("----------------------------------------------------------------------")

## デバッグ出力
print("------------------------------ Fit_Y_Df ------------------------------")
print(fitdf.create_fit_rrdf_Y().dtypes)
print(fitdf.create_fit_rrdf_Y())
print("----------------------------------------------------------------------")

predictdf = RankResultDfCreate.RankResultPredictDf("2017110508050212")

## デバッグ出力
print("---------------------------- Predict_X_Df ----------------------------")
print(predictdf.create_predict_rrdf_X().dtypes)
print(predictdf.create_predict_rrdf_X())
print("----------------------------------------------------------------------")
