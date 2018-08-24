######################################
# 特徴量作成の為のデータ整形メソッド
######################################

import datetime

# results馬柱を引数に、過去5走の勝率を計算する
def calc_Last5WinRaito(results):
    raito = 0
    if len(results) >= 4:
        result5 = results[1:5]
        raito = len(result5['KakuteiJyuni'].isin(["1"])) / 5
    elif len(results) >= 1:
        raito = len(results['KakuteiJyuni'].isin(["1"])) / len(results)
    else:
        raito = 0

    return raito

# results馬柱を引数に、過去5走の連対率を計算する
def calc_Last5Win3Raito(results):
    raito = 0
    if len(results) >= 4:
        result5 = results[1:5]
        raito = len(result5['KakuteiJyuni'].isin(["1","2","3"])) / 5
    elif len(results) >= 1:
        raito = len(results['KakuteiJyuni'].isin(["1","2","3"])) / len(results)
    else:
        raito = 0

    return raito

# race_info,results馬柱を引数に、ローテーション（前走から何日経過したか）を計算する
def calc_Rotation(race_info,results):
    # 出走当日の日付を取得
    CurrentRaceYYYYMMDD = str(race_info['Year'][0]) + str(race_info['MonthDay'][0])

    # 過去出走経験がない場合は、ローテーション日数を0として返す
    if len(results) > 0:
        # 馬過去戦績情報より前走の日付を取得しローテーションを計算
        LastRaceYYYYMMDD    = str(results.sort_values(by=['Year','MonthDay'],ascending=[False,False])['Year'][0]) + str(results.sort_values(by=['Year','MonthDay'],ascending=[False,False])['MonthDay'][0])
        rotation = (datetime.datetime.strptime(CurrentRaceYYYYMMDD, '%Y%m%d') - datetime.datetime.strptime(LastRaceYYYYMMDD, '%Y%m%d')).days
    else:
        rotation = 0

    return rotation
