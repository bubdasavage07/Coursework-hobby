import csv
from pathlib import Path

import pygame

from population import Population
from snake import Snake
from super_snake import SuperSnake


class World:
    def __init__(self, species_no: int, pop_size: int, base_path: Path, mutation_rate: float, legends_array: list[Snake] | None = None) -> None:
        self.base_path = base_path
        self.gen = 0
        self.world_best_score = 0

        if legends_array is None:
            self.species = [Population(pop_size, mutation_rate=mutation_rate) for _ in range(species_no)]
        else:
            self.species = [Population(pop_size, best=s, mutation_rate=mutation_rate) for s in legends_array]
            for i in range(len(legends_array)):
                with (self.base_path / "data" / f"SnakeStats{i}.csv").open("r", newline="") as f:
                    r = csv.reader(f)
                    next(r, None)
                    row = next(r)
                    self.species[i].population_id = int(float(row[1]))

        self.snakes_of_legend = [Snake() for _ in range(5)]
        self.top_brains = [None] * len(self.snakes_of_legend)
        self.fused_snake = None
        self.legend = None
        self.legend_no = 0

        self.save_super_frames = False
        self._frame_index = 0

    def set_mutation_rate(self, mutation_rate: float) -> None:
        for sp in self.species:
            sp.set_mutation_rate(mutation_rate)

    def update_alive(self, show_all: bool, surface: pygame.Surface) -> None:
        for sp in self.species:
            sp.update_alive(show_all, surface)

    def genetic_algorithm(self) -> None:
        for sp in self.species:
            sp.calc_fitness()
            sp.natural_selection()
        self.gen += 1
        self.set_top_score()
        for i in range(len(self.species)):
            self.save_top_snake(i)

    def load_best_snakes(self) -> None:
        for i in range(5):
            self.snakes_of_legend[i] = Snake.load_snake(i, self.base_path)

    def snake_fusion(self) -> None:
        self.load_best_snakes()
        self.top_brains = [s.brain.clone() for s in self.snakes_of_legend]
        self.fused_snake = SuperSnake(self.top_brains)

    def update_super_snake(self, surface: pygame.Surface) -> None:
        if self.fused_snake is None:
            return
        self.fused_snake.look()
        self.fused_snake.set_velocity()
        self.fused_snake.move()
        self.fused_snake.show(surface)

        if self.save_super_frames:
            out = self.base_path / "output" / "superSnake"
            out.mkdir(parents=True, exist_ok=True)
            self._frame_index += 1
            pygame.image.save(surface, out / f"frame_{self._frame_index:07d}.png")

    def update_legend(self, surface: pygame.Surface) -> None:
        if self.legend is None:
            return
        self.legend.look()
        self.legend.set_velocity()
        self.legend.move()
        self.legend.show(surface)

    def done(self) -> bool:
        return all(sp.done() for sp in self.species)

    def set_top_score(self) -> None:
        max_fit = 0
        max_idx = 0
        for i, sp in enumerate(self.species):
            if sp.global_best_fitness > max_fit:
                max_fit = sp.global_best_fitness
                max_idx = i
        self.world_best_score = self.species[max_idx].global_best

    def save_top_snake(self, species_no: int) -> None:
        stored_path = self.base_path / "data" / "snakesStored.csv"
        with stored_path.open("r", newline="") as f:
            row = [int(float(x)) for x in next(csv.reader(f))]

        snake_no = -1
        for i, v in enumerate(row):
            if v == 0:
                snake_no = i
                break

        sp = self.species[species_no]
        if snake_no != -1:
            sp.global_best_snake.clone().save_snake(snake_no, sp.global_best, sp.population_id, self.base_path)
            row[snake_no] = 1
            with stored_path.open("w", newline="") as f:
                csv.writer(f).writerow(row)
            return

        for i in range(len(row)):
            with (self.base_path / "data" / f"SnakeStats{i}.csv").open("r", newline="") as f:
                r = csv.reader(f)
                next(r, None)
                st = next(r)
                top = int(float(st[0]))
                pop_id = int(float(st[1]))
            if pop_id == sp.population_id:
                if sp.global_best > top:
                    sp.global_best_snake.clone().save_snake(i, sp.global_best, sp.population_id, self.base_path)
                return

        min_score = sp.global_best
        min_idx = -1
        for i in range(len(row)):
            with (self.base_path / "data" / f"SnakeStats{i}.csv").open("r", newline="") as f:
                r = csv.reader(f)
                next(r, None)
                st = next(r)
                top = int(float(st[0]))
            if top < min_score:
                min_score = top
                min_idx = i

        if min_idx != -1:
            sp.global_best_snake.clone().save_snake(min_idx, sp.global_best, sp.population_id, self.base_path)

    def play_legend(self, snake_no: int) -> None:
        self.load_best_snakes()
        self.legend = self.snakes_of_legend[snake_no].clone()
        self.legend_no = snake_no
        self.legend.test = True


if __name__ == "__main__":
    from main import main

    main()
