import random

from config import GRID, PLAY_MIN_X
from vector2d import PVector


class Food:
    def __init__(self) -> None:
        self.pos = PVector(
            PLAY_MIN_X + random.randrange(0, 40) * GRID,
            random.randrange(0, 40) * GRID,
        )

    def clone(self) -> "Food":
        clone = Food()
        clone.pos = self.pos.copy()
        return clone
