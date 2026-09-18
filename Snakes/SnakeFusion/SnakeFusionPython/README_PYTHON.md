# SnakeFusion Python Copy

This folder is a Python port of the original Processing (`.pde`) SnakeFusion project.

## Run

```bash
cd /Users/ethan/CyberSecurity_classes/SnakeFusion/SnakeFusionPython
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python3 main.py
```

## Important change

- Super-snake frame saving is disabled by default.
- Toggle is in `world.py` as `self.save_super_frames = False`.
