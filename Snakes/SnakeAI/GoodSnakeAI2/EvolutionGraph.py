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

        left = x0 + 50
        top = y0 + 10
        right = x0 + w - 10
        bottom = y0 + h - 50
        chart_w = max(1, right - left)
        chart_h = max(1, bottom - top)

        pygame.draw.line(surface, (0, 0, 0), (left, top), (left, bottom), 3)
        pygame.draw.line(surface, (0, 0, 0), (left, bottom), (right, bottom), 3)

        if len(evolution) == 0:
            return

        min_score = min(evolution)
        max_score = max(evolution)
        if min_score == max_score:
            min_score = 0
            max_score = max(1, max_score)

        gen_count = len(evolution)
        max_gen_index = max(1, gen_count - 1)

        x_ticks = min(10, max_gen_index)
        for i in range(x_ticks + 1):
            tick_gen = int(round((i / float(x_ticks)) * max_gen_index))
            tick_x = left + int((tick_gen / float(max_gen_index)) * chart_w)
            pygame.draw.line(surface, (180, 180, 180), (tick_x, top), (tick_x, bottom), 1)
            t = small_font.render(str(tick_gen), True, (0, 0, 0))
            surface.blit(t, (tick_x - (t.get_width() // 2), bottom + 6))

        y_ticks = 8
        score_span = float(max_score - min_score)
        for i in range(y_ticks + 1):
            ratio = i / float(y_ticks)
            score_val = min_score + int(round(score_span * ratio))
            tick_y = bottom - int(ratio * chart_h)
            pygame.draw.line(surface, (200, 200, 200), (left, tick_y), (right, tick_y), 1)
            t = small_font.render(str(score_val), True, (0, 0, 0))
            surface.blit(t, (x0 + 6, tick_y - 7))

        if len(evolution) < 2:
            single_ratio = 0.0
            if score_span > 0:
                single_ratio = (evolution[0] - min_score) / score_span
            y = bottom - int(single_ratio * chart_h)
            pygame.draw.circle(surface, (255, 0, 0), (left, y), 3)
            return

        points = []
        for i, score in enumerate(evolution):
            px = left + int((i / float(max_gen_index)) * chart_w)
            py_ratio = (score - min_score) / score_span
            py = bottom - int(py_ratio * chart_h)
            points.append((px, py))

        pygame.draw.lines(surface, (255, 0, 0), False, points, 2)
