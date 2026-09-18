import csv
from pathlib import Path

import pygame

from config import GRID, PLAY_MAX_X, PLAY_MAX_Y, PLAY_MIN_X, PLAY_MIN_Y
from food import Food
from neural_net import NeuralNet
from vector2d import PVector


class Snake:
    def __init__(self) -> None:
        self.len = 4
        x, y = 600, 200
        self.pos = PVector(x, y)
        self.vel = PVector(GRID, 0)
        self.tail_positions: list[PVector] = [PVector(x - 30, y), PVector(x - 20, y), PVector(x - 10, y)]

        self.food = Food()
        self.brain = NeuralNet(24, 18, 4)
        self.vision = [0.0] * 24
        self.decision: list[float] = []

        self.lifetime = 0
        self.fitness = 0
        self.left_to_live = 200
        self.grow_count = 0

        self.alive = True
        self.test = False

    def mutate(self, mutation_rate: float) -> None:
        self.brain.mutate(mutation_rate)

    def set_velocity(self) -> None:
        self.decision = self.brain.output(self.vision)
        max_idx = max(range(len(self.decision)), key=self.decision.__getitem__)
        if max_idx == 0:
            self.vel = PVector(-GRID, 0)
        elif max_idx == 1:
            self.vel = PVector(0, -GRID)
        elif max_idx == 2:
            self.vel = PVector(GRID, 0)
        else:
            self.vel = PVector(0, GRID)

    def move(self) -> None:
        self.lifetime += 1
        self.left_to_live -= 1
        if self.left_to_live < 0:
            self.alive = False
            return

        nx = self.pos.x + self.vel.x
        ny = self.pos.y + self.vel.y

        if self.gonna_die(nx, ny):
            self.alive = False
            return

        if nx == self.food.pos.x and ny == self.food.pos.y:
            self.eat()

        if self.grow_count > 0:
            self.grow_count -= 1
            self.grow()
        else:
            for i in range(len(self.tail_positions) - 1):
                self.tail_positions[i] = self.tail_positions[i + 1].copy()
            self.tail_positions[self.len - 2] = self.pos.copy()

        self.pos.add(self.vel)

    def eat(self) -> None:
        self.food = Food()
        while self.food.pos in self.tail_positions:
            self.food = Food()

        self.left_to_live += 100
        self.grow_count += 4 if (self.test or self.len >= 10) else 1

    def show(self, surface: pygame.Surface) -> None:
        for p in self.tail_positions:
            pygame.draw.rect(surface, (255, 255, 255), pygame.Rect(int(p.x), int(p.y), GRID, GRID))
        pygame.draw.rect(surface, (255, 255, 255), pygame.Rect(int(self.pos.x), int(self.pos.y), GRID, GRID))
        pygame.draw.rect(
            surface,
            (255, 0, 0),
            pygame.Rect(int(self.food.pos.x), int(self.food.pos.y), GRID, GRID),
        )

    def grow(self) -> None:
        self.tail_positions.append(self.pos.copy())
        self.len += 1

    def gonna_die(self, x: float, y: float) -> bool:
        if x < PLAY_MIN_X or y < PLAY_MIN_Y or x >= PLAY_MAX_X or y >= PLAY_MAX_Y:
            return True
        return self.is_on_tail(x, y)

    def is_on_tail(self, x: float, y: float) -> bool:
        return any(x == p.x and y == p.y for p in self.tail_positions)

    def calc_fitness(self) -> None:
        if self.len < 10:
            self.fitness = int(self.lifetime * self.lifetime * (2 ** int(self.len)))
        else:
            fit = self.lifetime * self.lifetime
            fit *= 2**10
            fit *= self.len - 9
            self.fitness = int(fit)

    def crossover(self, partner: "Snake") -> "Snake":
        child = Snake()
        child.brain = self.brain.crossover(partner.brain)
        return child

    def clone(self) -> "Snake":
        clone = Snake()
        clone.brain = self.brain.clone()
        clone.alive = True
        return clone

    def save_snake(self, snake_no: int, score: int, pop_id: int, base_path: Path) -> None:
        stats_path = base_path / "data" / f"SnakeStats{snake_no}.csv"
        with stats_path.open("w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["Top Score", "PopulationID"])
            writer.writerow([score, pop_id])

        self.brain.save_csv(base_path / "data" / f"Snake{snake_no}.csv")

    @staticmethod
    def load_snake(snake_no: int, base_path: Path) -> "Snake":
        s = Snake()
        s.brain.load_csv(base_path / "data" / f"Snake{snake_no}.csv")
        return s

    def look(self) -> None:
        dirs = [
            PVector(-GRID, 0),
            PVector(-GRID, -GRID),
            PVector(0, -GRID),
            PVector(GRID, -GRID),
            PVector(GRID, 0),
            PVector(GRID, GRID),
            PVector(0, GRID),
            PVector(-GRID, GRID),
        ]
        self.vision = [0.0] * 24
        idx = 0
        for d in dirs:
            vals = self.look_in_direction(d)
            self.vision[idx : idx + 3] = vals
            idx += 3

    def look_in_direction(self, direction: PVector) -> list[float]:
        vision_dir = [0.0, 0.0, 0.0]
        p = self.pos.copy()
        food_found = False
        tail_found = False
        distance = 0.0

        p.add(direction)
        distance += 1.0

        while not (p.x < PLAY_MIN_X or p.y < PLAY_MIN_Y or p.x >= PLAY_MAX_X or p.y >= PLAY_MAX_Y):
            if not food_found and p.x == self.food.pos.x and p.y == self.food.pos.y:
                vision_dir[0] = 1.0
                food_found = True

            if not tail_found and self.is_on_tail(p.x, p.y):
                vision_dir[1] = 1.0 / distance
                tail_found = True

            p.add(direction)
            distance += 1.0

        vision_dir[2] = 1.0 / distance
        return vision_dir
