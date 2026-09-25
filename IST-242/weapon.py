#weapon class
class Weapon:

    weaponName = "fist"
    weaponDMG = 5
    
    def weapon_choice(choice):
        match choice:
            case 0:
                weaponName = "fist"
                weaponDMG = 5
                print("fists")
            case 1:
                weaponName = "rusty knife"
                weaponDMG = 10
                print("rusty knife")
            case 2:
                weaponName = "lead pipe"
                weaponDMG = 15     
                print("lead pipe")
            case 3:
                weaponName = "bat"
                weaponDMG = 20
                print("bat")
            case 4:
                weaponName = "pistol"
                weaponDMG = 25
                print("pistol")
                #requires ammo
            case 5:
                weaponName = "fnuke"
                weaponDMG = -99
                print("fnuke")            
            case _:
                print("No weapon found")

#wep1 = Weapon()
#print(wep1.weaponName)
#print(wep1.weaponDMG)