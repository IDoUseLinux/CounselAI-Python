class sports :
    def __init__(self, name, position, totalMonths) :
        self.name = name
        self.position = position
        self.totalMonths = totalMonths
        self.sportsValue = position * (totalMonths**(2/5)) ## This leads to the gradual decline of extra months of sports, from 8 months compared to 4 months is large, but 20 to 24 is smaller