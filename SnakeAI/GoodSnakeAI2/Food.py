import random
import pygame
import config
from vec2 import Vec2


class Food:
    def __init__(self):
        x = config.BOARD_X + random.randrange(config.GRID_W) * config.SIZE
        y = config.BOARD_Y + random.randrange(config.GRID_H) * config.SIZE
        self.pos = Vec2(x, y)

    def show(self, surface):
        pygame.draw.rect(surface, (255, 0, 0), (self.pos.x, self.pos.y, config.SIZE, config.SIZE))

    def clone(self):
        clone = Food()
        clone.pos.x = self.pos.x
        clone.pos.y = self.pos.y
        return clone
