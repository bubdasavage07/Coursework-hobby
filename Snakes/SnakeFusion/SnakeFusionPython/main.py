from pathlib import Path

import pygame

from config import DEFAULT_SPEED, GLOBAL_MUTATION_RATE, WINDOW_H, WINDOW_W
from world import World


def draw_data(surface, font, speed, mutation_rate, world, world_of_legends, train_legends, showing_legend, fusion_go):
    pygame.draw.line(surface, (255, 255, 255), (400, 0), (400, 400), 1)
    pygame.draw.line(surface, (255, 255, 255), (0, 400), (800, 400), 1)

    lines = []
    if train_legends and world_of_legends is not None:
        lines = [
            f"Generation: {world_of_legends.gen}",
            f"Speed: {speed}",
            f"Global Best: {world_of_legends.world_best_score}",
            f"Mutation Rate: {mutation_rate}",
        ]
    elif showing_legend and world.legend is not None:
        lines = [f"Score: {world.legend.len - 4}"]
    elif fusion_go and world.fused_snake is not None:
        lines = [f"Score: {world.fused_snake.len - 4}"]
    else:
        lines = [
            f"Generation: {world.gen}",
            f"Speed: {speed}",
            f"Global Best: {world.world_best_score}",
            f"Mutation Rate: {mutation_rate}",
        ]

    y = 100
    for line in lines:
        surface.blit(font.render(line, True, (255, 255, 255)), (10, y))
        y += 50


def main() -> None:
    pygame.init()
    screen = pygame.display.set_mode((WINDOW_W, WINDOW_H))
    pygame.display.set_caption("SnakeFusion Python")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont(None, 30)

    speed = DEFAULT_SPEED
    show_all = True
    train_legend_snakes = False
    showing_legend = False
    fusion_go = False
    mutation_rate = GLOBAL_MUTATION_RATE

    base_path = Path(__file__).resolve().parent
    world = World(5, 2000, base_path, mutation_rate)
    world_of_legends = None

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    show_all = not show_all
                elif event.key in (pygame.K_PLUS, pygame.K_EQUALS, pygame.K_KP_PLUS):
                    speed += 10
                elif event.key in (pygame.K_MINUS, pygame.K_KP_MINUS):
                    speed = max(10, speed - 10)
                elif event.key == pygame.K_f:
                    fusion_go = True
                    world.snake_fusion()
                elif event.key == pygame.K_0:
                    showing_legend = True
                    world.play_legend(0)
                elif event.key == pygame.K_1:
                    showing_legend = True
                    world.play_legend(1)
                elif event.key == pygame.K_2:
                    showing_legend = True
                    world.play_legend(2)
                elif event.key == pygame.K_3:
                    showing_legend = True
                    world.play_legend(3)
                elif event.key == pygame.K_4:
                    showing_legend = True
                    world.play_legend(4)
                elif event.key == pygame.K_h:
                    mutation_rate /= 2
                    world.set_mutation_rate(mutation_rate)
                    if world_of_legends:
                        world_of_legends.set_mutation_rate(mutation_rate)
                elif event.key == pygame.K_d:
                    mutation_rate *= 2
                    world.set_mutation_rate(mutation_rate)
                    if world_of_legends:
                        world_of_legends.set_mutation_rate(mutation_rate)
                elif event.key == pygame.K_l:
                    train_legend_snakes = not train_legend_snakes
                    if train_legend_snakes:
                        world.load_best_snakes()
                        world_of_legends = World(0, 1000, base_path, mutation_rate, legends_array=world.snakes_of_legend)

        screen.fill((40, 40, 40))
        draw_data(screen, font, speed, mutation_rate, world, world_of_legends, train_legend_snakes, showing_legend, fusion_go)

        if train_legend_snakes and world_of_legends:
            if not world_of_legends.done():
                world_of_legends.update_alive(show_all, screen)
            else:
                world_of_legends.genetic_algorithm()
        elif showing_legend:
            if world.legend and world.legend.alive:
                world.update_legend(screen)
            elif world.legend and world.legend.len < 100:
                world.play_legend(world.legend_no)
            else:
                showing_legend = False
        elif fusion_go:
            if world.fused_snake and world.fused_snake.alive:
                world.update_super_snake(screen)
            else:
                fusion_go = False
        else:
            if not world.done():
                world.update_alive(show_all, screen)
            else:
                world.genetic_algorithm()

        pygame.display.flip()
        clock.tick(speed)

    pygame.quit()


if __name__ == "__main__":
    main()
