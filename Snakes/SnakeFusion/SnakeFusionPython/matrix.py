import math
import random


class Matrix:
    def __init__(self, rows: int, cols: int, matrix: list[list[float]] | None = None) -> None:
        self.rows = rows
        self.cols = cols
        self.matrix = matrix if matrix is not None else [[0.0 for _ in range(cols)] for _ in range(rows)]

    @classmethod
    def from_2d(cls, m: list[list[float]]) -> "Matrix":
        rows = len(m)
        cols = len(m[0]) if m else 0
        return cls(rows, cols, [row[:] for row in m])

    def dot(self, n: "Matrix") -> "Matrix":
        result = Matrix(self.rows, n.cols)
        if self.cols != n.rows:
            return result
        for i in range(self.rows):
            for j in range(n.cols):
                total = 0.0
                for k in range(self.cols):
                    total += self.matrix[i][k] * n.matrix[k][j]
                result.matrix[i][j] = total
        return result

    def randomize(self) -> None:
        for i in range(self.rows):
            for j in range(self.cols):
                self.matrix[i][j] = random.uniform(-1, 1)

    @staticmethod
    def single_column_matrix_from_array(arr: list[float]) -> "Matrix":
        out = Matrix(len(arr), 1)
        for i, val in enumerate(arr):
            out.matrix[i][0] = val
        return out

    def from_array(self, arr: list[float]) -> None:
        for i in range(self.rows):
            for j in range(self.cols):
                self.matrix[i][j] = arr[j + i * self.cols]

    def to_array(self) -> list[float]:
        arr = [0.0] * (self.rows * self.cols)
        for i in range(self.rows):
            for j in range(self.cols):
                arr[j + i * self.cols] = self.matrix[i][j]
        return arr

    def add_bias(self) -> "Matrix":
        out = Matrix(self.rows + 1, 1)
        for i in range(self.rows):
            out.matrix[i][0] = self.matrix[i][0]
        out.matrix[self.rows][0] = 1.0
        return out

    def activate(self) -> "Matrix":
        out = Matrix(self.rows, self.cols)
        for i in range(self.rows):
            for j in range(self.cols):
                out.matrix[i][j] = 1.0 / (1.0 + math.exp(-self.matrix[i][j]))
        return out

    def mutate(self, mutation_rate: float) -> None:
        for i in range(self.rows):
            for j in range(self.cols):
                if random.random() < mutation_rate:
                    self.matrix[i][j] += random.gauss(0, 1) / 5.0
                    self.matrix[i][j] = max(-1.0, min(1.0, self.matrix[i][j]))

    def crossover(self, partner: "Matrix") -> "Matrix":
        child = Matrix(self.rows, self.cols)
        rand_c = random.randrange(self.cols)
        rand_r = random.randrange(self.rows)
        for i in range(self.rows):
            for j in range(self.cols):
                if (i < rand_r) or (i == rand_r and j <= rand_c):
                    child.matrix[i][j] = self.matrix[i][j]
                else:
                    child.matrix[i][j] = partner.matrix[i][j]
        return child

    def clone(self) -> "Matrix":
        return Matrix.from_2d(self.matrix)
