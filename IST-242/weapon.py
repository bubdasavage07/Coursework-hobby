#Weapon class
class Weapon:
    def __init__(self, weaponName="fists", weaponDMG=5):
        self.weaponName = weaponName
        self.weaponDMG = weaponDMG    
    
    def weapon_choice(self, choice):
        match choice:
            case 0:
                self.weaponName = "fists"
                self.weaponDMG = 5 
                print("fists")
            case 1:
                self.weaponName = "rusty knife"
                self.weaponDMG = 10 
                print("rusty knife")
            case 2:
                self.weaponName = "lead pipe"
                self.weaponDMG = 15 
                print("lead pipe")
            case 3:
                self.weaponName = "bat"
                self.weaponDMG = 20 
                print("bat")
            case 4:
                self.weaponName = "pistol"
                self.weaponDMG = 25 
                print("pistol")
            case 5:
                self.weaponName = "fnuke"
                self.weaponDMG = -99 
                print("fnuke")      
            case _:
                print("No weapon found")
            
#wep1 = Weapon()
#print(wep1.weaponName)
#print(wep1.weaponDMG)