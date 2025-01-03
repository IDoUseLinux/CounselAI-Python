import json, sys, os
## This makes the scripts behave with the code...
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import universities

T1_UNIS = []
T2_UNIS = []
T3_UNIS = []
T4_UNIS = []
T5_UNIS = []
uni_score_list = ""

with open("tier1.json", 'r') as t1 :
    tier1s = json.load(t1)
    
    for i in tier1s :
        ## Ugly but works
        T1_UNIS.append(universities.university(i, tier1s[i]["acc_rate"], 5, tier1s[i]["75_sat"], tier1s[i]["50_sat"], tier1s[i]["25_sat"], tier1s[i]["tags"]))
        uni_score_list += (i + " : " + str(T1_UNIS[len(T1_UNIS)-1].universityDifficulty)) + "\n"

with open("tier2.json", 'r') as t2 :
    tier2s = json.load(t2)

    for i in tier2s :
        T2_UNIS.append(universities.university(i, tier2s[i]["acc_rate"], 4, tier2s[i]["75_sat"], tier2s[i]["50_sat"], tier2s[i]["25_sat"], tier2s[i]["tags"]))
        uni_score_list += (i + " : " +  str(T2_UNIS[len(T2_UNIS)-1].universityDifficulty)) + "\n"


with open("tier3.json", 'r') as t3 :
    tier3s = json.load(t3)

    for i in tier3s :
        T3_UNIS.append(universities.university(i, tier3s[i]["acc_rate"], 3, tier3s[i]["75_sat"], tier3s[i]["50_sat"], tier3s[i]["25_sat"], tier3s[i]["tags"]))
        uni_score_list += (i + " : " + str(T3_UNIS[len(T3_UNIS)-1].universityDifficulty)) + "\n"

with open("tier4.json", 'r') as t4 :
    tier4s = json.load(t4)

    for i in tier4s :
        T4_UNIS.append(universities.university(i, tier4s[i]["acc_rate"], 2, tier4s[i]["75_sat"], tier4s[i]["50_sat"], tier4s[i]["25_sat"], tier4s[i]["tags"]))
        uni_score_list += (i + " : " + str(T4_UNIS[len(T4_UNIS)-1].universityDifficulty)) + "\n"

with open("tier5.json", 'r') as t5 :
    tier5s = json.load(t5)

    for i in tier5s :
        T5_UNIS.append(universities.university(i, tier5s[i]["acc_rate"], 1, tier5s[i]["75_sat"], tier5s[i]["50_sat"], tier5s[i]["25_sat"], tier5s[i]["tags"]))
        uni_score_list += (i + " : " + str(T5_UNIS[len(T5_UNIS)-1].universityDifficulty)) + "\n"


## Also a bit janky but also works
ALL_UNIS = T1_UNIS + T2_UNIS + T3_UNIS + T4_UNIS + T5_UNIS

with open("Debug file1.txt", "w") as out_file :
    out_file.write(str(ALL_UNIS))

with open("Debug file2.txt", "w") as out_file :
    out_file.write(str(uni_score_list))