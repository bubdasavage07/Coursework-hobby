import csv
import os
import sys
import pygame

import config
from Button import Button
from EvolutionGraph import EvolutionGraph
from Matrix import Matrix
from Population import Population
from Snake import Snake


def default
lt_model_path():
    return os.path.join(os.path.dirname(__file__), "data", "snake_model.csv")


def pick_load_file():
    path = default_model_path()
    if not os.path.exists(path):
        return None
    return path


def pick_save_file():
    return default_model_path()


def list_to_matrix(values, rows, cols):
    data = [[0.0 for _ in range(cols)] for _ in range(rows)]
    for i in range(rows):
        for j in range(cols):
            idx = j + i * cols
            if idx < len(values):
                data[i][j] = values[idx]
    return Matrix(data)


def load_model(path):
    with open(path, "r", newline="") as f:
        reader = csv.DictReader(f)
        fieldnames = reader.fieldnames
        if not fieldnames:
            return None, [], {}
        layer_cols = [name for name in fieldnames if name.startswith("L")]
        layer_cols.sort(key=lambda s: int(s[1:]))
        graph_col = "Graph"
        mutation_col = "MutationRate"
        generation_col = "Generation"
        best_score_col = "BestScore"

        layer_vals = {name: [] for name in layer_cols}
        evolution = []
        metadata = {}

        for row in reader:
            for name in layer_cols:
                val = row.get(name, "")
                if val != "":
                    layer_vals[name].append(float(val))
            if graph_col in row and row[graph_col] not in ("", None):
                try:
                    evolution.append(int(float(row[graph_col])))
                except ValueError:
                    pass
            if mutation_col in row and "mutation_rate" not in metadata:
                val = row.get(mutation_col, "")
                if val not in ("", None):
                    try:
                        metadata["mutation_rate"] = float(val)
                    except ValueError:
                        pass
            if generation_col in row and "generation" not in metadata:
                val = row.get(generation_col, "")
                if val not in ("", None):
                    try:
                        metadata["generation"] = int(float(val))
                    except ValueError:
                        pass
            if best_score_col in row and "best_score" not in metadata:
                val = row.get(best_score_col, "")
                if val not in ("", None):
                    try:
                        metadata["best_score"] = int(float(val))
                    except ValueError:
                        pass

    weights = []
    if not layer_cols:
        return None, evolution, metadata

    in_rows = config.hidden_nodes
    in_cols = 24 + 1
    weights.append(list_to_matrix(layer_vals[layer_cols[0]], in_rows, in_cols))

    for i in range(1, len(layer_cols) - 1):
        weights.append(list_to_matrix(layer_vals[layer_cols[i]], config.hidden_nodes, config.hidden_nodes + 1))

    out_rows = 4
    out_cols = config.hidden_nodes + 1
    weights.append(list_to_matrix(layer_vals[layer_cols[-1]], out_rows, out_cols))

    return weights, evolution, metadata


