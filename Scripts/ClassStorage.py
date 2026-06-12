# models.py
class GameScore:
    def __init__(self):
        self.score = 0
        self.stage = 1

    def increase_score(self):
        self.score += 1

    def display(self):
        return f"Stage: {self.stage} | Score: {self.score}"