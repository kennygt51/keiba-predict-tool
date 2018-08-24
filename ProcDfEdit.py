# データフレームの値を修正する関数
# データの値修正などの細かいロジックを管理

import pandas as pd
import numpy as np
import sys

# 着順の数値を1着かそうでないかでバイナリ化する（1着：0 2着以下：1）
def rank_result_calassify_1(x):
    if not isinstance(x,int):
        print("[ERROR]rank_result_calassify_1()にint型以外の数値が渡されました。")
        sys.exit()

    if x == 1:
        return 0
    else:
        return 1

# 着順の数値を連対したかそうでないかでバイナリ化する（1〜3着：0 4着以下：1）
def rank_result_calassify_3(x):
    if not isinstance(x,int):
        print("[ERROR]rank_result_calassify_3()にint型以外の数値が渡されました。")
        sys.exit()

    if x >= 4:
        return 0
    else:
        return 1


### データフレームmodify関数
# 引数に指定されたデータフレーム「DBから取得したスキーマのカラム」から「レースキーのカラム」に変換する
def modify_df_union_racekey(df):
    # 結合後、不要となった結合元の列を削除
    df['RaceKey'] = df['Year'] + df['MonthDay'] + df['JyoCD'] + df['Kaiji'] + df['Nichiji'] + df['RaceNum']
    df_drop = df.drop(['Year', 'MonthDay','JyoCD','Kaiji','Nichiji','RaceNum'], axis=1)

    # RaceKeyカラムを先頭に持ってくる
    cols = df_drop.columns.tolist()
    cols = cols[-1:] + cols[:-1]
    df_drop = df_drop[cols]

    return df_drop


# TODO：引数に指定されたデータフレーム「レースキーのカラム」から「DBから取得したスキーマのカラム」に変換する
def modify_df_split_racekey(df):
    return df


### データフレーム
# 目的変数Y（着順予測）の生成変数（引数に3なら連対予測、1なら1着予測）
def modify_rankresult_mdf_y(MasterDf,x):
    print(MasterDf)
    if not isinstance(x,int):
        print("[ERROR]modify_rankresult_mdf_y()の第二引数にint型以外の数値が渡されました。")
        sys.exit()
    elif x != 1 and x != 3:
        print("[ERROR]modify_rankresult_mdf_y()の第二引数に1,3以外の数値が渡されました。")
        sys.exit()

    MasterDf["yResult"] = 0
    if x == 1:
        MasterDf["yResult"] = MasterDf["KakuteiJyuni"].astype(np.int).apply(rank_result_calassify_1)
    elif x == 3:
        MasterDf["yResult"] = MasterDf["KakuteiJyuni"].astype(np.int).apply(rank_result_calassify_3)

    MasterDf = MasterDf.drop('KakuteiJyuni',axis=1).drop('DataKubun',axis=1)

    return MasterDf
