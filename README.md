_This project has been created as part of the 42 curriculum by srosu, njunaidi._

# A-Maze-ing

## Description

**A-Maze-ing** is a configurable maze generator written in Python 3.10+.

From a configuration file, the program generates a maze — either **perfect**
(one unique path) or the default **imperfect** mode (a Pac-Man-playable board:
full connectivity, open corners/center, at least two independent routes, rare
dead-ends) — draws a **"42"** pattern in the center (when the maze is large
enough for it), finds the **shortest path** with BFS, renders it in the
terminal with ANSI colors through an interactive menu, exports it (plain text
or hexadecimal), and can be played as a mini-game.

The generation logic lives in a standalone, pip-installable package
(`mazegen`) so it can be reused by future projects.

## Instructions

### Requirements

- Python **3.10+**, no external runtime dependencies (`flake8`/`mypy` for
  linting only)
- A **Unix-like terminal** (uses ANSI escapes and `termios`)

### Makefile

```sh
make venv          # create a virtual environment
make install        # install dev tools
make run            # run with config.txt
make lint           # flake8 + mypy
make lint-strict    # flake8 + mypy --strict
make debug          # run under pdb
make clean          # remove caches
```

### Run manually

```sh
python3 a_maze_ing.py config.txt
```

Any error (missing file, bad syntax, impossible parameters, …) is reported
with a clear message instead of crashing.

### Interactive menu

```
ENTER  generate a new maze
0      choose the algorithm (dfs / prim)
1      show / hide the solution path
2      change the color theme
3      change the wall character
4      save the rendered maze
5      save the maze in hexadecimal
6      play (easy / hard, arrow keys, q to give up)
7      toggle the generation animation
8      toggle perfect / imperfect maze (imperfect by default)
q      quit
```

## Configuration file format

One `KEY=VALUE` pair per line; lines starting with `#` are ignored.

```
WIDTH=20            # columns
HEIGHT=15           # rows
ENTRY=0,0           # x,y — must be inside the maze
EXIT=19,14          # x,y — must differ from ENTRY
OUTPUT_FILE=maze.txt
PERFECT=False       # True: unique path, False: Pac-Man-style board
ALGORITHM=dfs       # dfs or prim
#SEED=12            # optional, for reproducible mazes
```

All keys are mandatory except `SEED`. The parser validates every value and
reports **all** the errors found at once, not just the first one.

The "42" pattern itself is exactly 7 columns by 5 rows, so it only fits with
room to spare — without entry/exit colliding with it — once the maze is
**strictly larger than 7×5** (8×6 or above). At 7×5 or smaller, the pattern is
skipped and a message is printed on the console, but the maze is still
generated normally.

## Output file format

One hexadecimal digit per cell, one bit per closed wall:

| Bit (weight) | Direction |
| ------------ | --------- |
| 0 → 1        | North     |
| 1 → 2        | East      |
| 2 → 4        | South     |
| 3 → 8        | West      |

Cells are written row by row. After an empty line, three more lines follow:
entry coordinates, exit coordinates, and the shortest path as `N`/`E`/`S`/`W`.
This file is written automatically every time a maze is generated (including
regenerations), not just on the first run.

## Maze generation algorithm

- **DFS (recursive backtracker), our main algorithm:** carves forward into a
  random unvisited neighbor, backtracking with a stack when stuck. Simple,
  produces long winding corridors, and naturally yields a perfect maze.
- **Prim's algorithm:** grows the maze from a frontier list instead of a
  single path, producing bushier mazes with more short branches — a
  different texture for comparison.
- **BFS**, used to **solve** the maze: explores level by level with a queue,
  guaranteeing the shortest path — the one used everywhere (path display,
  hexadecimal export, the mini-game).

## Reusable code

The `mazegen/` package is fully decoupled from the menu and the terminal UI:

- `Parsing` — generic `KEY=VALUE` config reader with error accumulation.
- `MazeGenerator` — builds and carves the grid, computes the BFS path.
- `render()` / `display()` — turn a grid into an ANSI or plain string.
- `save()` / `hex()` — export helpers.
- `game`, `Cell`, `Pixel`, `colors` — mini-game, data structures, themes.

```python
from mazegen import Parsing, MazeGenerator, save

config = Parsing()
config.parse("config.txt")
maze = MazeGenerator(config)
maze.generate()
save(maze)
```

See [`mazegen/README.md`](mazegen/README.md) for the full API. Build with
`python -m build` → `mazegen-1.0.0-py3-none-any.whl`.

## License

The repository includes a `LICENSE.md` (**MIT License**), covering the whole
project including `mazegen`. MIT was picked because it explicitly allows
reuse, modification and redistribution with only the copyright notice kept —
exactly what the subject requires for a package meant to be reused by later
projects.

## Team & project management

| Member       | Responsibilities                                                                       |
| ------------ | -------------------------------------------------------------------------------------- |
| **srosu**    | `a_maze_ing.py`, `generator.py` (DFS/Prim/BFS, "42" pattern), `game.py`, `renderer.py` |
| **njunaidi** | `cell.py`, `colors.py`, `menu.py`, `parsing.py`, `exporter.py`                         |

- **Planning:** parsing → DFS generation → rendering → BFS/exports → bonuses
  (themes, animation, mini-game, Prim). Rendering took longer than planned and
  was redesigned around a 3×3 pixel matrix per cell; Prim and the mini-game
  came in the final week.
- **What worked well:** splitting generation from rendering early made it easy
  to bolt on Prim, themes and the mini-game later without touching the core.
- **What could be improved:** the subject changed about a week before our
  first evaluation, and we only discovered it _during_ the evaluation —
  `LICENSE.md` had become mandatory, and "imperfect" now meant a full
  Pac-Man-style board, not just extra loops. Both were quick fixes once
  spotted, but re-reading the subject in full closer to the deadline would
  have caught them sooner.
- **Tools:** Git/GitHub, Make, flake8, mypy, Claude AI (see below).

## Resources

- Maze generation algorithms, DFS, BFS — Wikipedia
- Recursive backtracker & Prim's algorithm — Jamis Buck's blog
- ANSI escape codes reference and cheat sheet
- `termios` / `tty` docs (raw keyboard input)
- `setuptools` / `build` docs (packaging)
- MIT License text — opensource.org

**AI usage:** Claude AI was used as a learning/debugging assistant — explaining
DFS/Prim/BFS and `termios` raw mode before implementation, helping debug
specific issues, reviewing code style, and helping structure this README. All
suggestions were read, understood and adapted by us; no code was copy-pasted
blindly.
