import Basic_Imports as bi
from ClassStorage import WaitTime
from ClassStorage import Player

name = input("input your name ")
p1 = Player(name, 0)
print (f"{p1.name} now has {p1.score} score")

score_gain = 1

# 1. This function runs continuously in the background
def score_loop():
    while True:
        p1.ScoreUp(score_gain)
        print(f"\r{p1.name}'s score: {p1.score} ( earning +{score_gain}/s ) | Type 'b' to buy upgrade: ", end="", flush=True)
        WaitTime.Wait(1)

background_thread = bi.threading.Thread(target=score_loop, daemon=True)
background_thread.start()

while True:
    # choice = input("Druk op Enter voor volgende seconde, of typ 'b' om upgrade te kopen (kost 10): ").lower()
    choice = input().lower()
    
    if choice == 'b':
        score_gain = p1.Upgrade(score_gain)

