class clubs :
    def __init__(self, name, purpose, role) :
        self.name = name
        self.purpose = purpose
        self.role = role
        self.clubValue = purpose*role/3
