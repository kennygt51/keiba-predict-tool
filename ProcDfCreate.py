######################################
# 特徴量データフレームを作成する為の関数
# 予測ツールのキモとなる処理の為、別ファイルで作成している
######################################

import pandas as pd
import HorseTable
import ProcValueEdit as valueedit

### 順位（RankResult）予測の為のDataFrame作成メソッド
def make_rankresult_mdf(MasterDf):
        ### 特徴量追加手順 ###
        #① add_column_listにカラム追加（初期化）
        #② 特徴量格納処理をfor内に追加
        #③ onehot_columns_listに定義追加（名義特徴量の場合のみ）

        # 特徴量カラム初期化
        add_column_list = ['Kyori','TrackKind','BabaStatus','Age','Sex','Syozoku',・・・]
        for column in add_column_list:
            MasterDf[column] = 0

        # データセット（一行）ごとに特徴列に値を格納していく
        for key, row in MasterDf.iterrows():
            ### インスタンス生成処理
            # 馬柱インスタンス生成
            ht = HorseTable.Horse(row['KettoNum'])
            rt = HorseTable.Race(row['RaceKey'])

            # 馬柱インスタンスから情報生成
            horse_info      = ht.get_horse_info()                       # 馬属性情報
            horse_race_info = ht.get_horse_race_info(row['RaceKey'])    # 馬情報（レース毎）
            results         = ht.get_race_results(row['RaceKey'])       # 馬過去成績情報
            held_info       = rt.get_held_info()                        # レース開催情報
            race_info       = rt.get_race_info()                        # レース属性情報

            ### 特徴量取得及び格納処理
            # レース距離
            MasterDf.loc[key,['Kyori']]             =   int(race_info['Kyori'][0])
            # 芝・ダート種別
            MasterDf.loc[key,['TrackKind']]         =   race_info['TrackKind'][0]
            # 馬場状態
            MasterDf.loc[key,['BabaStatus']]        =   race_info['BabaStatus'][0]
            # 馬齢
            MasterDf.loc[key,['Age']]               =   int(horse_race_info['Barei'][0])
            # 性別
            MasterDf.loc[key,['Sex']]               =   str(horse_race_info['SexCD'][0])
            # 所属
            # ・・・
            # ************ 特徴量処理 ************ #

        ### 名義特徴量のワンホットエンコーディング
        # 対象カラムの定義
        onehot_columns_list = [
            {"column":'TrackKind',"suffix_list":[0,1,2,3]},
            {"column":'BabaStatus',"suffix_list":[0,1,2,3,4]},
            {"column":'Sex',"suffix_list":[0,1,2,3]},
            # ・・・
            # ************ 特徴量処理 ************ #
            ]
        # ワンホットエンコーディング実行
        MasterDf = toOneHot(MasterDf,onehot_columns_list)

        return MasterDf


### 名義特徴量をワンホットエンコーディングするメソッド
def toOneHot(MasterDf,onehot_columns_list):
    '''
    ### 引数のonehot_columns_list定義
    ・column:ワンホットエンコーディング対象のカラム名
    ・suffix_list：名義の次元数をリストで定義

    ### example
    onehot_columns_list = [
        {"column":'TrackKind',"suffix_list":[0,1,2,3]},
        {"column":'BabaStatus',"suffix_list":[0,1,2,3,4]}
        ]
    '''

    for column_dict in onehot_columns_list:
        origin_column_name = column_dict["column"]
        MasterDf = pd.get_dummies(MasterDf,columns=[origin_column_name])
        for suffix in column_dict["suffix_list"]:
            onehot_column_name = "{0}_{1}".format(origin_column_name,suffix)
            if onehot_column_name not in MasterDf.columns: MasterDf[onehot_column_name] = pd.Series(0, index=MasterDf.index)

    return MasterDf