def save_model(path, pop, evolution):
    model_to_save = pop.bestSnake.clone()
    model_weights = model_to_save.brain.pull()
    weights = [w.toArray() for w in model_weights]

    max_len = max(len(w) for w in weights)

    fieldnames = ["L" + str(i) for i in range(len(weights))] + ["Graph", "MutationRate", "Generation", "BestScore"]

    with open(path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        g = 0
        for i in range(max_len):
            row = {}
            for j in range(len(weights)):
                if i < len(weights[j]):
                    row["L" + str(j)] = weights[j][i]
            if g < len(evolution):
                row["Graph"] = evolution[g]
                g += 1
            if i == 0:
                row["MutationRate"] = config.mutationRate
                row["Generation"] = pop.gen
                row["BestScore"] = pop.bestSnakeScore
            writer.writerow(row)


def seed_population_from_weights(pop, weights):
    layers = len(weights) - 1
    base = Snake(layers)
    base.brain.load([w.clone() for w in weights])

    pop.bestSnake = base.cloneForReplay()
    pop.snakes[0] = base.clone()
    for i in range(1, len(pop.snakes)):
        child = base.clone()
        child.mutate()
        pop.snakes[i] = child


def main():
    pygame.init()
    screen = pygame.display.set_mode((config.WIDTH, config.HEIGHT))
    pygame.display.set_caption("SnakeAI")
    clock = pygame.time.Clock()

    font_path = os.path.join(os.path.dirname(__file__), "data", "agencyfb-bold.ttf")
    if os.path.exists(font_path):
        font = pygame.font.Font(font_path, 32)
        font_small = pygame.font.Font(font_path, 20)
        font_mid = pygame.font.Font(font_path, 25)
        font_tiny = pygame.font.Font(font_path, 15)
    else:
        # Fallback to a default system font if the bundled font is missing.
        font = pygame.font.Font(None, 32)
        font_small = pygame.font.Font(None, 20)
        font_mid = pygame.font.Font(None, 25)
        font_tiny = pygame.font.Font(None, 15)

    evolution = []
    highscore = 0

    graphButton = Button(349, 15, 100, 30, "Graph")
    loadButton = Button(249, 15, 100, 30, "Load")
    saveButton = Button(149, 15, 100, 30, "Save")
    increaseMut = Button(340, 85, 20, 20, "+")
    decreaseMut = Button(365, 85, 20, 20, "-")

    graph = EvolutionGraph()

    if config.humanPlaying:
        snake = Snake()
        pop = None
    else:
        snake = None
        pop = Population(2000, evolution)

    model = None

    running = True
    while running:
        clock.tick(config.fps)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = event.pos
                if graphButton.collide(mx, my):
                    graph.toggle()
                if loadButton.collide(mx, my):
                    path = pick_load_file()
                    if path is None:
                        print("No saved model found at:", default_model_path())
                    if path:
                        weights, evo, metadata = load_model(path)
                        if weights:
                            evolution[:] = evo
                            if "mutation_rate" in metadata:
                                config.mutationRate = metadata["mutation_rate"]
                                config.defaultmutation = metadata["mutation_rate"]

                            config.humanPlaying = False
                            config.modelLoaded = False
                            model = None
                            pop = Population(2000, evolution)
                            seed_population_from_weights(pop, weights)
                            if "generation" in metadata:
                                pop.gen = metadata["generation"]
                            else:
                                pop.gen = len(evolution)
                            if "best_score" in metadata:
                                pop.bestSnakeScore = metadata["best_score"]
                            elif evolution:
                                pop.bestSnakeScore = evolution[-1]
                            highscore = max(highscore, pop.bestSnakeScore)
                if saveButton.collide(mx, my):
                    if pop is not None:
                        path = pick_save_file()
                        if path:
                            save_model(path, pop, evolution)
                            print("Saved model to:", path)
                if increaseMut.collide(mx, my):
                    config.mutationRate *= 2
                    config.defaultmutation = config.mutationRate
                if decreaseMut.collide(mx, my):
                    config.mutationRate /= 2
                    config.defaultmutation = config.mutationRate
            elif event.type == pygame.KEYDOWN:
                if config.humanPlaying and snake is not None:
                    if event.key == pygame.K_UP:
                        snake.moveUp()
                    elif event.key == pygame.K_DOWN:
                        snake.moveDown()
                    elif event.key == pygame.K_LEFT:
                        snake.moveLeft()
                    elif event.key == pygame.K_RIGHT:
                        snake.moveRight()

        if config.humanPlaying and snake is not None:
            snake.move()
            if snake.dead:
                snake = Snake()
        else:
            if not config.modelLoaded:
                if pop.done():
                    highscore = pop.bestSnake.score
                    pop.calculateFitness()
                    pop.naturalSelection()
                else:
                    pop.update()
            else:
                if model is not None:
                    model.look()
                    model.think()
                    model.move()
                    if model.dead:
                        newmodel = Snake()
                        newmodel.brain = model.brain.clone()
                        model = newmodel

        screen.fill((0, 0, 0))
        pygame.draw.line(screen, (255, 255, 255), (config.PANEL_W, 0), (config.PANEL_W, config.HEIGHT), 1)
        pygame.draw.rect(screen, (255, 255, 255), (config.BOARD_X, config.BOARD_Y, config.BOARD_W, config.BOARD_H), 1)

        if config.humanPlaying and snake is not None:
            snake.show(screen)
            text = font_small.render("SCORE : " + str(snake.score), True, (150, 150, 150))
            screen.blit(text, (500, 50))
        else:
            if not config.modelLoaded:
                pop.show(screen, font_tiny)
                screen.blit(font_mid.render("GEN : " + str(pop.gen), True, (150, 150, 150)), (120, 60))
                screen.blit(font_mid.render("MUTATION RATE : " + str(config.mutationRate * 100) + "%", True, (150, 150, 150)), (120, 90))
                screen.blit(font_mid.render("SCORE : " + str(pop.bestSnake.score), True, (150, 150, 150)), (120, config.HEIGHT - 45))
                screen.blit(font_mid.render("HIGHSCORE : " + str(highscore), True, (150, 150, 150)), (120, config.HEIGHT - 15))
                increaseMut.show(screen, font_small)
                decreaseMut.show(screen, font_small)
            else:
                if model is not None:
                    model.show(screen)
                    model.brain.show(screen, 0, 0, 360, 790, model.vision, model.decision, font_tiny)
                    screen.blit(font_mid.render("SCORE : " + str(model.score), True, (150, 150, 150)), (120, config.HEIGHT - 45))

            screen.blit(font_small.render("RED < 0", True, (255, 0, 0)), (120, config.HEIGHT - 75))
            screen.blit(font_small.render("BLUE > 0", True, (0, 0, 255)), (200, config.HEIGHT - 75))
            graphButton.show(screen, font_small)
            loadButton.show(screen, font_small)
            saveButton.show(screen, font_small)

        graph_rect = (config.PANEL_W + 20, 20, 900, 600)
        graph.draw(screen, evolution, graph_rect, font_small, font_tiny)

        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()
