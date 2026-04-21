import random
import config
from Snake import Snake


class Population:
    def __init__(self, size, evolution):
        self.snakes = [None for _ in range(size)]
        for i in range(len(self.snakes)):
            self.snakes[i] = Snake()
        self.bestSnake = self.snakes[0].clone()

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
            self.bestSnake = candidate.clone()
            self.bestSnakeScore = candidate.score
            self.samebest = 0
        elif candidate.score == self.bestSnakeScore and candidate.fitness > self.bestFitness:
            self.bestFitness = candidate.fitness
            self.bestSnake = candidate.clone()
            self.samebest = 0
        else:
            self.samebest += 1
            self.bestSnake = self.bestSnake.clone()

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
        elif self.samebest < 18:
            boost = 1.35
        elif self.samebest < 32:
            boost = 1.9
        elif self.samebest < 48:
            boost = 2.5
        else:
            boost = 3.1
        config.mutationRate = min(0.45, base * boost)
        if self.samebest < 10:
            self.tournamentSize = 9
        elif self.samebest < 26:
            self.tournamentSize = 7
        elif self.samebest < 44:
            self.tournamentSize = 5
        else:
            self.tournamentSize = 4

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
        if self.samebest >= 10:
            inject_count = max(self.randomInjectBase, int(len(self.snakes) * 0.02))
        if self.samebest >= 20:
            inject_count = max(inject_count, int(len(self.snakes) * 0.05))
        if self.samebest >= 34:
            inject_count = max(inject_count, int(len(self.snakes) * 0.1))
        if self.samebest >= 50:
            inject_count = max(inject_count, int(len(self.snakes) * 0.16))
        if self.samebest >= 70:
            inject_count = max(inject_count, int(len(self.snakes) * 0.24))
        if self.samebest >= 95:
            inject_count = max(inject_count, int(len(self.snakes) * 0.35))

        best_mutant_count = 0
        if self.samebest >= 12:
            best_mutant_count = max(2, int(len(self.snakes) * 0.03))
        if self.samebest >= 24:
            best_mutant_count = max(best_mutant_count, int(len(self.snakes) * 0.08))
        if self.samebest >= 40:
            best_mutant_count = max(best_mutant_count, int(len(self.snakes) * 0.14))
        if self.samebest >= 65:
            best_mutant_count = max(best_mutant_count, int(len(self.snakes) * 0.2))

        total_diversity = inject_count + best_mutant_count
        max_diversity = max(1, len(self.snakes) - elite_count)
        if total_diversity > max_diversity:
            overflow = total_diversity - max_diversity
            reduce_inject = min(overflow, inject_count)
            inject_count -= reduce_inject
            overflow -= reduce_inject
            if overflow > 0:
                best_mutant_count = max(0, best_mutant_count - overflow)

        train_until = len(self.snakes) - inject_count
        breed_until = max(elite_count, train_until - best_mutant_count)
        for i in range(elite_count, breed_until):
            if random.random() < 0.2:
                child = self.selectParent(parent_pool).clone()
            else:
                child = self.selectParent(parent_pool).crossover(self.selectParent(parent_pool))
            if self.samebest >= 12 and random.random() < 0.35:
                child.brain.mutate(min(0.65, config.mutationRate * 1.35))
            else:
                child.mutate()
            newSnakes[i] = child

        for i in range(breed_until, train_until):
            child = self.bestSnake.clone()
            child.brain.mutate(min(0.75, max(config.mutationRate * 1.8, 0.08)))
            newSnakes[i] = child

        for i in range(train_until, len(self.snakes)):
            newSnakes[i] = Snake()

        self.snakes = list(newSnakes)
        self.evolution.append(self.bestSnakeScore)
        self.gen += 1
        if self.samebest > 120:
            self.samebest = 60

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
