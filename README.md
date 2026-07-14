# A-Maze_ing

## **Description**

### **1) Introduction** 
A-maze_ing is a maze generator project. In which the maze is generated in the terminal. There are two types of mazes that can be generated it's either a perfect one or an imperfect one. 

### **2) Perfect and imperfect maze**
The perfect maze has only 1 path from the entry to the exit and the imperfect one has multiple paths (they are created by breaking the walls down).

### **3) Rendering**
It can be exported as a plain text rendering or in a compact hexadecimal format, where each cell is encoded as one hex digit representing its four walls, followed
by the entry/exit coordinates and the solution path as cardinal moves.

### **4) What does it do ?**
The project has an interactive menu that allows you to regenerate the
maze, switch between two generation algorithms, show the solution path,
change the color theme and the wall character, watch the generation
live, export the maze, and even play it as a mini-game with the arrow
keys. Check them out in the "How to use the interactive menu" section.

### **5) The algos: DFS vs prim :**

#### 5.1) DFS (recursive backtracker)

DFS (Depth-First Search) starts at the entry cell and carves the maze by
always going as deep as possible. At each step, it picks a random
unvisited neighbor, knocks down the wall between the two cells and moves
into it. When the current cell has no unvisited neighbor left (dead
end), the algorithm backtracks using a stack until it finds a cell that
still has unvisited neighbors, and carves again from there. The
generation is complete when the stack is empty, meaning every cell has
been visited. Because it always digs forward before backtracking, DFS
produces mazes with long, winding corridors and few but long dead ends.

#### 5.2) Prim

Prim's algorithm grows the maze from a single random cell instead of
following one path. It keeps a list of "frontier" cells: the unvisited
neighbors of the maze built so far. At each step, it picks a random cell
from the frontier, connects it to one of its already-visited neighbors
by knocking down the wall between them, then adds its own unvisited
neighbors to the frontier. The maze is complete when the frontier is
empty. Because the maze grows from many points at once, Prim produces
bushy mazes with lots of short branches and many small dead ends.

#### 5.3) BFS


## The code explanation:

### **1) Project structure and quick description of each file**

```
a_maze_ing.py        entry point and interactive menu loop
config.txt           example configuration file
Makefile             shortcuts to run, lint, debug and clean the project
pyproject.toml       package configuration (setuptools)
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
### **2) A closer look at the interesting files**

Most files are self-explanatory, but a few deserve a more detailed
explanation.

#### 2.1) generator.py

This is the heart of the project. The `MazeGenerator` class stores the
grid (a 2D list of `Cell` objects) and everything happens by knocking
down walls between two neighboring cells (`knock_wall()`). The
generation itself is done either by `_dfs()` (a stack-based recursive
backtracker) or `_prim()` (a frontier-based growth algorithm). Once the
maze is generated, `_bfs()` finds the shortest path between the entry
and the exit: it explores the maze level by level using a queue, records
where each cell was reached from in a `came_from` dictionary, then walks
backwards from the exit to rebuild the path. The file also handles the
"42" pattern: before generation, the cells forming the pattern are
marked as `static` so the algorithms treat them as unbreakable blocks.

#### 2.2) renderer.py

Rendering works at two levels. Each cell owns a 3x3 matrix of `Pixel`
objects (corners, walls, center). `render()` fills these pixels
depending on which walls are up: the wall state of a cell is converted
to a 4-bit binary number (one bit per wall) and each bit decides whether
a pixel is a wall block or a floor. `display()` then stitches all the
matrices together into one big string, skipping the rows and columns
shared between neighboring cells so the walls are not drawn twice. The
colors are ANSI escape codes injected around the characters, and the
same functions can render without colors (for the text export).

#### 2.3) game.py

The mini-game needs to read the arrow keys instantly, without the user
pressing Enter. To do that, it switches the terminal to "raw mode" with
`tty.setraw()` and reads the input byte by byte: an arrow key arrives as
the escape character `\x1b` followed by two characters (e.g. `[A` for
up). Before exiting, the original terminal settings saved with
`termios.tcgetattr()` are always restored in a `finally` block,
otherwise the terminal would stay in raw mode after the program ends.
The game loop checks the walls of the current cell to decide if a move
is legal, tracks the visited path, and detects the win (reaching the
exit) or, in hard mode, the game over (no legal move left).

#### 2.4) parsing.py

Instead of stopping at the first invalid value, the parser collects all
the errors it finds in a list while reading the configuration file, and
only raises at the end with the full list. This way the user sees
everything that is wrong with their file in one run instead of fixing
errors one by one.

### 2.5) config.txt: 

The whole program is driven by this configuration file, passed as the
only command-line argument. It uses a simple KEY=VALUE format:
 
```
WIDTH=35            # number of columns (min 7)
HEIGHT=20           # number of rows (min 5)
ENTRY=0,0           # entry coordinates x,y
EXIT=34,19          # exit coordinates x,y
OUTPUT_FILE=maze.txt
PERFECT=True        # True: unique solution, False: loops allowed
ALGORITHM=dfs       # dfs or prim
#SEED=12            # optional, for reproducible mazes
```
 
Lines starting with `#` are ignored.
 
> [!NOTE]
> The entry and exit must be inside the maze and must not overlap the
> central "42" pattern.



## **Instructions**

### **1) How to use the makefile ?**

```bash
make venv          # create a virtual environment
make install       # install dev tools (flake8, mypy)
make run           # run the program with config.txt
make lint          # run flake8 and mypy
make debug         # run under pdb
make clean         # remove cache files
```


### **2) How to use the interactive menu ?**
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

### **3) command python3 -m build ***

//Construit ton package 

## **Resources**
 
General tools used throughout the project: Google, YouTube and Claude AI
(research, explanations and debugging help).
 
### **1) Algorithms (DFS, BFS, Prim)**
 
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

### **2) ANSI codes and ASCII animations**
 
- ANSI escape codes (reference):
  https://en.wikipedia.org/wiki/ANSI_escape_code
- ANSI escape codes cheat sheet (colors, cursor movement, screen control):
  https://gist.github.com/fnky/458719343aabd01cfb17a3a4f7296797
- Build your own command line with ANSI escape codes (cursor control,
  arrow keys, animations):
  https://www.lihaoyi.com/post/BuildyourownCommandLinewithANSIescapecodes.html
- Terminal animations in Python (ASCII animation basics):
  https://medium.com/@joloiuy/creating-captivating-terminal-animations-in-python-a-fun-and-interactive-guide-2eeb2a6b25ec

### **3) Python standard library**
 
- os (system calls, clearing the screen):
  https://docs.python.org/3/library/os.html
- termios (POSIX terminal control, raw keyboard input):
  https://docs.python.org/3/library/termios.html
- tty (terminal control helper functions):
  https://docs.python.org/3/library/tty.html
- collections.deque (BFS queue):
  https://docs.python.org/3/library/collections.html#collections.deque

### **4)Packaging and code quality**
 
- setuptools (build backend used in pyproject.toml):
  https://setuptools.pypa.io/en/latest/
- PEP 8, Style Guide for Python Code:
  https://peps.python.org/pep-0008/
- mypy documentation (static type checking):
  https://mypy.readthedocs.io/
