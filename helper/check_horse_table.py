import os, sys
sys.path.append(os.getcwd())

import HorseTable

# キタサンブラック：12102013
# レースキー：08173411
RaceKey = "2017102905040911"
KettoNum = "2012102013"

ht = HorseTable.Horse(KettoNum)
r = HorseTable.Race(RaceKey)

horse_info = ht.get_horse_info()
horse_race_info = ht.get_horse_race_info(RaceKey)
results = ht.get_race_results(RaceKey)

held_info = r.get_held_info()
race_info = r.get_race_info()


print("------------------------------ horse_info ------------------------------")
print(horse_info)
print("----------------------------------------------------------------------")

print("------------------------------ horse_race_info ------------------------------")
print(horse_race_info)
print("----------------------------------------------------------------------")

print("------------------------------ results ------------------------------")
print(results)
print("----------------------------------------------------------------------")

print("------------------------------ held_info ------------------------------")
print(held_info)
print("----------------------------------------------------------------------")

print("------------------------------ race_info ------------------------------")
print(race_info)
print("----------------------------------------------------------------------")
