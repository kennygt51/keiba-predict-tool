import HorseTable
import RankResultDfCreate as rrdf
import sklearn.preprocessing as sp
import pandas as pd
import numpy as np

fitdf = rrdf.RankResultFitDf(100)
fitdf.create_fit_rrdf_X().to_csv("fitcsv/fitrrdfX.csv", index=False)
fitdf.create_fit_rrdf_Y().to_csv("fitcsv/fitrrdfY.csv", index=False)
 
