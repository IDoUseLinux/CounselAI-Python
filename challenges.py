## TEMP Not used due to the complixity of implementing the grading
class challenges :
    def __init__(self, name, region, purpose, outcome) :
        self.name = name
        self.region = region
        self.purpose = purpose
        self.outcome = outcome
        self.challengeValue = region*outcome*purpose/2