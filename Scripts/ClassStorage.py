import Basic_Imports as bi

class WaitTime:
    def Wait(sec):
        bi.time.sleep(sec)

class Player:
    def __init__(self, name, score):
        self.name = name  # Attribute for the players name
        self.score = score

    def ScoreUp(self, amount):
        self.score += amount

    def ScoreDown(self, amount):
        self.score -= amount

    def Upgrade(self, gains):
        if (self.score > 10):
            self.ScoreDown(10)
            print(f"\r{self.name} lost {10} score and gained 1 upgrade", end="", flush=True)
            num = gains + 1
            return num
        else:
            print ("not enough score")
            return gains