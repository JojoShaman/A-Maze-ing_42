*This project has been created as part of the 42 curriculum by srosu, njunaidi.*

# A-Maze-ing

## 1. Description

A-Maze-ing is a maze generator project in which the maze is generated in
the terminal. The **goal** of the project is to generate random mazes
from a configuration file, solve them, render them with ANSI colors, and
export them to a file — while writing clean, fully type-annotated Python
code organized as a reusable package.

There are two types of mazes that can be generated: either a **perfect**
one or an **imperfect** one. The perfect maze has only one path from the
entry to the exit. The imperfect one has multiple paths, created by
knocking down extra walls after generation, which creates loops. Every
maze embeds a **"42" pattern** in its center.

### 1.1 Features

The project has an interactive menu that allows you to regenerate the
maze, switch between two generation algorithms, show the solution path,
change the color theme and the wall character, watch the generation
live, export the maze (plain text or hexadecimal), and even play it as a
mini-game with the arrow keys.

### 1.2 The algorithms

#### 1.2.1 DFS (recursive backtracker) — our main generation algorithm

DFS (Depth-First Search) starts at the entry cell and carves the maze by
always going as deep as possible. At each step, it picks a random
unvisited neighbor, knocks down the wall between the two cells and moves
into it. When the current cell has no unvisited neighbor left (dead
end), the algorithm **backtracks** using a **stack** until it finds a
cell that still has unvisited neighbors, and carves again from there.
The generation is complete when the stack is empty, meaning every cell
has been visited.

**Why we use DFS:**

- **Simplicity**: the whole algorithm holds in a few lines with a single
  stack — easy to implement, easy to debug, easy to explain.
- **Maze quality**: because it always digs forward before backtracking,
  DFS produces mazes with long, winding corridors and few but long dead
  ends, which are the most fun to look at and to play.
- **Guaranteed perfection**: DFS naturally produces a perfect maze
  (every cell reachable, no loops), which is the default required by the
  subject. Imperfect mazes are then obtained by knocking down extra
  walls afterwards.

#### 1.2.2 Prim's algorithm

Prim's algorithm grows the maze from a single random cell instead of
following one path. It keeps a list of **"frontier" cells**: the
unvisited neighbors of the maze built so far. At each step, it picks a
random cell from the frontier, connects it to one of its
already-visited neighbors by knocking down the wall between them, then
adds its own unvisited neighbors to the frontier. The maze is complete
when the frontier is empty. Because the maze grows from many points at
once, Prim produces **bushy mazes** with lots of short branches and many
small dead ends.

**Why we use Prim:**

- **Variety**: Prim produces a completely different maze "texture" than
  DFS — bushy with many short branches instead of long corridors. Having
  both lets the user compare two classic generation strategies. In
  short: DFS digs one long tunnel and backtracks, Prim grows outward
  like a crystal.
- **Guaranteed perfection too**: like DFS, Prim connects every cell
  exactly once, so it also produces a perfect maze by construction.
- **Different data structure**: implementing it was a good exercise —
  same `knock_wall()` building block as DFS, but driven by a frontier
  list instead of a stack, which shows how the choice of data structure
  shapes the result.

#### 1.2.3 BFS (maze solving)

Unlike DFS and Prim which generate the maze, **BFS (Breadth-First
Search) is used to solve it**. It explores the maze like a wave
spreading from the entry: first all the cells at distance 1, then all
the cells at distance 2, and so on, using a **queue** (first in, first
out). Every time a cell is discovered, the algorithm records which cell
it was reached from in a dictionary. When the wave reaches the exit, the
path is rebuilt by walking backwards through that dictionary, from the
exit to the entry.

**Why we use BFS:**

- **Shortest path guaranteed**: because the wave advances level by level
  in every direction at once, the first time it reaches the exit is
  necessarily through the **shortest path**. A DFS-based solver would
  find *a* path, but not necessarily the shortest one — this matters for
  imperfect mazes, which have several possible paths.
