# 1. Import libraries
import pygame, sys, math, os, random
from pygame.locals import *

# 2. Initialize the game
pygame.init()
pygame.mixer.init()

# Set screen window size (slightly taller to make room for a UI bottom panel)
width, height = 640, 540
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Zombie Survival - Pygame Edition")

# Predefine key pressed as false
keys = [False, False, False, False]

# Player & Weapon Classes / State (Ported from gameengine.py / player.py / weapon.py)
class PlayerState:
    def __init__(self):
        self.playerHealth = 194  # Matches healthvalue in original game.py
        self.zombieKillCount = 0

class WeaponSystem:
    def __init__(self):
        self.weapons = [
            {"name": "fists", "damage": 5, "cooldown": 20},
            {"name": "rusty knife", "damage": 12, "cooldown": 15},
            {"name": "lead pipe", "damage": 20, "cooldown": 25},
            {"name": "bat", "damage": 30, "cooldown": 30},
            {"name": "pistol", "damage": 50, "cooldown": 10},
            {"name": "fnuke", "damage": 100, "cooldown": 60}
        ]
        self.current_weapon_idx = 0

    def get_current_weapon(self):
        return self.weapons[self.current_weapon_idx]

p1 = PlayerState()
weapon_system = WeaponSystem()

# Select player position in window
playerpos = [100, 100]

# Shooting variables
acc = [0, 0]
arrows = []

# Badguys / enemies
badtimer = 100
badtimer1 = 0
badguys = [[640, 100]]

# Get path to images
cwd = os.getcwd().replace('\\', '/')

# 3. Load player images and assets
player_img = pygame.image.load(cwd + "/resources/images/dude.png")
grass = pygame.image.load(cwd + "/resources/images/grass.png")
castle = pygame.image.load(cwd + "/resources/images/castle.png")
arrow = pygame.image.load(cwd + "/resources/images/bullet.png")
badguyimg1 = pygame.image.load(cwd + "/resources/images/badguy.png")
badguyimg = badguyimg1
healthbar = pygame.image.load(cwd + "/resources/images/healthbar.png")
health = pygame.image.load(cwd + "/resources/images/health.png")
gameover = pygame.image.load(cwd + "/resources/images/gameover.png")
youwin = pygame.image.load(cwd + "/resources/images/youwin.png")

# 3.1 Load audio
hit = pygame.mixer.Sound(cwd + "/resources/audio/explode.wav")
enemy = pygame.mixer.Sound(cwd + "/resources/audio/enemy.wav")
shoot = pygame.mixer.Sound(cwd + "/resources/audio/shoot.wav")
hit.set_volume(0.05)
shoot.set_volume(0.05)
enemy.set_volume(0.05)
pygame.mixer.music.load(cwd + "/resources/audio/moonlight.wav")
pygame.mixer.music.play(-1, 0.0)
pygame.mixer.music.set_volume(0.25)

# Define weapon selection button rectangles on the screen UI panel (bottom area y: 480 to 540)
button_rects = []
btn_width, btn_height = 95, 35
for i, w in enumerate(weapon_system.weapons):
    bx = 10 + i * 103
    by = 490
    button_rects.append((pygame.Rect(bx, by, btn_width, btn_height), i))

