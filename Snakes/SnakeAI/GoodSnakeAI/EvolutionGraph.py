import pygame


class EvolutionGraph:
    def __init__(self):
        self.visible = False

    def toggle(self):
        self.visible = not self.visible

    def draw(self, surface, evolution, rect, font, small_font):
        if not self.visible:
            return
        x0, y0, w, h = rect
        pygame.draw.rect(surface, (150, 150, 150), rect)
        pygame.draw.rect(surface, (0, 0, 0), rect, 2)

        title = font.render("Generation", True, (0, 0, 0))
        surface.blit(title, title.get_rect(center=(x0 + w / 2, y0 + h - 15)))

        label = font.render("Score", True, (0, 0, 0))
        surface.blit(label, label.get_rect(center=(x0 + 25, y0 + h / 2)))

        x = x0 + 50
        y = y0 + h - 35
        xbuff = (w - 50) / 51.0
        ybuff = (h - 50) / 200.0

        for i in range(0, 51, 5):
            t = small_font.render(str(i), True, (0, 0, 0))
            surface.blit(t, (x - 5, y))
            x += xbuff * 5

        x = x0 + 35
        y = y0 + h - 50
        ydif = ybuff * 10.0
        for i in range(0, 200, 10):
            t = small_font.render(str(i), True, (0, 0, 0))
            surface.blit(t, (x, y - 6))
            pygame.draw.line(surface, (200, 200, 200), (x0 + 50, y), (x0 + w - 10, y), 1)
            y -= ydif

        pygame.draw.line(surface, (0, 0, 0), (x0 + 50, y0 + 10), (x0 + 50, y0 + h - 50), 3)
        pygame.draw.line(surface, (0, 0, 0), (x0 + 50, y0 + h - 50), (x0 + w - 10, y0 + h - 50), 3)

        if len(evolution) < 2:
            return

        pygame.draw.lines(
            surface,
            (255, 0, 0),
            False,
            [
                (
                    x0 + 50 + (i * xbuff),
                    y0 + h - 50 - (score * ybuff),
                )
                for i, score in enumerate(evolution)
            ],
            2,
        )