- **Simplicity**: BFS only needs a queue (`collections.deque`), a
  visited set and a dictionary — no weights, no heuristics. Since all
  moves in the maze have the same cost, more complex algorithms like
  Dijkstra or A* would bring nothing here.
- **Used everywhere in the program**: the path found by BFS is the one
  displayed by the "show path" option, exported in the hexadecimal
  format, and recomputed after each game.

### 1.3 Configuration file

The whole program is driven by a configuration file, passed as the only
command-line argument. It uses a simple **KEY=VALUE** format, one
parameter per line:

```
WIDTH=20            # number of columns (integer, min 7)
HEIGHT=15           # number of rows (integer, min 5)
ENTRY=0,0           # entry coordinates x,y (inside the maze)
EXIT=19,14          # exit coordinates x,y (inside the maze)
OUTPUT_FILE=maze.txt   # file used by the save options
PERFECT=True        # True: unique solution, False: loops allowed
ALGORITHM=dfs       # generation algorithm: dfs or prim
#SEED=12            # optional, integer, for reproducible mazes
```

Rules:

- Lines starting with `#` are ignored (comments).
- All keys are **mandatory** except `SEED`, which is optional.
- The **entry and exit** must be inside the maze and must not overlap
  the central "42" pattern.
- The parser validates every value and reports **all the errors found in
  the file at once**, instead of stopping at the first one.

### 1.4 Project structure

```
a_maze_ing.py        entry point and interactive menu loop
config.txt           example configuration file
Makefile             shortcuts to run, lint, debug and clean the project
pyproject.toml       p
mazegen/             the maze generation package
├── __init__.py      exposes the public functions and classes of the package
├── parsing.py       reads and validates the configuration file
├── cell.py          defines a Cell (4 walls, position) and a Pixel
│                    (smallest rendering unit)
├── generator.py     the core: MazeGenerator class with DFS and Prim
│                    generation, BFS path solving and the "42" pattern
├── renderer.py      turns the grid into a colored ANSI string
│                    (each cell is rendered as a 3x3 pixel matrix)
├── menu.py          prints the different menu screens
├── exporter.py      saves the maze to a file (text or hexadecimal)
├── game.py          the mini-game: reads arrow keys in raw terminal
│                    mode and moves the player through the maze
└── colors.py        ANSI color codes and the 5 color themes
```

### 1.5 A closer look at the important files

Most files are self-explanatory, but a few deserve a more detailed
explanation.

#### 1.5.1 generator.py

This is the **heart of the project**. The `MazeGenerator` class stores
the grid (a 2D list of `Cell` objects) and everything happens by
knocking down walls between two neighboring cells (`knock_wall()`). The
generation itself is done either by `_dfs()`  or `_prim()` (a frontier-based growth algorithm). Once the
maze is generated, `_bfs()` finds the shortest path between the entry
and the exit: it explores the maze level by level using a queue, records
where each cell was reached from in a `came_from` dictionary, then walks
backwards from the exit to rebuild the path. The file also handles the
**"42" pattern**: before generation, the cells forming the pattern are
marked as `static` so the algorithms treat them as unbreakable blocks.

#### 1.5.2 renderer.py

Rendering works at two levels. Each cell owns a **3x3 matrix of `Pixel`
objects** (corners, walls, center). `render()` fills these pixels
depending on which walls are up: the wall state of a cell is converted
to a **4-bit binary number** (one bit per wall) and each bit decides
whether a pixel is a wall block or a floor. `display()` then stitches
all the matrices together into one big string, skipping the rows and
columns shared between neighboring cells so the walls are not drawn
twice. The colors are ANSI escape codes injected around the characters,
and the same functions can render without colors (for the text export).
This same binary representation is what the hexadecimal export writes to
the file, one hex digit per cell.

#### 1.5.3 game.py

