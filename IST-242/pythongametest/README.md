# Pygame Game Coursework

## Overview

This folder contains an IST-242 Pygame course project. The scripts implement a small interactive game with player movement, mouse-directed projectiles, enemies, collision handling, game-state logic, image assets, and audio.

## Technologies

- Python
- Pygame
- Image and WAV audio assets stored in `resources/`

## Run

From this directory:

```bash
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install -r requirements.txt
python3 game.py
```

`newgame.py` is a related alternate version of the coursework.

## Skills demonstrated

- Event-driven programming
- Pygame game-loop structure
- Sprite/image and audio loading
- Collision and state management
- Use of local relative paths for project assets

## Known limitations

- This is course work and remains intentionally close to its assignment structure.
- A graphical display and working audio device are required for normal play.
- The game depends on the included assets remaining in their existing relative locations.
