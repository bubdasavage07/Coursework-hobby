import random

playerHealth = 100

def rerollZombie():
    zombieType = random.randrange(1,10)
    return zombieType

def selectZombie(zombieType):
    #Zombie selection code
    if zombieType == 1:
       return "Spitter zombie", 35, 5
        #add DOT effect
        
    elif zombieType == 2:
        return "Jeremiah the zombie", 40, 15
        
    elif zombieType == 3:
        return "John Wick's dog", 6, 50
        
    else:
        return "No name zombie", 20, 10

#inventory
#enemy


print("Brain Raider")
print("************")

print("Would you like to play this game of death?")
gameStart = input("[Y] Yes  or  [N] No: ")

if gameStart == 'Y' or gameStart == 'y':
    playerName = input("Name your hero? ")

    print("There is a virus outbreak called Gen X")
    print("Gen X was caused by a nuclear explosion")
    print("This has caused the undead to rise from their graves")
    print("the undead have spread and are partying in every Walmart")
    print("this must be stopped!!")
    print("the only cure is in this military base")
    print(playerName, "must get through the base and find the cure")

    print("********** WEAPONS **********")
    print("[1] Pistol, [2] Pipe Wrench,")
    print("[3] Pepper Spray, [4] AR-15,")
    print("[5] Fnuke (OP weapon), [0] Fists,")
    primaryWeapon = int(input(playerName + " please select a weapon: "))

    #Weapon selection code
    if primaryWeapon == 1:
        weapon = "Pistol"
        weaponDMG = 5
    elif primaryWeapon == 2:
        weapon = "Pipe Wrench"
        weaponDMG = 10
    elif primaryWeapon == 3:
        weapon = "Pepper spray"
        weaponDMG = 3
        #add AOE effect
    elif primaryWeapon == 4:
        weapon = "AR-15"
        weaponDMG = 8
    elif primaryWeapon == 5:
        weapon = "FNUKE"
        weaponDMG = -99
    else:
        weapon = "fists"
        weaponDMG = 1

    

    print()
    print("********* Level 1 ************")
    print()
# FOR loop to fight 3 zombies
    for enemyCount in range (0,3): 
        zombieName, zombieHealth, zombieDMG = selectZombie(rerollZombie())

        print("Oh no! here comes a " + zombieName)

        while playerHealth > 0 and zombieHealth > 0:
            playerHealth = playerHealth - zombieDMG
            zombieHealth = zombieHealth - weaponDMG

            print(zombieName + " 's Health: ", zombieHealth)
            print(playerName + "'s Health: ", playerHealth)
            #add a delay feature for better game visual
else:
    print("Game Over")
    
    
#FUTURE IDEAS
    # add easy, medium, hard difficulty
    # randomize game difficulty based on player damage
