import random
from tkinter import *
from tkinter import ttk

secret = random.randint(1,10)

root = Tk()
root.geometry("400x100")

style = ttk.Style()
style.configure("My.TFrame", background="lightblue")

frm = ttk.Frame(root, style="My.TFrame", padding=10)
frm.grid()
frm.grid_rowconfigure(1, minsize=10)

ttk.Label(frm, text="Hello and Welcome! \n" \
                    "Try guessing a number ").grid(column=0, row=0)

input_text = StringVar()

result_label = ttk.Label(frm, text="")
result_label.grid(column=2, row=0)

score_label = ttk.Label(frm, text="0")
score_label.grid(column=4, row=0)

score = 0

def submit(event=None):
    global score
    global secret

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
        secret = random.randint(1,10)
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

ttk.Button(frm, text="Quit", command=root.destroy).grid(column=4, row=2)

root.mainloop()