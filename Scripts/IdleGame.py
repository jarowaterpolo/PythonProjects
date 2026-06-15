import Basic_Imports as bi
from ClassStorage import WaitTime
from ClassStorage import Player

class IdleGame:

    def __init__(self, root):
        self.root = root
        self.root.title("My first python Idle Game")
        self.root.geometry("400x600")

        self.label = bi.Label(root, text="Enter your name:")
        self.label.pack(pady=10)
        
        self.username_entry = bi.Entry(root)
        self.username_entry.pack(pady=5)
        
        self.start_button = bi.Button(root, text="Start Game", command=self.start_game)
        self.start_button.pack(pady=10)


    def start_game(self):
        name = self.username_entry.get()
        
        if name.strip() == "":
            name = "Player 1"
        self.p1 = Player(name, 0)
        print (f"{self.p1.name} now has {self.p1.score} score")

        self.label.pack_forget()
        self.username_entry.pack_forget()
        self.start_button.pack_forget()
        
        self.build_game_interface()

    def build_game_interface(self):
        self.root.bind("1", self.u1_action)
        self.root.bind("2", self.u2_action)
        
        self.score_gain = 1

        self.costU1 = 10
        self.costU2 = 100
        self.U2Mult = 1

        self.u1Bought = 0

        self.label_score = bi.Label(
            self.root, text="Score: 0", font=("Arial", 24, "bold")
        )
        self.label_score.pack(pady=20)

        self.label_score_gain = bi.Label(
            self.root, text="+1 Score /s", font=("Arial", 24, "bold")
        )
        self.label_score_gain.pack(pady=20)

        self.score_button = bi.Button(
            self.root,
            text="CLick for Score!",
            font=("Arial", 14),
            command=self.score_action,
            bg="#4CAF50",
            fg="white",
        )
        self.score_button.pack(pady=10)

        self.u1_button = bi.Button(
            self.root,
            text=f"Buy Upgrade (+{self.U2Mult}/s) [Cost: {self.costU1}]",
            font=("Arial", 14),
            command=self.u1_action,
            bg="#4CAF50",
            fg="white",
        )
        self.u1_button.pack(pady=10)

        self.u2_button = bi.Button(
            self.root,
            text=f"Buy Upgrade (x2/s) [Cost: {self.costU2}]",
            font=("Arial", 14),
            command=self.u2_action,
            bg="#4CAF50",
            fg="white",
        )
        self.u2_button.pack(pady=10)

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

    def u1_action(self, event=None):
        if (self.p1.score >= self.costU1):
            self.u1Bought += 1

        new_gains = self.p1.Upgrade1(self.score_gain, self.costU1, self.U2Mult)

        if new_gains > self.score_gain:
            self.score_gain = new_gains

        self.label_score.config(text=f"Score: {self.p1.score}")
        self.label_score_gain.config(text=f"+{self.score_gain} Score /s")

        if (self.u1Bought >= 10):
            self.costU1 *= 2
            self.u1_button.config(text=f"Buy Upgrade (+{self.U2Mult}/s) [Cost: {self.costU1}]")
            self.u1Bought = 0


    def u2_action(self, event=None):
        (new_gains, self.U2Mult, self.costU2) = self.p1.Upgrade2(self.score_gain, self.costU2, self.U2Mult)

        if new_gains > self.score_gain:
            self.score_gain = new_gains

        self.label_score.config(text=f"Score: {self.p1.score}")
        self.label_score_gain.config(text=f"+{self.score_gain} Score /s")
        self.u1_button.config(text=f"Buy Upgrade (+{self.U2Mult}/s) [Cost: {self.costU1}]")
        self.u2_button.config(text=f"Buy Upgrade (x2/s) [Cost: {self.costU2}]")

def Main():
    window = bi.Tk()
    game = IdleGame(window)
    window.mainloop()


if __name__ == "__main__":
    Main()