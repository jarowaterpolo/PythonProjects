import random
from tkinter import *
from tkinter import ttk

maxSecretNumber = 10
secret = random.randint(1,maxSecretNumber)
maxStage = 1
stage = 1

correctCounter = 0

root = Tk()
root.geometry("605x115")

style = ttk.Style()
style.configure("My.TFrame", background="lightblue")

frm = ttk.Frame(root, style="My.TFrame", padding=10)
frm.grid()
for row in range(10):
    frm.grid_rowconfigure(row, minsize=10)
for column in range(10):
    frm.grid_columnconfigure(column, minsize=10)


ttk.Label(frm, text="Hello and Welcome! \n" \
                    "Try guessing a number ").grid(column=0, row=0)

input_text = StringVar()

result_label = ttk.Label(frm, text="")
result_label.grid(column=2, row=0)

guess_label = ttk.Label(frm, text="min = 1, max = 10")
guess_label.grid(column=2, row=2)

score_label = ttk.Label(frm, text="0")
score_label.grid(column=11, row=0)

stage_label = ttk.Label(frm, text="1/1")
stage_label.grid(column=7, row=1)

score = 0

def submit(event=None):
    global score
    global secret
    global correctCounter
    global maxStage
    global maxSecretNumber

    try:
        guess = int(input_text.get())
    except ValueError:
        result_label.config(text="Enter a number")
        input_text.set("")
        return

    print("You guessed:", guess)

    if guess == secret:
        result_label.config(text="Correct!")
        score += 1
        score_label.config(text=score)
        maxSecretNumber = 10**stage
        secret = random.randint(1,maxSecretNumber)
        guess_label.config(text=f"min = 1, max = {maxSecretNumber}")
        correctCounter += 1
        if correctCounter >= 10:
            maxStage += 1
            correctCounter = 0
            stage_label.config(text=f"{stage}/{maxStage}")
    elif guess > secret:
        result_label.config(text=f"secret number is lower than {guess}")
    elif guess < secret:
        result_label.config(text=f"secret number is higher than {guess}")
    else:
        result_label.config(text="Try Again")

    input_text.set("")

entry1 = ttk.Entry(
    frm,
    textvariable=input_text,
    justify=CENTER
)
entry1.grid(row=2, column=0, ipadx=30, ipady=6)
entry1.focus_force()

# press Enter inside the entry
entry1.bind("<Return>", submit)

def StageUp(event=None):
    global maxStage
    global stage
    if stage + 1 <= maxStage:
        stage += 1
        stage_label.config(text=f"{stage}/{maxStage}")

def StageDown(event=None):
    global maxStage
    global stage
    if stage - 1 > 0:
        stage -= 1
        stage_label.config(text=f"{stage}/{maxStage}")

ttk.Button(frm, text="-Stage", command=StageDown).grid(column=6, row=1)
ttk.Button(frm, text="+Stage", command=StageUp).grid(column=8, row=1)
ttk.Button(frm, text="Quit", command=root.destroy).grid(column=11, row=2)

root.mainloop()