The mini-game needs to read the arrow keys **instantly, without the user
pressing Enter**. To do that, it switches the terminal to "raw mode"
with `tty.setraw()` and reads the input byte by byte: an arrow key
arrives as the escape character `\x1b` followed by two characters (e.g.
`[A` for up). Before exiting, the original terminal settings saved with
`termios.tcgetattr()` are always restored in a `finally` block,
otherwise the terminal would stay in raw mode after the program ends.
The game loop checks the walls of the current cell to decide if a move
is legal, tracks the visited path, and detects the win (reaching the
exit) or, in hard mode, the game over (no legal move left).

#### 1.5.4 parsing.py

Instead of stopping at the first invalid value, the parser **collects
all the errors** it finds in a list while reading the configuration
file, and only raises at the end with the full list. This way the user
sees everything that is wrong with their file in one run instead of
fixing errors one by one.

#### 1.5.5 exporter.py

#### 1.5.5 exporter.py

This file handles the two save options of the menu. `save()` writes the
maze as plain text, exactly as it appears on screen (walls, entry, exit
and the path if it is displayed), without any color codes.
`save_hex()` writes the same maze as data instead: the walls of every
cell as hex digits, the entry and exit coordinates, and the solution
path as cardinal moves. Both write to the file given by `OUTPUT_FILE`
in the configuration.

### 1.6 Reusable code

The project is built as an **installable Python package** (`mazegen`),
so its components can be reused in other projects:

- **`MazeGenerator`** (`generator.py`) is fully independent from the
  menu and the rendering: any program can import it, generate a maze
  from a config object, and read the resulting grid of `Cell` objects.
  For example, a GUI or a web app could use it as its maze engine.
- **`Parsing`** (`parsing.py`) is a generic KEY=VALUE config parser with
  error accumulation, easy to adapt to any project that reads a
  configuration file.
- **The BFS solver** (`_bfs()`) works on any grid of cells with walls —
  it could solve mazes coming from another generator.
- **`colors.py`** is a standalone collection of ANSI codes and themes,
  reusable by any terminal program.

