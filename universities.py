class university :

    def __init__(self, name, acc_rate, tier, sat75, sat50, sat25, tags) :
        self.name = name
        self.acc_rate = acc_rate
        self.tier = tier ## Tiers are reversed in this, a tier 1 is a tier 5 which gives the most score
        self.sat75 = sat75
        self.sat50 = sat50
        self.sat25 = sat25
        self.tags = tags

        self.universityDifficulty = (1-self.acc_rate)*7*tier + sat75/40
        if (self.tier <= 3 ) :
            self.universityDifficulty -= (5*(2-self.tier))
        else :
            self.universityDifficulty += (2*self.tier)
            