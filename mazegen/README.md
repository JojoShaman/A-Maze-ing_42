_This project has been created as part of the 42 curriculum by srosu, njunaidi._

# mazegen

A small, dependency-free maze generator, reusable in other projects. Builds mazes with DFS or Prim's algorithm, renders them with ANSI colors, exports them (plain text or hexadecimal), and can be played interactively.

## Installation

```bash
python -m build                       # produces dist/mazegen-1.0.0-py3-none-any.whl
pip install dist/mazegen-1.0.0-py3-none-any.whl
```

Requires Python 3.10+. No external runtime dependencies.

## Basic usage

The generator is configured from a text file. `Parsing` reads it; the resulting object is passed to `MazeGenerator`.

```python
from mazegen import Parsing, MazeGenerator, save

config = Parsing()
config.parse("config.txt")

maze = MazeGenerator(config)
maze.generate()      # carves the grid, applies imperfection, computes the path,
                      # and automatically writes the hexadecimal grid to OUTPUT_FILE

save(maze)            # optional: also write the plain-text render to OUTPUT_FILE
```

`generate()` writes the hexadecimal export itself every time it runs (including
regenerations), so `OUTPUT_FILE` is always in sync with the maze currently in
memory. Calling `hex(maze)` (see below) by hand is only needed to re-save on
demand — e.g. after changing something without calling `generate()` again.

### Configuration file format

One `KEY=VALUE` pair per line (blank lines and `#` comments ignored, keys are
case-insensitive):

```
WIDTH=15
HEIGHT=15
ENTRY=0,0
EXIT=14,14
OUTPUT_FILE=maze.txt
PERFECT=True
ALGORITHM=dfs
SEED=42
```

| Key                | Meaning                                                 |
| ------------------ | ------------------------------------------------------- |
| `WIDTH` / `HEIGHT` | grid size                                               |
| `ENTRY` / `EXIT`   | `x,y` coordinates, must lie inside the grid, and differ |
| `OUTPUT_FILE`      | default output filename                                 |
| `PERFECT`          | `True` = single path, `False` = loops allowed           |
| `ALGORITHM`        | `dfs` or `prim`                                         |
| `SEED`             | optional, for a reproducible maze                       |

`parse()` collects every invalid value instead of stopping at the first one, and raises a single `Exception` listing them all.

The "42" pattern is 7 columns by 5 rows, so it only fits — without entry/exit
colliding with it — once the maze is **strictly larger than 7×5** (8×6 or
above). At 7×5 or smaller, `MazeGenerator` skips the pattern and prints a
message on the console, but the maze itself still generates normally.

## Accessing the maze

`generate()` builds `maze.grid`, a `list[list[Cell]]` of size `height`×`width`, and stores the BFS shortest path in `maze._path` (a `list[tuple[int, int]]`):

```python
cell = maze.grid[y][x]
cell.walls        # {'W': bool, 'S': bool, 'E': bool, 'N': bool}
cell.static        # part of the "42" pattern?
cell.get_binary()  # e.g. '1010' -> one bit per wall

print(maze._path)                          # [(0, 0), (0, 1), (1, 1), ...]
x, y = maze._path[0]
nx, ny = maze._path[1]
maze.get_direction(x, y, nx, ny)           # 'N', 'E', 'S' or 'W'
```

`maze.entry`, `maze.exit`, `maze.width`, `maze.height` give the maze boundaries.

## Rendering, saving, playing

```python
from mazegen import render, display, save, hex, game

render(maze)              # colors the grid with the active theme
print(display(maze))      # visual representation as a string

save(maze)                # plain-text rendering -> maze.output_file
hex(maze)                 # re-write the hex grid + entry/exit + path directions

game.play(maze)           # interactive play with the arrow keys
```

`render()` flags: `ansi=0` for no color codes (used by `save()`), `update=True` skips the path animation. `hex()` takes an `auto_save: bool = True` flag: when `True` (the default, and what `generate()` uses internally) it writes silently; pass `auto_save=False` to also print the "file saved" confirmation, e.g. after a manual save triggered from a menu. `maze._g_mode` sets the difficulty (`'easy'` allows backtracking, `'hard'` doesn't and ends the game if no move is left).

## Themes & menu

```python
maze._mode = 1   # pick a theme (0-4) from mazegen.colors.THEMES before rendering
render(maze)

from mazegen import menu
menu.user(maze, show="Show path", animation="Enable", is_perfect="perfect")
```

`colors.THEMES` holds `[wall, background, entry, exit]` ANSI sets plus the raw color constants. `menu` provides pure display functions (`show_themes`, `algo`, `game_mode`, `user`) for building a CLI on top of the package — call `user()` again after each state change to refresh its labels.

## Public API

| Symbol          | Description                                                |
| --------------- | ---------------------------------------------------------- |
| `Parsing`       | reads and validates the configuration file                 |
| `MazeGenerator` | builds the grid, carves it, and computes the solved path   |
| `render()`      | applies ANSI colors and wall/path characters to the grid   |
| `display()`     | returns the current maze as a printable string             |
| `save()`        | writes the plain-text rendering to a file                  |
| `hex()`         | writes the hexadecimal grid, entry/exit and path to a file |
| `game`          | interactive play mode (`game.play(maze)`)                  |
| `menu`          | printable CLI screens (theme, algorithm, mode, main menu)  |
| `Cell`, `Pixel` | grid cell and rendering-pixel data structures              |
| `colors`        | `THEMES` and individual ANSI color constants               |
