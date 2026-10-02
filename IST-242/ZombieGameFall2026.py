import random
import tkinter as tk
import weapon
import player

#Step 0: Create an instance of the Weapon class
w1 = weapon.Weapon("fists", 5)

#Create an instance of the Player class
p1 = player.Player()

# 1. VARIABLES (Global state)
#playerHealth = 100
#zombieKillCount = 0
level = ["the hospital", "the store", "the armory", "a church", "the bunker"]
#new suggestions: Level 1: your house, neighbor's house, the store, the streets leading to town
#Level 2: streets of level 2, the church, the graveyard, small patch of woods
#Level 3: the hospital (first floor), the ER, the stairs, floor 13

# 2. FUNCTIONS (Function 1: Handles combat choices)
def fight_zombie():
    p1.playerHealth, p1.zombieKillCount

# 2. FUNCTIONS (Function 2: Displays game ending)
def end_game():
    print("\n--- GAME OVER ---")
    print(f"Zombies defeated: {p1.zombieKillCount}")
    print("Thanks for playing!")

# MAIN GAME LOOP
#print("Welcome to Zombie Survival!")
# Create window
window = tk.Tk()
window.title("Zombie Survial")
window.geometry("800x600")



i = 0

# 4. LOOP(S) (Runs until player dies or kills 3 zombies)
#while p1.playerHealth > 0 and p1.zombieKillCount < 3:
    
#    print(f"\n[Health: {p1.playerHealth} | Zombies Defeated: {p1.zombieKillCount}/3]")
#----End of Loop -----


# Check final status
if p1.playerHealth <= 0:
    print("\nYou succumbed to your injuries and turned into a zombie!")
else:
    print("\nVictory! You made it to the safe zone!")

if level[4]:
    print("Saving your game.")
    #with open("output.txt", "w") as f:
        #f.write("Hello world\n")
        #f.write("This adds a new line")

button_frame = tk.Frame(window, bg="black", width=500, height=300)
#button_frame.pack(side="bottom", pady=20)
button_frame.pack(expand=True)

button_frame = tk.Frame(window)
button_frame.pack(side="bottom", pady=20)

click_button = tk.Button(button_frame, text="fists", command=lambda: w1.weapon_choice(0), font=("Chiller", 16), padx=10, pady=5)
click_button.pack(side="left", padx=5)

click_button = tk.Button(button_frame, text="rusty knife", command=lambda: w1.weapon_choice(1), font=("Chiller", 16), padx=10, pady=5)
click_button.pack(side="left", padx=5)

click_button = tk.Button(button_frame, text="lead pipe", command=lambda: w1.weapon_choice(2), font=("Chiller", 16), padx=10, pady=5)
click_button.pack(side="left", padx=5)

click_button = tk.Button(button_frame, text="bat", command=lambda: w1.weapon_choice(3), font=("Chiller", 16), padx=10, pady=5)
click_button.pack(side="left", padx=5)

click_button = tk.Button(button_frame, text="pistol", command=lambda: w1.weapon_choice(4), font=("Chiller", 16), padx=10, pady=5)
click_button.pack(side="left", padx=5)

click_button = tk.Button(button_frame, text="fnuke", command=lambda: w1.weapon_choice(5), font=("Chiller", 16), padx=10, pady=5)
click_button.pack(side="left", padx=5)

window.mainloop()
end_game()
