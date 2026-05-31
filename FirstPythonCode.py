import random
from tkinter import *
from tkinter import ttk

secret = random.randint(1,10)

root = Tk()
root.geometry("300x100")

frm = ttk.Frame(root, padding=10)
frm.grid()

ttk.Label(frm, text="Hello and Welcome!").grid(column=0, row=0)

input_text = StringVar()

result_label = ttk.Label(frm, text="")
result_label.grid(column=1, row=0)

def submit(event=None):
    try:
        guess = int(input_text.get())
    except ValueError:
        result_label.config(text="Enter a number")
        input_text.set("")
        return

    print("You guessed:", guess)

    if guess == secret:
        result_label.config(text="Correct!")
    else:
        result_label.config(text="Try Again")

    input_text.set("")

entry1 = ttk.Entry(
    frm,
    textvariable=input_text,
    justify=CENTER
)
entry1.grid(row=1, column=0, ipadx=30, ipady=6)
entry1.focus_force()

# press Enter inside the entry
entry1.bind("<Return>", submit)

ttk.Button(frm, text="Quit", command=root.destroy).grid(column=1, row=1)

root.mainloop()