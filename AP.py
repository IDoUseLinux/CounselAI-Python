## AP Weight is a item used to determin the strength of the AP class, from 1 to 5
## AP Calculus, Chemistry, and Physics (Including all variants) are considered to be a 5
## AP Precalcus, etc, are considered to be a 4
## AP CSA, AP CSP, all language, US History, Literature and English, is considered to be a 3
## AP Art and other relatively bad APs are consdiered to be a 1
class apClass :
    APweight = 2

    def __init__(self, score) :
        self.score = score
        self.apValue = score*self.APweight/10

class APCSA(apClass) :
    APweight = 3

class APCalc(apClass) :
    APweight = 5

## AP Foreign Language is a "catch-all" phrase for AP Chinese, AP Japanese, AP Spanish, AP French, AP Latin, etc.
class APForeignLanguage(apClass) :
    APWeight = 3