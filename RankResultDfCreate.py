######################################
# 順位（RankResult）予測の為のDataFrame作成クラス
######################################

import pandas as pd
import sqlalchemy as sa
import ProcDfEdit as dfedit
import ProcDfCreate as dfcreate

###############
# RankResultDfスーパークラス：着順を分類問題で予測する
###############
class RankResultDf():
    url = '・・・'
    engine = sa.create_engine(url)

###############
# RankResultDfクラスをスーパークラスとして継承するサブクラス
# 学習の為のマスタDFが1インスタンスとして生成される
###############
class RankResultFitDf(RankResultDf):

    def __init__(self,count):
        '''
        ## 引数
          学習データとして用いるレース数
        ## 処理概要
          ① 1サンプルを1行にしてDataFrameを作成（レースキーと血統IDをセット）
          (②〜③をforで回す)
          ② 馬柱から当該レースキー・血統IDの1レコード分の特徴量を生成する
          ③ ①と②を結合する
        ## 処理ポイント
          ・ORDER BY RACE_KEYしないと、過去のレース情報がないサンプル（データ訴求の限界）にぶち当たる
          ・TODO：障害と新馬戦はデータセットから除く
        '''

        ### 初期処理
        # マスタDataFrameの初期化
        MasterDf = pd.DataFrame()

        ### 対象となるレースのレースキーを取得する
        # クエリ生成（「DataKubun   = "7"」は、成績データのみを対象とする（成績の出たレースのみが、分析の学習データの対象となる）
        getTargetRaceKeys="""
        SELECT
            Year,
            MonthDay,
            JyoCD,
            Kaiji,
            Nichiji,
            RaceNum
        FROM N_RACE
        WHERE
            DataKubun   = "7"
        ORDER BY Year DESC, MonthDay DESC
        LIMIT '{0}'
        """.format(count)
        # クエリ実行
        TargetRaceKeys = RankResultDf.engine.execute(getTargetRaceKeys)

        ### レース毎にデータセットを生成し、全て結合してマスタDataFrameを生成する（1馬番が1データセットとなる）
        for TargetRaceKey in TargetRaceKeys:
            # 対象レースで出走する馬の情報を取得　「DataKubun   = "7"」は、成績データのみを対象とする（成績の出たレースのみが、分析の学習データの対象となる）
            # TODO:LIMIT1は検証用
            getBasisDfQuery="""
            SELECT
                Year,
                MonthDay,
                JyoCD,
                Kaiji,
                Nichiji,
                RaceNum,
                Umaban,
                KettoNum,
            	KakuteiJyuni,
                DataKubun
            FROM N_UMA_RACE
            WHERE
                Year        = '{0}' AND
                MonthDay    = '{1}' AND
                JyoCD       = '{2}' AND
                Kaiji       = '{3}' AND
                Nichiji     = '{4}' AND
                RaceNum     = '{5}' AND
                DataKubun   = "7"
            ORDER BY Umaban ASC
            """.format(TargetRaceKey[0],TargetRaceKey[1],TargetRaceKey[2],TargetRaceKey[3],TargetRaceKey[4],TargetRaceKey[5])
            # クエリ実行
            BasisDf = pd.read_sql_query(getBasisDfQuery,RankResultDf.engine)
            # 出力したマスタに対して、取得したレース毎の情報を、行方向にガシガシ追加していく
            MasterDf = MasterDf.append(BasisDf,ignore_index=True)

        ### DataFrame整理
        # レースキーカラム変換（各カラムを結合してRaceKeyを生成）
        MasterDf = dfedit.modify_df_union_racekey(MasterDf)
        # 基準DataFrame生成処理（テストセットと予測セットで共通のロジックを用いる）
        MasterDf = dfcreate.make_rankresult_mdf(MasterDf)
        # 目的変数Yのバイナリ化（第二引数が3なら3着以内が0に変換、1なら1着のみ1に変換）
        MasterDf = dfedit.modify_rankresult_mdf_y(MasterDf,3)

        self.MasterDf = MasterDf

    # マスタDataFrameから特徴変数Xとして扱うDataFrameを生成するメソッド
    def create_fit_rrdf_X(self):
        preFitRRDF_X = self.MasterDf

        # 特徴変数以外のカラムを削除
        drop_col = ['RaceKey', 'Umaban', 'KettoNum','yResult']
        FitRRDF_X = preFitRRDF_X.drop(drop_col,axis=1)

        # TODO:特徴変数DataFrame前処理
        #Fit_X_Df = dfedit.proc_X_df(Fit_X_Df)

        return FitRRDF_X

    # マスタDataFrameから目的変数Yとして扱うDataFrameを生成するメソッド
    def create_fit_rrdf_Y(self):
        preFitRRDF_Y = self.MasterDf

        # 目的変数のカラムを取得
        FitRRDF_X = preFitRRDF_Y['yResult']

        return FitRRDF_X

###############
# RankResultDfクラスをスーパークラスとして継承するサブクラス
# 予測の為のDataFrameを生成する
###############
class RankResultPredictDf(RankResultDf):

    def __init__(self,race_key):

        '''
        ## 引数
          予測対象とするレースキー
        ## 処理概要
          ① 1サンプルを1行にしてDataFrameを作成（レースキーと血統IDをセット）
          (②〜③をforで回す)
          ② 馬柱から当該レースキー・血統IDの1レコード分の特徴量を生成する
          ③ ①と②を結合する
        ## 処理ポイント
        ## レースキーサンプル
            2017110508050212
        '''

        ### 予測の対象となるレースのレースキーを取得
        # クエリ生成
        getBasisDfQuery="""
            SELECT
                Year,
                MonthDay,
                JyoCD,
                Kaiji,
                Nichiji,
                RaceNum,
                Umaban,
                Bamei,
                KettoNum,
                DataKubun
            FROM N_UMA_RACE
            WHERE
                Year        = '{0}' AND
                MonthDay    = '{1}' AND
                JyoCD       = '{2}' AND
                Kaiji       = '{3}' AND
                Nichiji     = '{4}' AND
                RaceNum     = '{5}'
            ORDER BY Umaban ASC
        """.format(race_key[0:4],race_key[4:8],race_key[8:10],race_key[10:12],race_key[12:14],race_key[14:16])
        # クエリ実行
        MasterDf = pd.read_sql_query(getBasisDfQuery,self.engine)

        ### DataFrame整理
        # レースキーカラム変換（各カラムを結合してRaceKeyを生成）
        MasterDf = dfedit.modify_df_union_racekey(MasterDf)
        # マスタDataFrame生成処理（テストセットと予測セットで共通のロジックを用いる）
        MasterDf = dfcreate.make_rankresult_mdf(MasterDf)
        # Yカラムの初期化
        MasterDf["yResult"] = 0
        MasterDf = MasterDf.drop('DataKubun',axis=1)

        self.MasterDf = MasterDf

    # マスタDataFrameから予測用特徴変数DataFrameを生成するメソッド
    def create_predict_rrdf_X(self):
        prePredictRRDF_X = self.MasterDf

        # 特徴変数の対象となるカラム以外のカラムを削除
        drop_col = ['RaceKey', 'Umaban', 'Bamei','KettoNum','yResult']
        PredictRRDF_X = prePredictRRDF_X.drop(drop_col,axis=1)

        # TODO:特徴変数DataFrame前処理
        # PredictRRDF_X = dfedit.proc_X_df(Predict_X_Df)

        return PredictRRDF_X
