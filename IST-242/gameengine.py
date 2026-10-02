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
    print("\nA zombie lunges at you!")
    
    # 3. SELECTION STATEMENT (Inside function)
    choice = input("Do you [1] Attack with your bat or [2] Run away? ").strip()
    
    if choice == "1":
        damage_taken = random.randint(10, 30)
        p1.playerHealth -= damage_taken
        p1.zombieKillCount += 1
        print(f"You defeat the zombie but take {damage_taken} damage!")
    elif choice == "2":
        print("You safely escape, but the zombie is still out there.")
    else:
        print("You hesitate! The zombie bites you for 40 damage.")
        p1.playerHealth -= 40

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
window.geometry("700x500")



i = 0

# 4. LOOP(S) (Runs until player dies or kills 3 zombies)
while p1.playerHealth > 0 and p1.zombieKillCount < 3:
    
    print(f"\n[Health: {p1.playerHealth} | Zombies Defeated: {p1.zombieKillCount}/3]")
    action = input(f"You see a dark alley. Leading to {level[i]}. "
                   "Do you explore it? (yes/no): ").lower().strip()
    
    if action == "yes":
        fight_zombie()
        i+=1
    elif action == "no":
        print("You walk around the block safely.")
        i+=1
    else:
        print("Invalid choice. Time passes...")
#----End of Loop -----


# Check final status
if p1.playerHealth <= 0:
    print("\nYou succumbed to your injuries and turned into a zombie!")
else:
    print("\nVictory! You made it to the safe zone!")

if level[4]:
    print("Saving your game.")
    with open("output.txt", "w") as f:
        f.write("Hello world\n")
        f.write("This adds a new line")
        
button_frame = tk.Frame(window)
button_frame.pack(pady=20)

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