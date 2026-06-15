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

    def Upgrade1(self, gains, cost, upgradeMult):
        if (self.score >= cost):
            self.ScoreDown(cost)
            print(f"\r{self.name} lost {cost} score and gained 1 upgrade1", end="", flush=True)
            num = gains + 1 * upgradeMult
            return num
        else:
            print (f"\rnot enough score", end="", flush=True)
            return gains
        
    def Upgrade2(self, gains, cost, upgradeMult):
        if (self.score >= cost):
            self.ScoreDown(cost)
            print(f"\r{self.name} lost {cost} score and gained 1 upgrade2", end="", flush=True)
            num = gains * 2
            upgradeMult *= 2
            cost *= 10
            return (num, upgradeMult, cost)
        else:
            print (f"\rnot enough score", end="", flush=True)
            return (gains, upgradeMult, cost)