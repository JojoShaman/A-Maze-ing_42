from random import choice, randint, random, seed
from .colors import END, RED
from collections import deque
from time import sleep
from os import system
from . import Parsing
from .cell import Cell, Pixel


class MazeGenerator:
    """Store the maze data and generate the maze.

    Attributes:
        width: number of columns in the maze.
        height: number of rows in the maze.
        entry: coordinates of the maze entry point.
        exit: coordinates of the maze exit point.
        output_file: path to the output file.
        perfect: whether the maze has a unique path between entry and exit.
        algorithm: generation algorithm ('dfs' or 'prim').
        seed: optional seed for reproducible generation.
        grid: 2D grid of Cell reprenting the maze.
        _path: path between entry and exit.
        _show: whether the path displaying is active.
        _wall: wall character of the maze.
        _animation: whether the generation animation is active.
        _mode: index of the current theme in THEMES.
        _g_mode: current state of the game mode ('easy' or 'hard').
        _pattern42: 42 pattern position in the maze.
    """
    def __init__(self, config: Parsing) -> None:
        self.width: int = config._width
        self.height: int = config._height
        self.entry: tuple[int, int] = config._entry
        self.exit: tuple[int, int] = config._exit
        self.output_file: str = config._output_file
        self.perfect: bool = config._perfect
        self.algorithm: str = config._algorithm
        self.seed: int = config._seed
        self.grid: list[list[Cell]] = []
        self._path: list[tuple[int, int]] = []
        self._show: bool = False
        self._wall: str = '█'
        self._animation: bool = False
        self._mode: int = 0
        self._g_mode: str = 'easy'
        self._pattern42: list[tuple[int, int]] = [
            (0, 0), (0, 1), (0, 2), (1, 2), (2, 2),
            (2, 3), (2, 4),  # 4
            (4, 0), (5, 0), (6, 0), (6, 1), (6, 2),
            (5, 2), (4, 2), (4, 3), (4, 4), (5, 4), (6, 4)  # 2
        ]

    def get_neighbors(self,
                      x: int, y: int, status: str) -> list[tuple[int, int]]:
        """Return a tuple with visited or unvisited neighbors.

        Args:
            x: column of the current cell.
            y: row of the current cell.
            status: filter for neighbor type, either 'visited' or 'unvisited'.
        Returns:
            list[tuple[int, int]]: list of neighbors visited or unvisited.
        """
        nb: list[tuple[int, int]] = []
        cell = self.grid
        neighbors = [(x, y-1), (x+1, y), (x, y+1), (x-1, y)]
        for nx, ny in neighbors:
            if ((nx >= 0 and nx < self.width) and
                    (ny >= 0 and ny < self.height)):
                if status == 'visited':
                    if cell[ny][nx].visited and not cell[ny][nx].static:
                        nb.append((nx, ny))
                elif status == 'unvisited':
                    if not cell[ny][nx].visited and not cell[ny][nx].static:
                        nb.append((nx, ny))
        return nb

    def init_grid(self) -> None:
        """Initialize the 2D grid of Cell objects with their coordinates
        and 3x3 Pixel matrix for rendering.
        """
        self.grid = [
            [Cell() for _ in range(self.width)] for _ in range(self.height)]
        for pos_y, row in enumerate(self.grid):
            for pos_x, cell in enumerate(row):
                cell.x = pos_x
                cell.y = pos_y
                cell.matrix = [[Pixel() for _ in range(3)] for _ in range(3)]

    def get_direction(self, x: int, y: int, nx: int, ny: int) -> str:
        """Return string with the cardinal direction of the neighbor's cell.

        Args:
            x: column of the current cell.
            y: row of the current cell.
            nx: column of the neighbor's cell.
            ny: row of the neighbor's cell.
        Returns:
            str: cardinal direction indicator ('W', 'S', 'E', 'N').
        """
        direction: str = ''
        if nx > x:
            direction = 'E'
        elif nx < x:
            direction = 'W'
        elif ny > y:
            direction = 'S'
        elif ny < y:
            direction = 'N'
        return direction

    def knock_wall(self, x: int, y: int, nx: int, ny: int) -> None:
        """Knock down wall between two cells.

        Args:
            x: column of the current cell.
            y: row of the current cell.
            nx: column of the neighbor's cell.
            ny: row of the neighbor's cell.
        """
        opposite: dict[str, str] = {'E': 'W', 'W': 'E', 'N': 'S', 'S': 'N'}
        direction: str = self.get_direction(x, y, nx, ny)
        self.grid[y][x].walls[direction] = False
        self.grid[ny][nx].walls[opposite[direction]] = False

    def generate(self) -> None:
        """Run the selected generation algorithm, apply imperfection
        if needed, compute the BFS path and render."""
        from . import render
        if self.seed:
            seed(self.seed)
        if self.algorithm == 'dfs':
            self._dfs()
        else:
            self._prim()
        if not self.perfect:
            self.make_imperfect()
        self._path = []
        self._bfs(self.entry, self.exit)
        render(maze=self)

    def init_static(self) -> None:
        """Initialize each cell of the 42 pattern to static."""
        cell = self.grid
        offset_x = (self.width - 7) // 2
        offset_y = (self.height - 5) // 2
        for rel_x, rel_y in self._pattern42:
            tx: int = offset_x + rel_x
            ty: int = offset_y + rel_y
            if (tx == self.entry[0] and ty == self.entry[1] or
                    tx == self.exit[0] and ty == self.exit[1]):
                raise Exception(
                    f'{RED}Entry & Exit must not be in 42 position{END}')
            cell[ty][tx].static = True
            cell[ty][tx].visited = True

    def _animate(self) -> None:
        """Animate the generation of the maze."""
        from . import render, display
        print('\033[H', end='')
        render(maze=self)
        print(display(self))
        sleep(0.001)

    def make_imperfect(self) -> None:
        """Randomly knock down additional walls to create loops
        and multiple paths in the maze."""
        s_e: dict[str, str] = {'E': 'EAST', 'S': 'SOUTH'}
        row = self.grid
        for column in row:
            for cell in column:
                x, y = cell.x, cell.y
                for wall, neighbour in s_e.items():
                    if cell.walls[wall] and not cell.static:
                        nx, ny = cell.neighbors()[neighbour]
                        if (nx >= 0 and nx < self.width and
                            ny >= 0 and ny < self.height and
                                not row[ny][nx].static):
                            if random() < 0.15:
                                self.knock_wall(x, y, nx, ny)

    def _dfs(self) -> None:
        """Generate the maze using Depth-First Search, carving
        paths by recursively visiting unvisited neighbors."""
        self.init_grid()
        self.init_static()
        stack: list[tuple[int, int]] = []
        stack.append(self.entry)
        cell = self.grid
        cell[self.entry[1]][self.entry[0]].visited = True
        while stack:
            x, y = stack[-1]
            neighbors = self.get_neighbors(x, y, 'unvisited')
            if neighbors:
                n = choice(neighbors)
                self.knock_wall(x, y, n[0], n[1])
                cell[n[1]][n[0]].visited = True
                stack.append(n)

            else:
                stack.pop()
            if self._animation:
                self._animate()
        system('clear')

    def _prim(self) -> None:
        """Generate the maze using Prim's algorithm, growing
        the maze from a random cell by expanding frontiers."""
        self.init_grid() # Initialize the grid (all cells with walls, unvisited).
        self.init_static() # Initialize static cells (fixed cells, not modifiable).
        frontiers: list[tuple[int, int]] = []  # Cells adjacent to visited cells, but not yet visited themselves.
        cell = self.grid # Alias for maze grid.
        while True: # Loop until a valid non-static starting cell is found.
            x = randint(0, self.width - 1) # Random x coordinate.
            y = randint(0, self.height - 1) # Random y coordinate.
            if cell[y][x].static: # If the cell is static, discard it and retry.
                continue
            break # Valid starting cell found, exit the loop.
        cell[y][x].visited = True # Mark the starting cell as visited.
        frontiers.extend(self.get_neighbors(x, y, 'unvisited')) # Add starting cell's unvisited neighbors as initial frontiers.
        while frontiers: # While there are frontier cells left to process.
            n = choice(frontiers) # Randomly pick a frontier cell to expand next.
            frontiers.remove(n) # Remove it from the list since it's about to be processed.
            v = choice(self.get_neighbors(n[0], n[1], 'visited')) # Randomly pick one of its already-visited neighbors to connect to.
            self.knock_wall(n[0], n[1], v[0], v[1]) # Break the wall between the frontier cell and its chosen visited neighbor.
            cell[n[1]][n[0]].visited = True # Mark the frontier cell as visited, it now belongs to the maze.
            frontiers.extend(
                [c for c in self.get_neighbors(n[0], n[1], 'unvisited') if
                 c not in frontiers]) # Add the newly visited cell's unvisited neighbors to frontiers, avoiding duplicates.
            if self._animation: # If animation mode is enabled.
                self._animate() # Display the current generation step.
        system('clear') # Clear the terminal once generation is complete.

    def _bfs(self, entry: tuple[int, int], exit: tuple[int, int]) -> None:
        """Find the path in the maze between entry and exit.

        Args:
            entry: coordinate of the entry point.
            exit: coordinate of the exit point.
        """
        opposite: dict[str, str] = {
            'E': 'W', 'W': 'E', 'N': 'S', 'S': 'N'} # Opposite direction helper.
        cell = self.grid # Alias for maze grid.
        x: int = 0
        y: int = 0
        visited: set[tuple[int, int]] = set() # Set for visited cell in order to avoid infinite loops.
        came_from: dict[tuple[int, int], tuple[int, int]] = {} # Dict containing a cell and it's previous one.
        queue: deque[tuple[int, int]] = deque() # cells to visit next, in discovery order.
        visited.add(entry)
        queue.append(entry)
        came_from[entry] = entry
        while queue: # While there are cells remaining in the queue, we iterate.
            x, y = queue.popleft() # Unpacking the first object in the queue in order to obtain x, y positions.
            if (x, y) == exit: # Condition to break the loop if we're in exit position.
                break
            neighbours = [(x, y-1), (x+1, y), (x, y+1), (x-1, y)] # The four adjacent cells: North, East, South, West.
            for nx, ny in neighbours: # Unpack the position of the neighbor in each iteration.
                if (nx >= 0 and nx < self.width and
                        ny >= 0 and ny < self.height): # Checking if the neighbor is withing grid bounds.
                    if (nx, ny) not in visited:
                        direction: str = self.get_direction(x, y, nx, ny) # If the neighbor hasn't been visited, get its direction from the current cell.
                        if not cell[y][x].walls[direction]: # With this condition we check if the wall between both cells is open.
                            queue.append((nx, ny)) # if the wall is open we append the neighbor's position at the end of the queue.
                            came_from[(nx, ny)] = (x, y) # Here we attribute the provenance of the neighbor.
                            visited.add((nx, ny)) # Here we add the neighbor to the visited set.
        current = (exit) # This variable serves as a tracker starting at the end of the path.
        p: list[tuple[int, int]] = [] # This list will contain the final path (end to start order).
        p.append(current) # Here we init the p list with current cell's coordinates which is the exit.
        while current != entry: # While the current cell is not the entry we itterate.
            current = came_from[current] # The current becomes before it.
            p.append(current) # Here we append the current to the p list.
        self._path = list(reversed(p)) # Finally, we invert the whole p list in the right order and assign it to the Class variable _path.
