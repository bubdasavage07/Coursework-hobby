import random
import config
from Snake import Snake


class Population:
    def __init__(self, size, evolution):
        self.snakes = [None for _ in range(size)]
        for i in range(len(self.snakes)):
            self.snakes[i] = Snake()
        self.bestSnake = self.snakes[0].clone()
        self.bestSnake.replay = True

        self.bestSnakeScore = 0
        self.gen = 0
        self.samebest = 0

        self.bestFitness = 0.0
        self.fitnessSum = 0.0
        self.evolution = evolution

    def done(self):
        for i in range(len(self.snakes)):
            if not self.snakes[i].dead:
                return False
        if not self.bestSnake.dead:
            return False
        return True

    def update(self):
        if not self.bestSnake.dead:
            self.bestSnake.look()
            self.bestSnake.think()
            self.bestSnake.move()
        for i in range(len(self.snakes)):
            if not self.snakes[i].dead:
                self.snakes[i].look()
                self.snakes[i].think()
                self.snakes[i].move()

    def show(self, surface, font):
        if config.replayBest:
            self.bestSnake.show(surface)
            self.bestSnake.brain.show(surface, 0, 0, 360, 790, self.bestSnake.vision, self.bestSnake.decision, font)
        else:
            for i in range(len(self.snakes)):
                self.snakes[i].show(surface)

    def setBestSnake(self):
        maxFit = 0
        maxIndex = 0
        for i in range(len(self.snakes)):
            if self.snakes[i].fitness > maxFit:
                maxFit = self.snakes[i].fitness
                maxIndex = i
        if maxFit > self.bestFitness:
            self.bestFitness = maxFit
            self.bestSnake = self.snakes[maxIndex].cloneForReplay()
            self.bestSnakeScore = self.snakes[maxIndex].score
        else:
            self.bestSnake = self.bestSnake.cloneForReplay()

    def selectParent(self):
        rand = random.random() * self.fitnessSum
        summation = 0
        for i in range(len(self.snakes)):
            summation += self.snakes[i].fitness
            if summation > rand:
                return self.snakes[i]
        return self.snakes[0]

    def naturalSelection(self):
        newSnakes = [None for _ in range(len(self.snakes))]

        self.setBestSnake()
        self.calculateFitnessSum()

        newSnakes[0] = self.bestSnake.clone()
        for i in range(1, len(self.snakes)):
            child = self.selectParent().crossover(self.selectParent())
            child.mutate()
            newSnakes[i] = child
        self.snakes = list(newSnakes)
        self.evolution.append(self.bestSnakeScore)
        self.gen += 1

    def mutate(self):
        for i in range(1, len(self.snakes)):
            self.snakes[i].mutate()

    def calculateFitness(self):
        for i in range(len(self.snakes)):
            self.snakes[i].calculateFitness()

    def calculateFitnessSum(self):
        self.fitnessSum = 0
        for i in range(len(self.snakes)):
            self.fitnessSum += self.snakes[i].fitness
