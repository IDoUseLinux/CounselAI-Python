import json, time

with open("tier1.json", 'r') as t1 :
    tier1s = json.load(t1)
with open("tier2.json", 'r') as t2 :
    tier2s = json.load(t2)
with open("tier3.json", 'r') as t3 :
    tier3s = json.load(t3)
with open("tier4.json", 'r') as t4 :
    tier4s = json.load(t4)
with open("tier5.json", 'r') as t5 :
    tier5s = json.load(t5)

all_universities = {
    "Date Generated" : time.strftime("%Y-%m-%d %H:%M:%S %Z",time.localtime())
}

all_universities.update(tier1s)
all_universities.update(tier2s)
all_universities.update(tier3s)
all_universities.update(tier4s)
all_universities.update(tier5s)

print(all_universities)

with open("all tiers.json", 'w') as ta :
    json.dump(all_universities, ta, indent=4)