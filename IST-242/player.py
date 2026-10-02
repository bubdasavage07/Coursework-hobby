import tkinter as UI
from tkinter import messagebox

def prompt_for_name():
#Opens a small tkinter window to get the player's name.
    name = None

    def submit():
        nonlocal name
        entered = entry.get().strip()
        if not entered:
            messagebox.showwarning("Warning", "Name cannot be empty!")
            return
        name = entered
        root.destroy()

    root = UI.Tk()
    root.title("Player Setup")
    root.geometry("250x130")
    root.resizable(False, False)

    UI.Label(root, text="Enter Your Name:", font=("Arial", 11)).pack(pady=10)

    entry = UI.Entry(root, font=("Arial", 11), width=18)
    entry.pack(pady=5)
    entry.focus()
    entry.bind("<Return>", lambda event: submit())

    UI.Button(root, text="Start Game", command=submit, width=10).pack(pady=10)

    root.mainloop()
    return name if name else "Anonymous"


# Player class/object
class Player:

    def __init__(self):
        self.playerHealth = 100
        self.playerName = prompt_for_name()
        self.lives = 3
        self.playerXP = 1
        self.zombieKillCount = 0
        self.playerGold = 25


# Instantiate the player
#p1 = Player()
#print(f"Welcome, {p1.playerName}!")
#print(f"Health: {p1.playerHealth}")

