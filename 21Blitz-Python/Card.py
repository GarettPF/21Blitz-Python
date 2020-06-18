class Card:
    """Card class for the game"""

    def __init__(self):
        self.suite = None
        self.value = None

    def __init__(self, s, v):
        self.suite = s
        self.value = v

    def __str__(self):
        string = ""
        if self.value == 10:
            string += 'T'
        elif self.value == 11:
            string += 'J'
        elif self.value == 12:
            string += 'Q'
        elif self.value == 13:
            string += 'K'
        else:
            string += str(self.value)
        string += self.suite
        return string    

    def isWild(self):
        isBlack = (self.suite == 's' or self.suite == 'c')
        isJack = (self.value == 11)
        return isBlack and isJack
