import pygame
import config
from Matrix import Matrix


class NeuralNet:
    def __init__(self, input_nodes, hidden_nodes, output_nodes, hidden_layers):
        self.iNodes = input_nodes
        self.hNodes = hidden_nodes
        self.oNodes = output_nodes
        self.hLayers = hidden_layers

        self.weights = [None for _ in range(self.hLayers + 1)]
        self.weights[0] = Matrix(self.hNodes, self.iNodes + 1)
        for i in range(1, self.hLayers):
            self.weights[i] = Matrix(self.hNodes, self.hNodes + 1)
        self.weights[len(self.weights) - 1] = Matrix(self.oNodes, self.hNodes + 1)

        for w in self.weights:
            w.randomize()

    def mutate(self, mr):
        for w in self.weights:
            w.mutate(mr)

    def output(self, inputsArr):
        inputs = self.weights[0].singleColumnMatrixFromArray(inputsArr)
        curr_bias = inputs.addBias()

        for i in range(self.hLayers):
            hidden_ip = self.weights[i].dot(curr_bias)
            hidden_op = hidden_ip.activate()
            curr_bias = hidden_op.addBias()

        output_ip = self.weights[len(self.weights) - 1].dot(curr_bias)
        output = output_ip.activate()

        return output.toArray()

    def crossover(self, partner):
        child = NeuralNet(self.iNodes, self.hNodes, self.oNodes, self.hLayers)
        for i in range(len(self.weights)):
            child.weights[i] = self.weights[i].crossover(partner.weights[i])
        return child

    def clone(self):
        clone = NeuralNet(self.iNodes, self.hNodes, self.oNodes, self.hLayers)
        for i in range(len(self.weights)):
            clone.weights[i] = self.weights[i].clone()
        return clone

    def load(self, weight):
        for i in range(len(self.weights)):
            self.weights[i] = weight[i]

    def pull(self):
        return list(self.weights)

    def show(self, surface, x, y, w, h, vision, decision, font):
        space = 5
        nSize = (h - (space * (self.iNodes - 2))) / float(self.iNodes)
        nSpace = (w - (len(self.weights) * nSize)) / float(len(self.weights))
        hBuff = (h - (space * (self.hNodes - 1)) - (nSize * self.hNodes)) / 2.0
        oBuff = (h - (space * (self.oNodes - 1)) - (nSize * self.oNodes)) / 2.0

        maxIndex = 0
        for i in range(1, len(decision)):
            if decision[i] > decision[maxIndex]:
                maxIndex = i

        lc = 0

        for i in range(self.iNodes):
            if vision[i] != 0:
                color = (0, 255, 0)
            else:
                color = (255, 255, 255)
            pygame.draw.ellipse(surface, color, (x, y + (i * (nSize + space)), nSize, nSize))
            pygame.draw.ellipse(surface, (0, 0, 0), (x, y + (i * (nSize + space)), nSize, nSize), 1)
            text_surf = font.render(str(i), True, (0, 0, 0))
            text_rect = text_surf.get_rect(center=(x + (nSize / 2), y + (nSize / 2) + (i * (nSize + space))))
            surface.blit(text_surf, text_rect)

        lc += 1

        for _ in range(self.hLayers):
            for i in range(self.hNodes):
                pygame.draw.ellipse(surface, (255, 255, 255), (x + (lc * nSize) + (lc * nSpace), y + hBuff + (i * (nSize + space)), nSize, nSize))
                pygame.draw.ellipse(surface, (0, 0, 0), (x + (lc * nSize) + (lc * nSpace), y + hBuff + (i * (nSize + space)), nSize, nSize), 1)
            lc += 1

        for i in range(self.oNodes):
            color = (0, 255, 0) if i == maxIndex else (255, 255, 255)
            pygame.draw.ellipse(surface, color, (x + (lc * nSpace) + (lc * nSize), y + oBuff + (i * (nSize + space)), nSize, nSize))
            pygame.draw.ellipse(surface, (0, 0, 0), (x + (lc * nSpace) + (lc * nSize), y + oBuff + (i * (nSize + space)), nSize, nSize), 1)

        lc = 1

        for i in range(self.weights[0].rows):
            for j in range(self.weights[0].cols - 1):
                color = (255, 0, 0) if self.weights[0].matrix[i][j] < 0 else (0, 0, 255)
                pygame.draw.line(surface, color, (x + nSize, y + (nSize / 2) + (j * (space + nSize))), (x + nSize + nSpace, y + hBuff + (nSize / 2) + (i * (space + nSize))), 1)

        lc += 1

        for a in range(1, self.hLayers):
            for i in range(self.weights[a].rows):
                for j in range(self.weights[a].cols - 1):
                    color = (255, 0, 0) if self.weights[a].matrix[i][j] < 0 else (0, 0, 255)
                    pygame.draw.line(surface, color, (x + (lc * nSize) + ((lc - 1) * nSpace), y + hBuff + (nSize / 2) + (j * (space + nSize))), (x + (lc * nSize) + (lc * nSpace), y + hBuff + (nSize / 2) + (i * (space + nSize))), 1)
            lc += 1

        for i in range(self.weights[len(self.weights) - 1].rows):
            for j in range(self.weights[len(self.weights) - 1].cols - 1):
                color = (255, 0, 0) if self.weights[len(self.weights) - 1].matrix[i][j] < 0 else (0, 0, 255)
                pygame.draw.line(surface, color, (x + (lc * nSize) + ((lc - 1) * nSpace), y + hBuff + (nSize / 2) + (j * (space + nSize))), (x + (lc * nSize) + (lc * nSpace), y + oBuff + (nSize / 2) + (i * (space + nSize))), 1)

        label_color = (0, 0, 0)
        labels = ["U", "D", "L", "R"]
        for i, lbl in enumerate(labels):
            tx = x + (lc * nSize) + (lc * nSpace) + nSize / 2
            ty = y + oBuff + (i * (space + nSize)) + (nSize / 2)
            text_surf = font.render(lbl, True, label_color)
            text_rect = text_surf.get_rect(center=(tx, ty))
            surface.blit(text_surf, text_rect)
