import pygame


class Button:
    def __init__(self, x, y, w, h, t):
        self.X = x
        self.Y = y
        self.W = w
        self.H = h
        self.text = t

    def collide(self, x, y):
        return self.X - self.W / 2 <= x <= self.X + self.W / 2 and self.Y - self.H / 2 <= y <= self.Y + self.H / 2

    def show(self, surface, font):
        pygame.draw.rect(surface, (255, 255, 255), (self.X - self.W / 2, self.Y - self.H / 2, self.W, self.H))
        pygame.draw.rect(surface, (0, 0, 0), (self.X - self.W / 2, self.Y - self.H / 2, self.W, self.H), 1)
        text_surf = font.render(self.text, True, (0, 0, 0))
        text_rect = text_surf.get_rect(center=(self.X, self.Y - 2))
        surface.blit(text_surf, text_rect)
