import random

# 1. VARIABLES (Global state)
player_health = 100
zombies_killed = 0
level = ["the hospital", "the store", "the armory", "a church", "the bunker"]

# 2. FUNCTIONS (Function 1: Handles combat choices)
def fight_zombie():
    global player_health, zombies_killed
    print("\nA zombie lunges at you!")
    
    # 3. SELECTION STATEMENT (Inside function)
    choice = input("Do you [1] Attack with your bat or [2] Run away? ").strip()
    
    if choice == "1":
        damage_taken = random.randint(10, 30)
        player_health -= damage_taken
        zombies_killed += 1
        print(f"You defeat the zombie but take {damage_taken} damage!")
    elif choice == "2":
        print("You safely escape, but the zombie is still out there.")
    else:
        print("You hesitate! The zombie bites you for 40 damage.")
        player_health -= 40

# 2. FUNCTIONS (Function 2: Displays game ending)
def end_game():
    print("\n--- GAME OVER ---")
    print(f"Zombies defeated: {zombies_killed}")
    print("Thanks for playing!")

def weapon_choice():
    choice = 0
    
    match choice:
        case 0:
            print("fists")
        case 1:
            print("lead pipe")
        case 2:
            print("bat")
        case 3:
            print("pistol")            
        case 4:
            print("fnuke")            
        case _:
            print("No weapon found")

# MAIN GAME LOOP
print("Welcome to Zombie Survival!")

i = 0

# 4. LOOP(S) (Runs until player dies or kills 3 zombies)
while player_health > 0 and zombies_killed < 3:
    
    print(f"\n[Health: {player_health} | Zombies Defeated: {zombies_killed}/3]")
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
if player_health <= 0:
    print("\nYou succumbed to your injuries and turned into a zombie!")
else:
    print("\nVictory! You made it to the safe zone!")

if level[4]:
    print("Saving your game.")
    with open("output.txt", "w") as f:
        f.write("Hello world\n")
        f.write("This adds a new line")


end_game()