Once built (see [section 2.3 "How to build the
package"](#23-how-to-build-the-package)), the package can
be installed with pip and
imported like any library:

```python
from mazegen import MazeGenerator, Parsing

config = Parsing()
config.parse("config.txt")
maze = MazeGenerator(config)
maze.generate()
```

## 2. Instructions

### 2.1 How to run the program

```bash
python3 a_maze_ing.py my_config.txt
```

**Warning**: the rendering and the game rely on ANSI escape codes and
termios: a **Unix-like terminal** (Linux/macOS) is required.

### 2.2 How to use the Makefile

```bash
make venv          # create a virtual environment
make install       # install dev tools (flake8, mypy)
make run           # run the program with config.txt
make lint          # run flake8 and mypy
make lint-strict   # run flake8 and mypy in strict mode
make debug         # run under pdb
make clean         # remove cache files
```

### 2.3 How to build the package

The project is packaged with **setuptools** (see `pyproject.toml`). To
build the distribution files:

```bash
pip install build          # install the build tool
python -m build            # build the package
```

This creates a `dist/` folder containing a source archive (`.tar.gz`)
and a wheel (`.whl`). The package can then be installed with:

```bash
pip install dist/mazegen-1.0.0-py3-none-any.whl
```

### 2.4 How to use the interactive menu

```
ENTER   generate a new maze
0       choose the generation algorithm (dfs / prim)
1       show / hide the solution path
2       change the color theme
3       change the wall character
4       save the rendered maze to the output file
5       save the maze in hexadecimal format
6       play the maze (easy / hard mode, arrow keys, q to give up)
7       toggle the generation animation
q       quit
```

## 3. Team and project management

### 3.1 Roles

- **srosu**: architecture and core engine — `a_maze_ing.py` (entry point
  and interactive menu loop), `generator.py` (grid handling, DFS and
  Prim generation, BFS solving, "42" pattern), `game.py` (the arrow-key
  mini-game) and `renderer.py`. He designed how the different modules
  fit together and wrote most of the program logic.

- **nameen**: presentation and configuration layer — `cell.py` (the
  `Cell` and `Pixel` data structures), `colors.py` and the color themes,
  `menu.py` (menu screens), `parsing.py` (configuration file reading and
  validation) and `exporter.py` (text and hexadecimal exports).

Both members reviewed each other's code before merging

### 3.2 Planning and how it evolved

Our initial plan was: (1) parsing and data structures, (2) DFS
generation, (3) rendering, (4) BFS solving and exports, (5) bonus
features (themes, animation, mini-game, Prim).

In practice, the plan evolved: the rendering took longer than expected
and was redesigned mid-project around a 3x3 pixel matrix per cell, which
simplified both the path drawing and the mini-game display. Prim's
algorithm and the mini-game were added in the final week once the core
was stable.

### 3.3 Tools used

- **Git / GitHub** for version control and collaboration (feature
  branches, merges)
- **Make** for automating run, lint and clean tasks
- **flake8 and mypy** for style and static type checking
- **Google, YouTube and Claude AI** for research and help (see section
  4.1 for details on AI usage)

## 4. Resources

### 4.1 How AI was used

We used **Claude AI** (Anthropic) as a learning and debugging assistant,
not as a code generator. Concretely, it was used for:

- **Understanding concepts**: explanations of the DFS, Prim and BFS
  algorithms before implementing them ourselves, and of the `termios` /
  `tty` raw terminal mode used by the mini-game.
- **Debugging help**: identifying the cause of specific bugs (parsing
  edge cases, rendering glitches) — the fixes were then written and
  applied by us.
- **Code review**: spotting PEP 8 issues, unused code and error-handling
  weaknesses before submission.
- **Documentation**: help structuring and proofreading this README.

The algorithms, the architecture and the code itself were written by the
team; AI answers were always read, understood and adapted, never
copy-pasted blindly.

### 4.2 Algorithms (DFS, BFS, Prim)

- Maze generation algorithms (overview):
  https://en.wikipedia.org/wiki/Maze_generation_algorithm
- Maze generation with recursive backtracking / DFS (Jamis Buck):
  https://weblog.jamisbuck.org/2010/12/27/maze-generation-recursive-backtracking
- Maze generation with Prim's algorithm (Jamis Buck):
  https://weblog.jamisbuck.org/2011/1/10/maze-generation-prim-s-algorithm
- Depth-First Search:
  https://en.wikipedia.org/wiki/Depth-first_search
- Breadth-First Search (shortest path solving):
  https://en.wikipedia.org/wiki/Breadth-first_search

### 4.3 ANSI codes and ASCII animations

- ANSI escape codes (reference):
  https://en.wikipedia.org/wiki/ANSI_escape_code
- ANSI escape codes cheat sheet (colors, cursor movement, screen control):
  https://gist.github.com/fnky/458719343aabd01cfb17a3a4f7296797
- Build your own command line with ANSI escape codes (cursor control,
  arrow keys, animations):
  https://www.lihaoyi.com/post/BuildyourownCommandLinewithANSIescapecodes.html
- Terminal animations in Python (ASCII animation basics):
  https://medium.com/@joloiuy/creating-captivating-terminal-animations-in-python-a-fun-and-interactive-guide-2eeb2a6b25ec

### 4.4 Python standard library

- os (system calls, clearing the screen):
  https://docs.python.org/3/library/os.html
- termios (POSIX terminal control, raw keyboard input):
  https://docs.python.org/3/library/termios.html
- tty (terminal control helper functions):
  https://docs.python.org/3/library/tty.html
- collections.deque (BFS queue):
  https://docs.python.org/3/library/collections.html#collections.deque

### 4.5 Packaging and code quality

- setuptools (build backend used in pyproject.toml):
  https://setuptools.pypa.io/en/latest/
- build (PyPA build frontend):
  https://build.pypa.io/en/stable/
- PEP 8, Style Guide for Python Code:
  https://peps.python.org/pep-0008/
- mypy documentation (static type checking):
  https://mypy.readthedocs.io/