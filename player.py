class Player():
    def __init__(self, name, score=0):
        self.name = name
        self.score = score

    def getScore(self):
        return self.score

    def getName(self):
        return self.name
