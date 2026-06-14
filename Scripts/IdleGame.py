import Basic_Imports as bi
from ClassStorage import WaitTime
from ClassStorage import Player

class IdleGame:

    def __init__(self, root):
        self.root = root
        self.root.title("My first python Idle Game")
        self.root.geometry("400x300")

        name = input("input your name ")
        self.p1 = Player(name, 0)
        print (f"{self.p1.name} now has {self.p1.score} score")
        self.score_gain = 1

        self.label_score = bi.Label(
            root, text="Score: 0", font=("Arial", 24, "bold")
        )
        self.label_score.pack(pady=20)

        self.label_score_gain = bi.Label(
            root, text="+1 Score /s", font=("Arial", 24, "bold")
        )
        self.label_score_gain.pack(pady=20)

        self.score_button = bi.Button(
            root,
            text="CLick for Score!",
            font=("Arial", 14),
            command=self.score_action,
            bg="#4CAF50",
            fg="white",
        )
        self.score_button.pack(pady=10)

        self.u1_button = bi.Button(
            root,
            text="Buy Upgrade (+1/s) [Cost: 10]",
            font=("Arial", 14),
            command=self.u1_action,
            bg="#4CAF50",
            fg="white",
        )
        self.u1_button.pack(pady=10)

        self.background_thread = bi.threading.Thread(
            target=self.score_loop, daemon=True
        )
        self.background_thread.start()

    def score_loop(self):
        while True:
            self.p1.ScoreUp(self.score_gain)
            self.label_score.config(text=f"Score: {self.p1.score}")
            print(f"\r{self.p1.name}'s score: {self.p1.score} ( earning +{self.score_gain}/s ) | Type 'b' to buy upgrade: ", end="", flush=True)
            WaitTime.Wait(1)

    def score_action(self):
        self.p1.ScoreUp(self.score_gain)
        self.label_score.config(text=f"Score: {self.p1.score}")

    def u1_action(self):
        new_gains = self.p1.Upgrade(self.score_gain)

        if new_gains > self.score_gain:
            self.score_gain = new_gains

        self.label_score.config(text=f"Score: {self.p1.score}")
        self.label_score_gain.config(text=f"+{self.score_gain} Score /s")

def Main():
    window = bi.Tk()
    game = IdleGame(window)
    window.mainloop()


if __name__ == "__main__":
    Main()