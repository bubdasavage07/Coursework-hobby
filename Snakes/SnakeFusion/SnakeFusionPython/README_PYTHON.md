# SnakeFusion Python

## Overview

This folder is a Python port of the original Processing (`.pde`) SnakeFusion project. It simulates Snake agents with neural-network and evolutionary-programming components, then provides interactive options for viewing agents, loading saved legends, and attempting snake fusion.

## Technologies

- Python
- Pygame
- CSV files for stored snake and statistics data

## Setup and run

Run these commands from this directory:

```bash
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install -r requirements.txt
python3 main.py
```

## Controls

| Key | Action |
| --- | --- |
| `Space` | Toggle drawing all snakes. |
| `+` / `-` | Increase or decrease simulation speed. |
| `F` | Start snake fusion. |
| `0`–`4` | Play a saved legend snake. |
| `H` / `D` | Halve or double the mutation rate. |
| `L` | Toggle legend-snake training. |

## Skills demonstrated

- Modular Python design across game, world, population, and neural-network components
- Pygame event loops and rendering
- Vector and matrix operations
- Evolutionary selection and mutation logic
- Local CSV data persistence

## Known limitations

- The application requires a graphical environment.
- Training behavior varies because the simulation uses randomness.
- Saved CSV model data is part of the project state; moving or renaming it can affect legend loading.
- Super-snake frame saving is disabled by default through `self.save_super_frames = False` in `world.py`.
