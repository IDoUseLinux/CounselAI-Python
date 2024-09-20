class awards :
    def __init__(self, awardname, awardlevel, awardplace):
        self.awardname = awardname
        self.awardlevel = awardlevel
        self.awardplace = awardplace
        self.awardvalue = awardlevel*awardplace/2