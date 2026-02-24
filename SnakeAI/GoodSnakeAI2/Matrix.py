import random
import math


class Matrix:
    def __init__(self, r, c=None):
        if c is None:
            m = r
            self.matrix = m
            self.rows = len(self.matrix)
            self.cols = len(self.matrix[0])
        else:
            self.rows = r
            self.cols = c
            self.matrix = [[0.0 for _ in range(self.cols)] for _ in range(self.rows)]

    def dot(self, n):
        result = Matrix(self.rows, n.cols)
        if self.cols == n.rows:
            for i in range(self.rows):
                for j in range(n.cols):
                    s = 0.0
                    for k in range(self.cols):
                        s += self.matrix[i][k] * n.matrix[k][j]
                    result.matrix[i][j] = s
        return result

    def randomize(self):
        for i in range(self.rows):
            for j in range(self.cols):
                self.matrix[i][j] = random.uniform(-1, 1)

    def singleColumnMatrixFromArray(self, arr):
        n = Matrix(len(arr), 1)
        for i in range(len(arr)):
            n.matrix[i][0] = arr[i]
        return n

    def toArray(self):
        arr = [0.0 for _ in range(self.rows * self.cols)]
        for i in range(self.rows):
            for j in range(self.cols):
                arr[j + i * self.cols] = self.matrix[i][j]
        return arr

    def addBias(self):
        n = Matrix(self.rows + 1, 1)
        for i in range(self.rows):
            n.matrix[i][0] = self.matrix[i][0]
        n.matrix[self.rows][0] = 1
        return n

    def activate(self):
        n = Matrix(self.rows, self.cols)
        for i in range(self.rows):
            for j in range(self.cols):
                n.matrix[i][j] = self.leaky_relu(self.matrix[i][j])
        return n

    def relu(self, x):
        return max(0, x)

    def leaky_relu(self, x):
        return x if x > 0 else 0.01 * x

    def mutate(self, mutationRate):
        for i in range(self.rows):
            for j in range(self.cols):
                rand = random.random()
                if rand < mutationRate:
                    self.matrix[i][j] += random.gauss(0, 1) / 5
                    if self.matrix[i][j] > 1:
                        self.matrix[i][j] = 1
                    if self.matrix[i][j] < -1:
                        self.matrix[i][j] = -1

    def crossover(self, partner):
        child = Matrix(self.rows, self.cols)
        randC = math.floor(random.random() * self.cols)
        randR = math.floor(random.random() * self.rows)
        for i in range(self.rows):
            for j in range(self.cols):
                if (i < randR) or (i == randR and j <= randC):
                    child.matrix[i][j] = self.matrix[i][j]
                else:
                    child.matrix[i][j] = partner.matrix[i][j]
        return child

    def clone(self):
        clone = Matrix(self.rows, self.cols)
        for i in range(self.rows):
            for j in range(self.cols):
                clone.matrix[i][j] = self.matrix[i][j]
        return clone