# 4. Keep looping
running = 1
exitcode = 0
while running:
    badtimer -= 1

    # 5. Clear the screen before drawing it again
    screen.fill(0)

    # 6. Draw the grass tiling across the upper play area (height up to 480)
    for x in range(width // grass.get_width() + 1):
        for y in range(480 // grass.get_height() + 1):
            screen.blit(grass, (x * grass.get_width(), y * grass.get_height()))

    # 6a. Draw the castles once per frame
    screen.blit(castle, (0, 30))
    screen.blit(castle, (0, 135))
    screen.blit(castle, (0, 240))
    screen.blit(castle, (0, 345))

    # 6.1 Set player position and rotation (restricted to play area Y < 480)
    position = pygame.mouse.get_pos()
    angle = math.atan2(position[1] - (playerpos[1] + 32), position[0] - (playerpos[0] + 26))
    playerrot = pygame.transform.rotate(player_img, 360 - angle * 57.29)
    playerpos1 = (playerpos[0] - playerrot.get_rect().width / 2, playerpos[1] - playerrot.get_rect().height / 2)
    screen.blit(playerrot, playerpos1)

    # 6.2 Draw arrows / projectiles
    for bullet in arrows[:]:
        velx = math.cos(bullet[0]) * 10
        vely = math.sin(bullet[0]) * 10
        bullet[1] += velx
        bullet[2] += vely
        if bullet[1] < -64 or bullet[1] > 640 or bullet[2] < -64 or bullet[2] > 480:
            arrows.remove(bullet)
        else:
            arrow1 = pygame.transform.rotate(arrow, 360 - bullet[0] * 57.29)
            screen.blit(arrow1, (bullet[1], bullet[2]))

    # 6.3 Draw badgers / zombies
    if badtimer == 0:
        badguys.append([640, random.randint(50, 430)])
        badtimer = 100 - (badtimer1 * 2)
        if badtimer1 >= 35:
            badtimer1 = 35
        else:
            badtimer1 += 5

    index = 0
    for badguy in badguys[:]:
        if badguy[0] < -64:
            badguys.remove(badguy)
            continue
        badguy[0] -= 7

        # 6.3.1 Attack castle
        badrect = pygame.Rect(badguyimg.get_rect())
        badrect.top = badguy[1]
        badrect.left = badguy[0]
        if badrect.left < 64:
            hit.play()
            p1.playerHealth -= random.randint(5, 20)
            badguys.remove(badguy)
            continue

        # 6.3.2 - Check for collisions with projectiles
        for bullet in arrows[:]:
            bullrect = pygame.Rect(arrow.get_rect())
            bullrect.left = bullet[1]
            bullrect.top = bullet[2]
            if badrect.colliderect(bullrect):
                enemy.play()
                acc[0] += 1
                p1.zombieKillCount += 1  # Track zombie kills from gameengine logic
                if badguy in badguys:
                    badguys.remove(badguy)
                if bullet in arrows:
                    arrows.remove(bullet)
                break

    for badguy in badguys:
        screen.blit(badguyimg, badguy)

    # 6.4 Draw clock & Stats (Kills & Weapon)
    font = pygame.font.Font(None, 24)
    survivedtext = font.render(str((90000 - pygame.time.get_ticks()) // 60000) + ":" + str((90000 - pygame.time.get_ticks()) // 1000 % 60).zfill(2), True, (0, 0, 0))
    textRect = survivedtext.get_rect()
    textRect.topright = [635, 5]
    screen.blit(survivedtext, textRect)

    # Display current weapon & kills info
    current_wep = weapon_system.get_current_weapon()
    stats_text = font.render(f"Weapon: {current_wep['name']} | Kills: {p1.zombieKillCount}", True, (255, 255, 255))
    screen.blit(stats_text, (200, 10))

    # 6.5 Draw healthbar
    screen.blit(healthbar, (5, 5))
    for health1 in range(max(0, p1.playerHealth)):
        screen.blit(health, (health1 + 8, 8))

    # --- 6.6 Draw UI Control Panel for Weapons at the bottom ---
    pygame.draw.rect(screen, (30, 30, 30), (0, 480, width, 60))
    for rect, idx in button_rects:
        is_selected = (idx == weapon_system.current_weapon_idx)
        btn_color = (0, 150, 0) if is_selected else (100, 100, 100)
        pygame.draw.rect(screen, btn_color, rect, border_radius=4)
        pygame.draw.rect(screen, (255, 255, 255), rect, 2, border_radius=4)
        
        wep_name = weapon_system.weapons[idx]["name"]
        btn_text = font.render(wep_name, True, (255, 255, 255))
        text_rect = btn_text.get_rect(center=rect.center)
        screen.blit(btn_text, text_rect)

    # 7. Update the screen
    pygame.display.flip()

    # 8. Loop through events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit(0)
            
        if event.type == pygame.KEYDOWN:
            if event.key == K_w:
                keys[0] = True
            elif event.key == K_a:
                keys[1] = True
            elif event.key == K_s:
                keys[2] = True
            elif event.key == K_d:
                keys[3] = True
                
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_w:
                keys[0] = False
            elif event.key == pygame.K_a:
                keys[1] = False
            elif event.key == pygame.K_s:
                keys[2] = False
            elif event.key == pygame.K_d:
                keys[3] = False
                
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = event.pos
            # Check if user clicked on weapon selection buttons
            clicked_ui = False
            for rect, idx in button_rects:
                if rect.collidepoint(mouse_pos):
                    weapon_system.current_weapon_idx = idx
                    clicked_ui = True
                    break
            
            # If they clicked inside the gameplay zone, shoot projectile
            if not clicked_ui and mouse_pos[1] < 480:
                shoot.play()
                acc[1] += 1
                arrows.append([math.atan2(mouse_pos[1] - (playerpos1[1] + 32), mouse_pos[0] - (playerpos1[0] + 26)), playerpos1[0] + 32, playerpos1[1] + 32])

    # 9. Move player (bounded within screen and above UI bar)
    if keys[0] and playerpos[1] > 40:
        playerpos[1] -= 5
    elif keys[2] and playerpos[1] < 440:
        playerpos[1] += 5
    if keys[1] and playerpos[0] > 40:
        playerpos[0] -= 5
    elif keys[3] and playerpos[0] < 600:
        playerpos[0] += 5

    # 10. Win/Lose check
    if pygame.time.get_ticks() >= 90000:
        running = 0
        exitcode = 1
    if p1.playerHealth <= 0:
        running = 0
        exitcode = 0

    if acc[1] != 0:
        accuracy = acc[0] * 1.0 / acc[1] * 100
    else:
        accuracy = 0

# 11. Win/lose display loop
if exitcode == 0:
    font = pygame.font.Font(None, 24)
    text = font.render("Accuracy: " + str(round(accuracy, 2)) + "% | Zombies Killed: " + str(p1.zombieKillCount), True, (255, 0, 0))
    textRect = text.get_rect()
    textRect.centerx = screen.get_rect().centerx
    textRect.centery = screen.get_rect().centery + 24
    screen.blit(gameover, (0, 0))
    screen.blit(text, textRect)
else:
    font = pygame.font.Font(None, 24)
    text = font.render("Accuracy: " + str(round(accuracy, 2)) + "% | Zombies Killed: " + str(p1.zombieKillCount), True, (0, 255, 0))
    textRect = text.get_rect()
    textRect.centerx = screen.get_rect().centerx
    textRect.centery = screen.get_rect().centery + 24
    screen.blit(youwin, (0, 0))
    screen.blit(text, textRect)

pygame.display.flip()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit(0)