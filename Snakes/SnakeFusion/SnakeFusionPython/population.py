import random

from snake import Snake


class Population:
    def __init__(self, size: int, best: Snake | None = None, mutation_rate: float = 0.01) -> None:
        self.gen = 1
        self.global_best = 4
        self.global_best_fitness = 0
        self.current_best = 4
        self.current_best_snake = 0
        self.population_id = random.randrange(0, 10000)
        self._mutation_rate = mutation_rate

        if best is None:
            self.snakes = [Snake() for _ in range(size)]
            self.global_best_snake = self.snakes[0].clone()
        else:
            self.snakes = [best.clone() for _ in range(size)]
            for s in self.snakes:
                s.mutate(self._mutation_rate)
            self.global_best_snake = best.clone()

    def set_mutation_rate(self, mutation_rate: float) -> None:
        self._mutation_rate = mutation_rate

    def update_alive(self, show_all: bool, surface) -> None:
        for i, s in enumerate(self.snakes):
            if s.alive:
                s.look()
                s.set_velocity()
                s.move()
                if s.alive and (show_all or i == self.current_best_snake):
                    s.show(surface)
        self.set_current_best()

    def done(self) -> bool:
        return not any(s.alive for s in self.snakes)

    def calc_fitness(self) -> None:
        for s in self.snakes:
            s.calc_fitness()

    def natural_selection(self) -> None:
        self.set_best_snake()
        new_snakes = [self.global_best_snake.clone()]
        for _ in range(1, len(self.snakes)):
            p1 = self.select_snake()
            p2 = self.select_snake()
            child = p1.crossover(p2)
            child.mutate(self._mutation_rate)
            new_snakes.append(child)

        self.snakes = new_snakes
        self.gen += 1
        self.current_best = 4

    def select_snake(self) -> Snake:
        fitness_sum = sum(s.fitness for s in self.snakes)
        if fitness_sum <= 0:
            return self.snakes[0]

        rand_val = random.randrange(0, fitness_sum)
        running = 0
        for s in self.snakes:
            running += s.fitness
            if running > rand_val:
                return s
        return self.snakes[0]

    def set_best_snake(self) -> None:
        max_fit = 0
        max_idx = 0
        for i, s in enumerate(self.snakes):
            if s.fitness > max_fit:
                max_fit = s.fitness
                max_idx = i

        if max_fit > self.global_best_fitness:
            self.global_best_fitness = max_fit
            self.global_best_snake = self.snakes[max_idx].clone()

    def set_current_best(self) -> None:
        if self.done():
            return

        max_len = 0
        max_idx = 0
        for i, s in enumerate(self.snakes):
            if s.alive and s.len > max_len:
                max_len = s.len
                max_idx = i

        if max_len > self.current_best:
            self.current_best = max_len

        current = self.snakes[self.current_best_snake]
        if (not current.alive) or (max_len > current.len + 5):
            self.current_best_snake = max_idx

        if self.current_best > self.global_best:
            self.global_best = self.current_best
