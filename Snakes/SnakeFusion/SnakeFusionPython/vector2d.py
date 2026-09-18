from dataclasses import dataclass


@dataclass(eq=True, frozen=False)
class PVector:
    x: float = 0.0
    y: float = 0.0

    def add(self, other: "PVector") -> None:
        self.x += other.x
        self.y += other.y

    def copy(self) -> "PVector":
        return PVector(self.x, self.y)
