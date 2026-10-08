from __future__ import annotations

import math
import random
from dataclasses import dataclass
from pathlib import Path

import pygame

WIDTH, HEIGHT, FPS = 640, 480, 60
GAME_LENGTH_MS = 90_000
RESOURCE_DIR = Path(__file__).resolve().parent / "resources"


@dataclass
class Bullet:
    angle: float
    x: float
    y: float

    def update(self) -> None:
        self.x += math.cos(self.angle) * 600 / FPS
        self.y += math.sin(self.angle) * 600 / FPS

    @property
    def off_screen(self) -> bool:
        return self.x < -64 or self.x > WIDTH or self.y < -64 or self.y > HEIGHT


@dataclass
class Enemy:
    x: float
    y: float

    def update(self) -> None:
        self.x -= 420 / FPS


def load_image(name: str) -> pygame.Surface:
    """Load an image relative to this file, regardless of the launch directory."""
    return pygame.image.load(RESOURCE_DIR / name).convert_alpha()


def load_sound(name: str) -> pygame.mixer.Sound | None:
    try:
        return pygame.mixer.Sound(RESOURCE_DIR / name)
    except pygame.error:
        return None


def play(sound: pygame.mixer.Sound | None) -> None:
    if sound is not None:
        sound.play()


def main() -> None:
    pygame.init()
    try:
        pygame.mixer.init()
    except pygame.error:
        pass  # The game remains playable on systems without an audio device.

    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Castle Defense")
    clock, font = pygame.time.Clock(), pygame.font.Font(None, 24)

    player, grass, castle = (load_image(name) for name in ("dude.png", "grass.png", "castle.png"))
    bullet_image, enemy_image = load_image("bullet.png"), load_image("badguy.png")
    healthbar, health_image = load_image("healthbar.png"), load_image("health.png")
    gameover, youwin = load_image("gameover.png"), load_image("youwin.png")
    hit_sound, enemy_sound, shoot_sound = (load_sound(name) for name in ("explode.wav", "enemy.wav", "shoot.wav"))
    for sound in (hit_sound, enemy_sound, shoot_sound):
        if sound is not None:
            sound.set_volume(0.05)
    if pygame.mixer.get_init():
        try:
            pygame.mixer.music.load(RESOURCE_DIR / "moonlight.wav")
            pygame.mixer.music.set_volume(0.25)
            pygame.mixer.music.play(-1)
        except pygame.error:
            pass

    player_pos = pygame.Vector2(100, 100)
    bullets: list[Bullet] = []
    enemies: list[Enemy] = [Enemy(WIDTH, 100)]
    health = 194
    shots = hits = spawn_counter = difficulty = 0
    spawn_delay = 100
    start_time = pygame.time.get_ticks()
    result: bool | None = None

    while result is None:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                direction = pygame.Vector2(pygame.mouse.get_pos()) - player_pos
                bullets.append(Bullet(math.atan2(direction.y, direction.x), player_pos.x, player_pos.y))
                shots += 1
                play(shoot_sound)

        pressed = pygame.key.get_pressed()
        movement = pygame.Vector2(pressed[pygame.K_d] - pressed[pygame.K_a], pressed[pygame.K_s] - pressed[pygame.K_w])
        if movement.length_squared():
            player_pos += movement.normalize() * (300 / FPS)
        player_pos.x = max(32, min(WIDTH - 32, player_pos.x))
        player_pos.y = max(32, min(HEIGHT - 32, player_pos.y))

        spawn_counter += 1
        if spawn_counter >= spawn_delay:
            enemies.append(Enemy(WIDTH, random.randint(50, 430)))
            spawn_counter, difficulty = 0, min(difficulty + 5, 35)
            spawn_delay = max(20, 100 - difficulty * 2)

        for bullet in bullets:
            bullet.update()
        bullets = [bullet for bullet in bullets if not bullet.off_screen]
        surviving_enemies: list[Enemy] = []
        for enemy in enemies:
            enemy.update()
            enemy_rect = enemy_image.get_rect(topleft=(enemy.x, enemy.y))
            if enemy.x < 64:
                health -= random.randint(5, 20)
                play(hit_sound)
                continue
            collision = next((bullet for bullet in bullets if enemy_rect.colliderect(bullet_image.get_rect(topleft=(bullet.x, bullet.y)))), None)
            if collision:
                bullets.remove(collision)
                hits += 1
                play(enemy_sound)
            elif enemy.x >= -64:
                surviving_enemies.append(enemy)
        enemies = surviving_enemies

        elapsed = pygame.time.get_ticks() - start_time
        result = True if elapsed >= GAME_LENGTH_MS else False if health <= 0 else None
        if result is not None:
            break

        screen.fill((0, 0, 0))
        for x in range(0, WIDTH, grass.get_width()):
            for y in range(0, HEIGHT, grass.get_height()):
                screen.blit(grass, (x, y))
        for y in (30, 135, 240, 345):
            screen.blit(castle, (0, y))
        for enemy in enemies:
            screen.blit(enemy_image, (enemy.x, enemy.y))
        for bullet in bullets:
            screen.blit(pygame.transform.rotate(bullet_image, -math.degrees(bullet.angle)), (bullet.x, bullet.y))
        aim = pygame.Vector2(pygame.mouse.get_pos()) - player_pos
        rotated_player = pygame.transform.rotate(player, -math.degrees(math.atan2(aim.y, aim.x)))
        screen.blit(rotated_player, rotated_player.get_rect(center=player_pos))
        screen.blit(healthbar, (5, 5))
        for offset in range(max(0, health)):
            screen.blit(health_image, (offset + 8, 8))
        remaining = max(0, (GAME_LENGTH_MS - elapsed) // 1000)
        timer = font.render(f"{remaining // 60}:{remaining % 60:02d}", True, (0, 0, 0))
        screen.blit(timer, timer.get_rect(topright=(635, 5)))
        pygame.display.flip()

    accuracy = 100 * hits / shots if shots else 0
    screen.blit(youwin if result else gameover, (0, 0))
    color = (0, 255, 0) if result else (255, 0, 0)
    text = font.render(f"Accuracy: {accuracy:.1f}%", True, color)
    screen.blit(text, text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 24)))
    pygame.display.flip()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                pygame.quit()
                return
        clock.tick(FPS)


if __name__ == "__main__":
    main()
