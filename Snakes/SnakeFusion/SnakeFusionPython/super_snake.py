import pygame

from config import GRID, PLAY_MAX_X, PLAY_MAX_Y, PLAY_MIN_X, PLAY_MIN_Y
from food import Food
from super_snake_clone import SuperSnakeClone
from vector2d import PVector


class SuperSnake:
    def __init__(self, dem_brains: list) -> None:
        self.len = 4
        x, y = 600, 200
        self.pos = PVector(x, y)
        self.vel = PVector(GRID, 0)
        self.tail_positions = [PVector(x - 30, y), PVector(x - 20, y), PVector(x - 10, y)]

        self.food = Food()
        self.brain = dem_brains
        self.clones = [None] * len(dem_brains)

        self.vision = [0.0] * 24
        self.lifetime = 0
        self.left_to_live = 500
        self.grow_count = 0
        self.alive = True

        self.brain_to_follow = 0
        self.food_found = False
        self.saw_food = False
        self.moves_to_follow = 0

    def best_decision(self) -> None:
        for i, b in enumerate(self.brain):
            c = SuperSnakeClone(self, b)
            c.run_clone()
            self.clones[i] = c

        min_seen = 1000
        clone_ate_food = -1
        for i, c in enumerate(self.clones):
            if c.food_found and c.food_seen_at_count < min_seen:
                min_seen = c.food_seen_at_count
                clone_ate_food = i

        if clone_ate_food != -1:
            self.food_found = True
            self.moves_to_follow = self.clones[clone_ate_food].move_count
            self.brain_to_follow = clone_ate_food
            return

        min_seen = 1000
        clone_seen_food = -1
        for i, c in enumerate(self.clones):
            if c.seen_food and c.food_seen_at_count < min_seen:
                min_seen = c.food_seen_at_count
                clone_seen_food = i

        if clone_seen_food != -1:
            self.saw_food = True
            self.moves_to_follow = self.clones[clone_seen_food].food_seen_at_count
            self.brain_to_follow = clone_seen_food
            return

        max_moves = 0
        clone_lasted = 0
        for i, c in enumerate(self.clones):
            if (not c.ran_out) and c.move_count > max_moves:
                max_moves = c.move_count
                clone_lasted = i

        self.brain_to_follow = clone_lasted
        self.moves_to_follow = 1

    def set_velocity(self) -> None:
        self.look()
        if self.moves_to_follow <= 0:
            self.saw_food = False
            self.food_found = False
            self.best_decision()

        outputs = self.brain[self.brain_to_follow].output(self.vision)
        direction = max(range(len(outputs)), key=outputs.__getitem__)

        if direction == 0:
            self.vel = PVector(-GRID, 0)
        elif direction == 1:
            self.vel = PVector(0, -GRID)
        elif direction == 2:
            self.vel = PVector(GRID, 0)
        else:
            self.vel = PVector(0, GRID)

    def move(self) -> None:
        self.lifetime += 1
        self.left_to_live -= 1
        self.moves_to_follow -= 1

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
            if self.len > 1:
                self.tail_positions[self.len - 2] = self.pos.copy()

        self.pos.add(self.vel)

    def eat(self) -> None:
        self.food = Food()
        while self.food.pos in self.tail_positions:
            self.food = Food()

        self.left_to_live += 100
        self.grow_count += 4
        self.moves_to_follow = 0
        self.food_found = False

    def show(self, surface: pygame.Surface) -> None:
        color = (255, 255, 255)
        if self.food_found:
            color = (0, 255, 0)
        elif self.saw_food:
            color = (0, 0, 255)

        for p in self.tail_positions:
            pygame.draw.rect(surface, color, pygame.Rect(int(p.x), int(p.y), GRID, GRID))
        pygame.draw.rect(surface, color, pygame.Rect(int(self.pos.x), int(self.pos.y), GRID, GRID))
        pygame.draw.rect(surface, (255, 0, 0), pygame.Rect(int(self.food.pos.x), int(self.food.pos.y), GRID, GRID))

    def grow(self) -> None:
        self.tail_positions.append(self.pos.copy())
        self.len += 1

    def gonna_die(self, x: float, y: float) -> bool:
        if x < PLAY_MIN_X or y < PLAY_MIN_Y or x >= PLAY_MAX_X or y >= PLAY_MAX_Y:
            return True
        return any(x == p.x and y == p.y for p in self.tail_positions)

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
        out = [0.0, 0.0, 0.0]
        p = self.pos.copy()
        food_found = False
        tail_found = False
        distance = 1.0
        p.add(direction)

        while not (p.x < PLAY_MIN_X or p.y < PLAY_MIN_Y or p.x >= PLAY_MAX_X or p.y >= PLAY_MAX_Y):
            if not food_found and p.x == self.food.pos.x and p.y == self.food.pos.y:
                out[0] = 1.0
                food_found = True
            if not tail_found and any(p.x == t.x and p.y == t.y for t in self.tail_positions):
                out[1] = 1.0 / distance
                tail_found = True
            p.add(direction)
            distance += 1.0

        out[2] = 1.0 / distance
        return out
