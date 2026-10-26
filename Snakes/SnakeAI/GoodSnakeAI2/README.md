# SnakeAI

## Overview

SnakeAI is a Python/Pygame experiment that trains populations of Snake agents. The project contains neural-network, matrix, population, fitness, and mutation logic alongside an interactive visualizer.

## Educational purpose

This project is a programming and algorithmic-learning exercise. It explores how an evolutionary loop can evaluate agents, select stronger candidates, and mutate later generations. It is not presented as a production machine-learning system.

## Technologies

- Python
- Pygame for the interactive display
- CSV files for saved model data

## Run the interactive program

From this directory, create and activate a virtual environment, install Pygame, then run the entry point:

```bash
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install pygame
python3 SnakeAI.py
```

## Run the headless smoke test

The smoke test substitutes a minimal Pygame interface and exercises short training runs without opening a window:

```bash
python3 headless_smoke_test.py --gens 2 --pop-size 20 --max-steps 7000
```

## Skills demonstrated

- Object-oriented Python design
- State management and game-loop logic
- Matrix and neural-network data structures
- Fitness calculation, selection, and mutation experiments
- Basic automated smoke testing

## Known limitations

- The project has no locked dependency file; install Pygame in a local virtual environment.
- Training behavior and outcomes can vary because the program uses randomness.
- The interactive application requires a graphical environment.
