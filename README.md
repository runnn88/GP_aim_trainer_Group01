# Aim Trainer (Pygame)

A reflex-training mini game built with `pygame`.

Players click fruit targets as quickly as possible before they time out. The game tracks score, combo, misses, accuracy, and reaction-time metrics, then stores results in a local SQLite database.

## Features

- State-based game flow:
  - Start Menu
  - Playing
  - Pause
  - Results
  - Settings
  - Instruction
  - History Statistics
- Fixed-timestep style update loop using `dt`
- Random target spawning inside valid screen bounds
- Fruit targets (procedurally drawn):
  - orange, apple, watermelon, coconut, peach, plum, lemon, kiwi, grape
- Hit effects:
  - fruit-colored juice splash particle animation on successful hit
  - hit sound effect (`pop.ogg`)
- Music system:
  - different BGM for menu vs gameplay
  - live volume slider in Settings
- Scoring system:
  - base points + reaction bonus
  - combo multiplier for consecutive hits
  - miss-click penalty
- Combo system:
  - increases on consecutive hits
  - resets on miss
- Difficulty options in Settings:
  - target size
  - TTL difficulty
  - spawn delay between targets
  - optional difficulty progression over time
- Persistent results storage with SQLite (`aim_trainer.db`)
- History screen with top records and best stats shown on main menu

## Game Rules

- You have a fixed duration to score as high as possible.
- Click fruit targets before they expire.
- A miss-click (clicking outside the target) increases misses and applies a score penalty.
- A timeout miss also increases misses and queues the next target.

## Controls

### Start Menu
- `Left Click`:
  - `Start` -> start game
  - `Settings` -> open settings
  - `Instruction` -> show instructions
  - `History Statistic` -> show top records
  - `Exit` -> close game

### Playing
- `Left Click` target -> hit target
- `Left Click` outside target -> miss-click penalty
- `ESC` or click pause (`||`) -> pause

### Pause
- `ENTER` or `ESC` -> resume
- `Left Click`:
  - `Continue` -> resume
  - `Main menu` -> return to menu

### Results
- `ENTER` -> return to main menu
- `ESC` -> quit

### Settings
- `Left Click` options to change values
- Volume uses a drag slider (or click the bar)
- `ESC` or `Back` -> return to main menu

## Settings Overview

- Difficulty Progression: `Off` / `On`
  - When ON, difficulty increases by game quarter (4 phases total).
- Game Duration: `30s`, `60s`, `90s`
- Target Size: `Default`, `Easy`, `Hard`
- Difficulty (TTL): `Default`, `Easy`, `Hard`
- Delay (between targets): `None`, `100ms`, `250ms`
- Volume: `0%` to `100%` via slider

## Scoring Details

Per hit:
- base score = `100`
- reaction bonus up to `50` (faster click -> higher bonus)
- combo multiplier scales with streak and is capped

Miss behavior:
- miss-click: miss count + score penalty
- timeout miss: miss count + score penalty

## Persistence and History

Game results are stored in local SQLite database:
- file: `aim_trainer.db`
- table: `GAME_STATS`

Stored fields include:
- play date
- score
- accuracy
- average reaction time
- hits
- misses
- max combo

Main menu displays best score and highest combo from database records.

## Requirements

- Python `3.10+` recommended
- `pygame>=2.5.0`

## How to Run

From project root (`GP_aim_trainer_Group01`):

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python main.py
```

## Project Structure

```text
GP_aim_trainer_Group01/
  main.py
  config.py
  requirements.txt
  pop.ogg
  aim_trainer.db
  assets/music/
  game/
    game.py
    database.py
    state_machine.py
    target.py
    aim_trainer.sql
    states/
  ui/
    button.py
    hud.py
    effects.py
```

## Asset Credits

- Hit sound: `pop.ogg` (project asset)
- Background music: Pixabay (menu + gameplay tracks)
- Font: `LuckiestGuy-Regular.ttf`

---


