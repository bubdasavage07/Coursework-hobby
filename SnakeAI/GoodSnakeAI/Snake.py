import math
import pygame
import config
from vec2 import Vec2
from Food import Food
from NeuralNet import NeuralNet


class Snake:
    def __init__(self, layers=None):
        if layers is None:
            layers = config.hidden_layers

        self.score = 1
        self.lifeLeft = 200
        self.lifetime = 0
        self.xVel = 0
        self.yVel = 0
        self.foodItterate = 0

        self.fitness = 0.0

        self.dead = False
        self.replay = False

        self.vision = None
        self.decision = None

        self.head = Vec2(800, config.HEIGHT / 2)

        self.body = []
        self.foodList = None

        self.food = Food()
        self.brain = None

        if not config.humanPlaying:
            self.vision = [0.0 for _ in range(24)]
            self.decision = [0.0 for _ in range(4)]
            self.foodList = []
            self.foodList.append(self.food.clone())
            self.brain = NeuralNet(24, config.hidden_nodes, 4, layers)
            self.body.append(Vec2(800, (config.HEIGHT / 2) + config.SIZE))
            self.body.append(Vec2(800, (config.HEIGHT / 2) + (2 * config.SIZE)))
            self.score += 2

    @classmethod
    def from_foods(cls, foods):
        s = cls.__new__(cls)
        s.score = 1
        s.lifeLeft = 200
        s.lifetime = 0
        s.xVel = 0
        s.yVel = 0
        s.foodItterate = 0
        s.fitness = 0.0
        s.dead = False
        s.replay = True
        s.vision = [0.0 for _ in range(24)]
        s.decision = [0.0 for _ in range(4)]
        s.head = Vec2(800, config.HEIGHT / 2)
        s.body = []
        s.foodList = []
        for f in foods:
            s.foodList.append(f.clone())
        s.food = s.foodList[s.foodItterate]
        s.foodItterate += 1
        s.brain = None
        s.body.append(Vec2(800, (config.HEIGHT / 2) + config.SIZE))
        s.body.append(Vec2(800, (config.HEIGHT / 2) + (2 * config.SIZE)))
        s.score += 2
        return s

    def bodyCollide(self, x, y):
        for i in range(len(self.body)):
            if x == self.body[i].x and y == self.body[i].y:
                return True
        return False

    def foodCollide(self, x, y):
        return x == self.food.pos.x and y == self.food.pos.y

    def wallCollide(self, x, y):
        if x >= config.WIDTH - config.SIZE or x < config.BOARD_X or y >= config.HEIGHT - config.SIZE or y < config.BOARD_Y:
            return True
        return False

    def show(self, surface):
        self.food.show(surface)
        for i in range(len(self.body)):
            pygame.draw.rect(surface, (255, 255, 255), (self.body[i].x, self.body[i].y, config.SIZE, config.SIZE))
            pygame.draw.rect(surface, (0, 0, 0), (self.body[i].x, self.body[i].y, config.SIZE, config.SIZE), 1)
        color = (150, 150, 150) if self.dead else (255, 255, 255)
        pygame.draw.rect(surface, color, (self.head.x, self.head.y, config.SIZE, config.SIZE))
        pygame.draw.rect(surface, (0, 0, 0), (self.head.x, self.head.y, config.SIZE, config.SIZE), 1)

    def move(self):
        if not self.dead:
            if not config.humanPlaying and not config.modelLoaded:
                self.lifetime += 1
                self.lifeLeft -= 1
            if self.foodCollide(self.head.x, self.head.y):
                self.eat()
            self.shiftBody()
            if self.wallCollide(self.head.x, self.head.y):
                self.dead = True
            elif self.bodyCollide(self.head.x, self.head.y):
                self.dead = True
            elif (len(self.body) + 1) >= (config.GRID_W * config.GRID_H):
                # Grid fully occupied by the snake.
                self.dead = True
            elif self.lifeLeft <= 0 and not config.humanPlaying:
                self.dead = True

    def eat(self):
        length = len(self.body) - 1
        self.score += 1
        if not config.humanPlaying and not config.modelLoaded:
            if self.lifeLeft < 500:
                if self.lifeLeft > 400:
                    self.lifeLeft = 500
                else:
                    self.lifeLeft += 100
        if length >= 0:
            self.body.append(Vec2(self.body[length].x, self.body[length].y))
        else:
            self.body.append(Vec2(self.head.x, self.head.y))
        if not self.replay:
            self.food = Food()
            while self.bodyCollide(self.food.pos.x, self.food.pos.y):
                self.food = Food()
            if not config.humanPlaying:
                self.foodList.append(self.food)
        else:
            if self.foodItterate < len(self.foodList):
                self.food = self.foodList[self.foodItterate]
                self.foodItterate += 1
            else:
                # If replay runs out of recorded food, continue with fresh spawns.
                self.food = Food()
                while self.bodyCollide(self.food.pos.x, self.food.pos.y):
                    self.food = Food()
                self.foodList.append(self.food)
                self.foodItterate += 1

    def shiftBody(self):
        tempx = self.head.x
        tempy = self.head.y
        self.head.x += self.xVel
        self.head.y += self.yVel
        for i in range(len(self.body)):
            temp2x = self.body[i].x
            temp2y = self.body[i].y
            self.body[i].x = tempx
            self.body[i].y = tempy
            tempx = temp2x
            tempy = temp2y

    def cloneForReplay(self):
        clone = Snake.from_foods(self.foodList)
        clone.brain = self.brain.clone()
        return clone

    def clone(self):
        clone = Snake(config.hidden_layers)
        clone.brain = self.brain.clone()
        return clone

    def crossover(self, parent):
        child = Snake(config.hidden_layers)
        child.brain = self.brain.crossover(parent.brain)
        return child

    def mutate(self):
        self.brain.mutate(config.mutationRate)

    def calculateFitness(self):
        if self.score < 10:
            self.fitness = math.floor(self.lifetime * self.lifetime) * pow(2, self.score)
        else:
            self.fitness = math.floor(self.lifetime * self.lifetime)
            self.fitness *= pow(2, 10)
            self.fitness *= (self.score - 9)

    def look(self):
        self.vision = [0.0 for _ in range(24)]
        temp = self.lookInDirection(Vec2(-config.SIZE, 0))
        self.vision[0] = temp[0]
        self.vision[1] = temp[1]
        self.vision[2] = temp[2]
        temp = self.lookInDirection(Vec2(-config.SIZE, -config.SIZE))
        self.vision[3] = temp[0]
        self.vision[4] = temp[1]
        self.vision[5] = temp[2]
        temp = self.lookInDirection(Vec2(0, -config.SIZE))
        self.vision[6] = temp[0]
        self.vision[7] = temp[1]
        self.vision[8] = temp[2]
        temp = self.lookInDirection(Vec2(config.SIZE, -config.SIZE))
        self.vision[9] = temp[0]
        self.vision[10] = temp[1]
        self.vision[11] = temp[2]
        temp = self.lookInDirection(Vec2(config.SIZE, 0))
        self.vision[12] = temp[0]
        self.vision[13] = temp[1]
        self.vision[14] = temp[2]
        temp = self.lookInDirection(Vec2(config.SIZE, config.SIZE))
        self.vision[15] = temp[0]
        self.vision[16] = temp[1]
        self.vision[17] = temp[2]
        temp = self.lookInDirection(Vec2(0, config.SIZE))
        self.vision[18] = temp[0]
        self.vision[19] = temp[1]
        self.vision[20] = temp[2]
        temp = self.lookInDirection(Vec2(-config.SIZE, config.SIZE))
        self.vision[21] = temp[0]
        self.vision[22] = temp[1]
        self.vision[23] = temp[2]

    def lookInDirection(self, direction):
        look = [0.0, 0.0, 0.0]
        pos = Vec2(self.head.x, self.head.y)
        distance = 0
        foodFound = False
        bodyFound = False
        pos.add(direction)
        distance += 1
        while not self.wallCollide(pos.x, pos.y):
            if (not foodFound) and self.foodCollide(pos.x, pos.y):
                foodFound = True
                look[0] = 1
            if (not bodyFound) and self.bodyCollide(pos.x, pos.y):
                bodyFound = True
                look[1] = 1
            pos.add(direction)
            distance += 1
        look[2] = 1.0 / distance
        return look

    def think(self):
        self.decision = self.brain.output(self.vision)
        maxIndex = 0
        maxVal = 0
        for i in range(len(self.decision)):
            if self.decision[i] > maxVal:
                maxVal = self.decision[i]
                maxIndex = i

        if maxIndex == 0:
            self.moveUp()
        elif maxIndex == 1:
            self.moveDown()
        elif maxIndex == 2:
            self.moveLeft()
        elif maxIndex == 3:
            self.moveRight()

    def moveUp(self):
        if self.yVel != config.SIZE:
            self.xVel = 0
            self.yVel = -config.SIZE

    def moveDown(self):
        if self.yVel != -config.SIZE:
            self.xVel = 0
            self.yVel = config.SIZE

    def moveLeft(self):
        if self.xVel != config.SIZE:
            self.xVel = -config.SIZE
            self.yVel = 0

    def moveRight(self):
        if self.xVel != -config.SIZE:
            self.xVel = config.SIZE
            self.yVel = 0
