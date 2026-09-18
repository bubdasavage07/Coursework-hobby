from collections import deque

from config import GRID, PLAY_MAX_X, PLAY_MAX_Y, PLAY_MIN_X, PLAY_MIN_Y
from vector2d import PVector


class SuperSnakeClone:
    def __init__(self, original, chosen_brain) -> None:
        self.len = original.len
        self.pos = original.pos.copy()
        self.tail_positions = [p.copy() for p in original.tail_positions]
        self.vel = original.vel.copy()
        self.food = original.food.clone()
        self.brain = chosen_brain.clone()

        self.vision = [0.0] * 24
        self.left_to_live = original.left_to_live
        self.move_count = 0
        self.alive = True
        self.food_found = False
        self.trapped = False
        self.seen_food = False
        self.food_seen_at_count = 300
        self.ran_out = False
        self.grow_count = original.grow_count

    def run_clone(self) -> None:
        for _ in range(500):
            self.look()
            self.set_velocity()
            self.move()
            if not self.alive or self.food_found or self.trapped:
                return
        self.ran_out = True

    def set_velocity(self) -> None:
        outputs = self.brain.output(self.vision)
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
        self.move_count += 1
        self.left_to_live -= 1

        if self.left_to_live < 0:
            self.alive = False
            return

        nx = self.pos.x + self.vel.x
        ny = self.pos.y + self.vel.y

        if self.gonna_die(nx, ny):
            self.alive = False
            return

        if self.is_trapped():
            self.trapped = True
            return

        if nx == self.food.pos.x and ny == self.food.pos.y:
            self.food_found = True
            return

        if self.grow_count > 0:
            self.grow_count -= 1
            self.grow()
        else:
            for i in range(len(self.tail_positions) - 1):
                self.tail_positions[i] = self.tail_positions[i + 1].copy()
            if self.len > 1:
                self.tail_positions[self.len - 2] = self.pos.copy()

        self.pos.add(self.vel)

        if not self.seen_food and self.see_food():
            self.seen_food = True
            self.food_seen_at_count = self.move_count

    def grow(self) -> None:
        self.tail_positions.append(self.pos.copy())
        self.len += 1

    def see_food(self) -> bool:
        for d in [PVector(-GRID, 0), PVector(GRID, 0), PVector(0, -GRID), PVector(0, GRID)]:
            p = self.pos.copy()
            p.add(d)
            while not self.gonna_die(p.x, p.y):
                if p.x == self.food.pos.x and p.y == self.food.pos.y:
                    return True
                p.add(d)
        return False

    def gonna_die(self, x: float, y: float) -> bool:
        if x < PLAY_MIN_X or y < PLAY_MIN_Y or x >= PLAY_MAX_X or y >= PLAY_MAX_Y:
            return True
        return any(x == p.x and y == p.y for p in self.tail_positions)

    def is_trapped(self) -> bool:
        limit = min((1600 - len(self.tail_positions)) // 2, 300)
        q = deque([(self.pos.x, self.pos.y)])
        seen = {(self.pos.x, self.pos.y)}
        blanks = set()

        while q and len(blanks) <= limit:
            x, y = q.popleft()
            for dx, dy in ((GRID, 0), (-GRID, 0), (0, GRID), (0, -GRID)):
                nx, ny = x + dx, y + dy
                if (nx, ny) in seen:
                    continue
                seen.add((nx, ny))
                if self.gonna_die(nx, ny):
                    continue
                blanks.add((nx, ny))
                q.append((nx, ny))

        return len(blanks) <= limit

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
