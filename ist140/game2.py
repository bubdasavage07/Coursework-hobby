import random

playerHealth = 100

print("Brain Raider")
print("************")

print("Would you like to play this game of death?")
gameStart = input("[Y] Yes  or  [N] No: ").strip().lower()

if gameStart == "y":
    playerName = input("Name your hero? ").strip()

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

    # Weapon selection code
    if primaryWeapon == 1:
        weapon = "pistol"
        weaponDMG = 5
    elif primaryWeapon == 2:
        weapon = "pipe wrench"
        weaponDMG = 10
    elif primaryWeapon == 3:
        weapon = "pepper spray"
        weaponDMG = 3
    elif primaryWeapon == 4:
        weapon = "AR-15"
        weaponDMG = 8
    elif primaryWeapon == 5:
        weapon = "Fnuke"
        weaponDMG = -99  
    else:
        weapon = "fists"
        weaponDMG = 1

    print()
    print("********* Level 1 ************")
    print()

    enemyCount = 3

    # Stores the last zombie type so the same zombie does not fight twice in a row (codex)
    lastZombieType = None

    # 4. LOOP (Runs one complete fight for each zombie)
    while enemyCount > 0 and playerHealth > 0:
        # Randomizes the zombie type for this fight
        zombieType = random.randrange(1, 5)

        # Keeps choosing until the zombie is different from the last one (codex)
        while zombieType == lastZombieType:
            zombieType = random.randrange(1, 5)

        # Saves this zombie type so the next fight can use a different one (codex)
        lastZombieType = zombieType

        if zombieType == 1:
            zombieName = "Spitter zombie"
            zombieHealth = 35
            zombieDMG = 5
        elif zombieType == 2:
            zombieName = "Jeremiah the zombie"
            zombieHealth = 40
            zombieDMG = 15
        elif zombieType == 3:
            zombieName = "John Wick's dog"
            zombieHealth = 6
            zombieDMG = 50
        else:
            zombieName = "No name zombie"
            zombieHealth = 20
            zombieDMG = 10

        print("Oh no! here comes a " + zombieName)

        # --- Fight this zombie ---
        while playerHealth > 0 and zombieHealth > 0:
            playerHealth -= zombieDMG
            zombieHealth -= weaponDMG

        # --- Display health AFTER the fight ends ---
        if playerHealth < 0:
            playerHealth = 0
        if zombieHealth < 0:
            zombieHealth = 0

        print("Fight over!")
        print(zombieName + "'s Health:", zombieHealth)
        print(playerName + "'s Health:", playerHealth)
        print("--------------------------")

        if playerHealth <= 0:
            print("You died... Game Over.")
            break

        enemyCount -= 1

    if playerHealth > 0 and enemyCount == 0:
        print("You survived Level 1!")

else:
    print("Game Over")
