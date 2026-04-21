SIZE = 20
hidden_nodes = 16
hidden_layers = 2
fps = 240

WIDTH = 1200
HEIGHT = 800
PANEL_W = 400
BOARD_X = PANEL_W + SIZE
BOARD_Y = SIZE
BOARD_W = WIDTH - PANEL_W - 40
BOARD_H = HEIGHT - 40
GRID_W = BOARD_W // SIZE
GRID_H = BOARD_H // SIZE

mutationRate = 0.05
defaultmutation = mutationRate

humanPlaying = False
replayBest = True
seeVision = False
modelLoaded = False
