import random
from tkinter import *
from tkinter import ttk

maxSecretNumber = 10
secret = random.randint(1,maxSecretNumber)
maxStage = 1
stage = 1

correctCounter = 0

root = Tk()

root.attributes("-fullscreen", True)

# Bind the 'Escape' key to easily exit fullscreen mode if needed
root.bind("<Escape>", lambda event: root.attributes("-fullscreen", False))
root.geometry("1920x1080")

style = ttk.Style()
style.configure("My.TFrame", background="lightblue")

# 2. Make the main root window rows and columns stretchable
root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure(0, weight=1)

# 'sticky="nsew"' stretches the frame to fill up the entire window space
frm = ttk.Frame(root, style="My.TFrame", padding=20)
frm.grid(row=0, column=0, sticky="nsew")

for row in range(12):
    frm.grid_rowconfigure(row, weight=1)
for column in range(13):
    frm.grid_columnconfigure(column, weight=1)

def resize_fonts(event):
    # Dynamically pick a base size according to your current resolution height
    base_size = max(14, int(event.height / 45))
    
    # Configure custom styles for different text components
    style.configure("Title.TLabel", font=("Arial", int(base_size * 1.3), "bold"), background="lightblue")
    style.configure("Main.TLabel", font=("Arial", base_size), background="lightblue")
    style.configure("Entry.TEntry", font=("Arial", base_size))
    style.configure("Action.TButton", font=("Arial", int(base_size * 0.8), "bold"))

# Bind the font update logic to the frame resize window trigger event
frm.bind("<Configure>", resize_fonts)


ttk.Label(frm, text="Hello and Welcome! \n" \
                    "Try guessing a number ", style="Title.TLabel", justify=CENTER).grid(column=0, row=0, columnspan=3, sticky="nsew")

input_text = StringVar()

result_label = ttk.Label(frm, text="", style="Main.TLabel", justify=CENTER)
result_label.grid(column=2, row=2, columnspan=4, sticky="nsew")

guess_label = ttk.Label(frm, text="min = 1, max = 10", style="Main.TLabel", justify=CENTER)
guess_label.grid(column=0, row=4, columnspan=2, sticky="nsew")

score_label = ttk.Label(frm, text="0", style="Title.TLabel")
score_label.grid(column=11, row=0)

stage_label = ttk.Label(frm, text="1/1", style="Title.TLabel")
stage_label.grid(column=6, row=7)

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
        score += 1 * stage**stage
        score_label.config(text=score)
        maxSecretNumber = 10**stage
        secret = random.randint(1,maxSecretNumber)
        correctCounter += 1 * stage**stage
        if correctCounter >= 10:
            maxStage += 1
            correctCounter = 0
            stage_label.config(text=f"{stage}/{maxStage}")
    elif guess == -1:
        maxStage += 10
        stage_label.config(text=f"{stage}/{maxStage}")
    elif guess > secret:
        result_label.config(text=f"secret number is lower than {guess}")
    elif guess < secret:
        result_label.config(text=f"secret number is higher than {guess}")
    else:
        result_label.config(text="Try Again")

    input_text.set("")
    guess_label.config(text=f"min = 1, max = {maxSecretNumber}")

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

btn_dwn = ttk.Button(frm, text="-Stage", command=StageDown, style="Action.TButton")
btn_dwn.grid(column=5, row=8, columnspan=2, sticky="nsew", padx=5, pady=5)

btn_up = ttk.Button(frm, text="+Stage", command=StageUp, style="Action.TButton")
btn_up.grid(column=7, row=8, columnspan=2, sticky="nsew", padx=5, pady=5)

btn_quit = ttk.Button(frm, text="Quit", command=root.destroy, style="Action.TButton")
btn_quit.grid(column=11, row=8, columnspan=2, sticky="nsew", padx=5, pady=5)

root.mainloop()