######################################
# 馬柱作成の為のデータ整形メソッド
######################################

# TrackCDをTrackKindに変換する
# 0：未設定　1：芝　2：ダート
def toTrackKind(TrackCD):
    TrackCD = int(TrackCD)
    TrackKind = 0

    if 10 <= TrackCD <= 22:
        TrackKind = 1
    elif 23 <= TrackCD <= 26:
        TrackKind = 2
    else:
        TrackKind = 0

    TrackKind = str(TrackKind)

    return TrackKind

# トラックコードから芝orダートを判別し馬場状態区分を返す
# 0: 未設定　1:良　2:稍重　3:重　4:不良
def toBabaStatus(TrackCD,SibaBabaCD,DirtBabaCD):
    TrackCD = int(TrackCD)
    BabaStatus = 0
    if 10 <= TrackCD <= 22:
        BabaStatus = SibaBabaCD
    elif 23 <= TrackCD <= 26:
        BabaStatus = DirtBabaCD
    else:
        BabaStatus = 0

    BabaStatus = str(BabaStatus)

    return BabaStatus
