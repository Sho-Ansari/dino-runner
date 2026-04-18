# Dino Runner

A Chrome-style dinosaur endless runner game built with Python and Pygame.

## Features

- Jump and duck mechanics
- Cactus and bird (pterodactyl) obstacles
- Progressive difficulty (speed ramps up with score)
- Day / night cycle
- High score tracking per session
- Animated dino legs and flapping birds

## Controls

| Key            | Action          |
| -------------- | --------------- |
| Space / Up     | Jump / Start / Restart |
| Down           | Duck            |
| Esc            | Quit            |

## Install

```bash
pip install -r requirements.txt
```

## Run

2D version (pygame):

```bash
py game.py
```

3D version (Ursina / Panda3D) — Subway-Surfers style with lanes:

```bash
py game3d.py
```

### 3D Controls

| Key                  | Action            |
| -------------------- | ----------------- |
| Space / Up           | Jump / Start / Restart |
| A / Left             | Move lane left    |
| D / Right            | Move lane right   |
| Esc                  | Quit              |

## Requirements

- Python 3.10+ (tested on 3.14)
- `pygame-ce` (2D version)
- `ursina` + Panda3D (3D version — ~200 MB install)
