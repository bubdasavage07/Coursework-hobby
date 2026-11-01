import pygame

class PlayerState:
    def __init__(self):
        self.playerHealth = 194
        self.zombieKillCount = 0

class WeaponSystem:
    def __init__(self):
        self.weapons = [
            {"name": "arrow", "damage": 5, "cooldown": 20, "img": "/resources/images/bullet.png"},
            {"name": "rusty knife", "damage": 12, "cooldown": 15, "img": "/resources/images/r.png"},
            {"name": "lead pipe", "damage": 20, "cooldown": 25},
            {"name": "bat", "damage": 30, "cooldown": 30},
            {"name": "pistol", "damage": 50, "cooldown": 10, "img": "/resources/images/nerfdart.png"},
            {"name": "fnuke", "damage": 100, "cooldown": 60, "img": "/resources/images/fnuke.png"}
        ]
        self.current_weapon_idx = 0

    def get_current_weapon(self):
        return self.weapons[self.current_weapon_idx]

    def load_current_weapon_image(self, cwd):
        weapon = self.get_current_weapon()
        # Fallback to a default image if 'img' key is missing
        img_rel_path = weapon.get("img", "/resources/images/bullet.png")
        return pygame.image.load(cwd + img_rel_path)

