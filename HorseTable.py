######################################
# 馬柱作成クラス
######################################

import pandas as pd
import sqlalchemy as sa
import ProcHtEdit as htedit

class HorseTable():
    ## データベース（SQLite）への接続情報
    url = '***'
    engine = sa.create_engine(url)

    def __init__(self,count):
        self.count = count

#------------------------#
#--  レースクラス
#------------------------#

class Race(HorseTable):
    def __init__(self,RaceKey):
        self.RaceKey = RaceKey

    #### 開催属性 ####
    # RaceKeyを指定して、そのレースが開催される日の情報を、DataFrame（1×？）で返す
    def get_held_info(self):
        # RaceKeyを指定して、そのレースが行われる開催情報を、DataFrame（1×？）で返す。
        getQuery = """
        SELECT
            DataKubun,
            Year,
            MonthDay,
            JyoCD,
            Kaiji,
            RaceNum,
            YoubiCD,
            TenkoCD
        FROM N_RACE
        WHERE
            Year     = '{0}' AND
            MonthDay = '{1}' AND
            JyoCD    = '{2}' AND
            Kaiji    = '{3}' AND
            Nichiji  = '{4}' AND
            RaceNum  = '{5}'
        """.format(self.RaceKey[0:4],self.RaceKey[4:8],self.RaceKey[8:10],self.RaceKey[10:12],self.RaceKey[12:14],self.RaceKey[14:16])

        ### クエリを発行しDf形式で取得
        preData = pd.read_sql_query(getQuery,Race.engine)



        return preData


    #### 番組情報 ####
    # RaceKeyを指定して、そのレースの情報を、DataFrame（1×？）で返す
    def get_race_info(self):

        getQuery = """
        SELECT
            DataKubun,
            Year,
            MonthDay,
            JyoCD,
            Kaiji,
            RaceNum,
            GradeCD,
            KigoCD,
            Kyori,
            TrackCD,
            SibaBabaCD,
            DirtBabaCD
        FROM N_RACE
        WHERE
            Year     = '{0}' AND
            MonthDay = '{1}' AND
            JyoCD    = '{2}' AND
            Kaiji    = '{3}' AND
            Nichiji  = '{4}' AND
            RaceNum  = '{5}'
        """.format(self.RaceKey[0:4],self.RaceKey[4:8],self.RaceKey[8:10],self.RaceKey[10:12],self.RaceKey[12:14],self.RaceKey[14:16])

        ### クエリを発行しDf形式で取得
        preData = pd.read_sql_query(getQuery,Race.engine)

        ### データ整形
        # 芝・ダート種別追加
        preData['TrackKind']    =   htedit.toTrackKind(preData['TrackCD'][0])
        # 馬場状態追加
        preData['BabaStatus']   =   htedit.toBabaStatus(preData['TrackCD'][0],preData['SibaBabaCD'][0],preData['DirtBabaCD'][0])

        return preData

#------------------------
#--  馬クラス
#------------------------
class Horse(HorseTable):

    def __init__(self,KettoNum):
        self.KettoNum = KettoNum

    #### 馬属性 ####
    # KettoNumを指定して、馬固有の情報を、DataFrame（1×？）で返す
    def get_horse_info(self):
        ### 血統登録番号(KettoNum)を用いて競走馬マスタ（N_UMA）より馬属性情報を取得
        getQuery = """
        SELECT
            KettoNum,
            DelKubun,
            BirthDate,
            Bamei,
            HinsyuCD,
        	KeiroCD,
            ChokyosiCode,
            BreederCode,
            BanusiCode,
            Kyakusitu1,
            Kyakusitu2,
            Kyakusitu3,
            Kyakusitu4,
            RaceCount
        FROM N_UMA
        WHERE
            KettoNum = '{0}'
        """.format(self.KettoNum)

        ### クエリを発行しDf形式で取得
        preData = pd.read_sql_query(getQuery,Horse.engine)

        return preData
    ##### 馬毎レース情報 #####
    # RaceKeyとKettoNumを指定して、対象のレースの馬毎レース情報をDataFrane(1×?)形式で返す
    def get_horse_race_info(self,RaceKey):
        ### レースキー（RaceKey）・血統登録番号(KettoNum)を用いて馬毎レース情報（N_UMA_RACE）より馬毎のレース情報を取得
        getQuery = """
        SELECT
            DataKubun,
            Year,
            MonthDay,
            JyoCD,
            Kaiji,
            RaceNum,
            Wakuban,
            Umaban,
            KettoNum,
            Bamei,
            UmaKigoCD,
        	Barei,
            SexCD,
            TozaiCD,
            Futan,
            Blinker,
            KisyuCode,
        	KisyuRyakusyo,
            BaTaijyu
        FROM N_UMA_RACE
        WHERE
            Year     = '{0}' AND
            MonthDay = '{1}' AND
            JyoCD    = '{2}' AND
            Kaiji    = '{3}' AND
            Nichiji  = '{4}' AND
            RaceNum  = '{5}' AND
            KettoNum = '{6}'
        """.format(RaceKey[0:4],RaceKey[4:8],RaceKey[8:10],RaceKey[10:12],RaceKey[12:14],RaceKey[14:16],self.KettoNum)

        ### クエリを発行しDf形式で取得
        preData = pd.read_sql_query(getQuery,Horse.engine)

        return preData

    ##### 馬成績 #####
    # RaceKeyとKettoNumを指定して、対象のレースより前（データ作成年月日が古いレース）の結果をDataFrame形式で返す
    def get_race_results(self,RaceKey):

        ###
        getQuery = """
        SELECT
            DataKubun,
            Year,
            MonthDay,
            JyoCD,
            Kaiji,
            RaceNum,
            Umaban,
            KettoNum,
        	KisyuRyakusyo,
        	KakuteiJyuni
        FROM N_UMA_RACE
        WHERE
            Year || MonthDay  < '{0}' AND
            KettoNum          = '{1}'
        """.format(RaceKey[0:8],self.KettoNum)

        ### クエリを発行しDf形式で取得
        preData = pd.read_sql_query(getQuery,Horse.engine)

        return preData
