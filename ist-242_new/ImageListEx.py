import os, pygame

# Get path to images
#cwd = os.getcwd().replace('\\', '/')
cwd = os.path.dirname(os.path.abspath(__file__)).replace('\\','/')

imgList = ["/resources/images/dude.png", 
            "/resources/images/grass.png",
            "/resources/images/castle.png",
            "/resources/images/badguy.gif",
            "/resources/images/healthbar.png",
            "/resources/images/health.png",
            "/resources/images/gameover.png",
            "/resources/images/youwin.png"
            ]

print(imgList)
print(imgList[4])


"""
# 3. Load player images and assets
player_img = pygame.image.load(cwd + "/resources/images/dude.png")
grass = pygame.image.load(cwd + "/resources/images/grass.png")
castle = pygame.image.load(cwd + "/resources/images/castle.png")
# arrow = pygame.image.load(cwd + "/resources/images/bullet.png")
arrow = weapon_system.load_current_weapon_image(cwd)
badguyimg1 = pygame.image.load(cwd + "/resources/images/badguy.gif")
badguyimg = badguyimg1
healthbar = pygame.image.load(cwd + "/resources/images/healthbar.png")
health = pygame.image.load(cwd + "/resources/images/health.png")
gameover = pygame.image.load(cwd + "/resources/images/gameover.png")
youwin = pygame.image.load(cwd + "/resources/images/youwin.png")
"""