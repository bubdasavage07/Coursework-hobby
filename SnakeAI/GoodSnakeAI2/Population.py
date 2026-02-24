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
        self.eliteCount = max(2, int(size * 0.005))
        self.tournamentSize = max(3, min(9, int(size * 0.005)))
        self.randomInjectBase = max(1, int(size * 0.005))

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
        maxIndex = 0
        for i in range(1, len(self.snakes)):
            current = self.snakes[i]
            best = self.snakes[maxIndex]
            if current.score > best.score or (current.score == best.score and current.fitness > best.fitness):
                maxIndex = i

        candidate = self.snakes[maxIndex]
        if candidate.score > self.bestSnakeScore:
            self.bestFitness = candidate.fitness
            self.bestSnake = candidate.cloneForReplay()
            self.bestSnakeScore = candidate.score
            self.samebest = 0
        elif candidate.score == self.bestSnakeScore and candidate.fitness > self.bestFitness:
            self.bestFitness = candidate.fitness
            self.bestSnake = candidate.cloneForReplay()
            self.samebest += 1
        else:
            self.samebest += 1
            self.bestSnake = self.bestSnake.cloneForReplay()

    def selectParent(self, pool=None):
        source = self.snakes if pool is None else pool
        parent = random.choice(source)
        rounds = min(self.tournamentSize, len(source))
        for _ in range(rounds - 1):
            challenger = random.choice(source)
            if challenger.fitness > parent.fitness:
                parent = challenger
        return parent

    def adaptMutationRate(self):
        base = max(config.defaultmutation, 0.0001)
        if self.samebest < 8:
            boost = 1.0
        elif self.samebest < 16:
            boost = 1.4
        elif self.samebest < 28:
            boost = 2.0
        elif self.samebest < 40:
            boost = 2.6
        else:
            boost = 3.2
        config.mutationRate = min(0.6, base * boost)
        if self.samebest < 10:
            self.tournamentSize = 7
        elif self.samebest < 24:
            self.tournamentSize = 5
        else:
            self.tournamentSize = 3

    def naturalSelection(self):
        newSnakes = [None for _ in range(len(self.snakes))]

        self.setBestSnake()
        self.calculateFitnessSum()
        self.adaptMutationRate()

        ranked = sorted(self.snakes, key=lambda s: s.fitness, reverse=True)
        elite_count = min(self.eliteCount, len(self.snakes))
        parent_pool_size = max(2, int(len(self.snakes) * 0.2))
        parent_pool = ranked[:parent_pool_size]

        newSnakes[0] = self.bestSnake.clone()

        for i in range(1, elite_count):
            newSnakes[i] = ranked[i].clone()

        inject_count = 0
        if self.samebest >= 8:
            inject_count = max(self.randomInjectBase, int(len(self.snakes) * 0.03))
        if self.samebest >= 14:
            inject_count = max(inject_count, int(len(self.snakes) * 0.08))
        if self.samebest >= 22:
            inject_count = max(inject_count, int(len(self.snakes) * 0.16))
        if self.samebest >= 32:
            inject_count = max(inject_count, int(len(self.snakes) * 0.25))
        if self.samebest >= 45:
            inject_count = max(inject_count, int(len(self.snakes) * 0.4))
        if self.samebest >= 60:
            inject_count = max(inject_count, int(len(self.snakes) * 0.7))

        train_until = len(self.snakes) - inject_count
        for i in range(elite_count, train_until):
            if random.random() < 0.2:
                child = self.selectParent(parent_pool).clone()
            else:
                child = self.selectParent(parent_pool).crossover(self.selectParent(parent_pool))
            if self.samebest >= 12 and random.random() < 0.35:
                child.brain.mutate(min(0.75, config.mutationRate * 1.5))
            else:
                child.mutate()
            newSnakes[i] = child

        for i in range(train_until, len(self.snakes)):
            newSnakes[i] = Snake()

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
