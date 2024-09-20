## AP Weight is a item used to determin the strength of the AP class, from 1 to 5
## AP Calculus, Chemistry, and Physics (Including all variants) are considered to be a 5
## AP Precalcus, etc, are considered to be a 4
## AP CSA, AP CSP, all language, US History, Literature and English, is considered to be a 3
## AP Art and other relatively bad APs are consdiered to be a 1
class apClass :
    def __init__(self, name, tier, apgrade, score) :
        self.name = name
        self.tier = tier
        self.apgrade = apgrade
        self.score = score
        self.apValue = (score+apgrade)*tier/20