from random import choice, randint, random, seed
from .colors import END, RED, GREEN, _theme
from collections import deque
import sys
import termios
import tty
from time import sleep
from os import system
from . import Parsing


class Pixel:
    def __init__(self) -> None:
        self.px: str = ''
        self.bg: str = ''

    def render_helper(self) -> str:
        return self.bg + self.px


class Cell:
    def __init__(self) -> None:
        self.walls: dict[str, bool] = {
            'W': True, 'S': True, 'E': True, 'N': True}
        self.visited: bool = False
        self.static: bool = False
        self.matrix: list[list[Pixel]] = []
        self.x: int = 0
        self.y: int = 0

    def get_binary(self) -> str:
        value: list[int] = [int(x) for x in self.walls.values()]
        binary: str = ''.join([str(x) for x in value])
        return (binary)

    def neighbors(self) -> dict[str, tuple[int, int]]:
        return {
            'NORTH': (self.x, self.y-1),
            'EAST': (self.x+1, self.y),
            'SOUTH': (self.x, self.y+1),
            'WEST': (self.x-1, self.y),
        }


class MazeGenerator:
    def __init__(self, config: Parsing):
        self.width: int = config._width
        self.height: int = config._height
        self.entry: tuple[int, int] = config._entry
        self.exit: tuple[int, int] = config._exit
        self.output_file: str = config._output_file
        self.perfect: bool = config._perfect
        self.algorythm: str = config._algorythm
        self.seed: int = config._seed
        self.grid: list[list[Cell]] = []
        self._path: list[tuple[int, int]] = []
        self._show: bool = False
        self._wall: str = '█'
        self._animation: bool = False
        self._mode: int = 0
        self._g_mode: str = 'easy'
        self._pattern42: list[tuple] = [
            (0, 0), (0, 1), (0, 2), (1, 2), (2, 2),
            (2, 3), (2, 4),  # 4
            (4, 0), (5, 0), (6, 0), (6, 1), (6, 2),
            (5, 2), (4, 2), (4, 3), (4, 4), (5, 4), (6, 4)  # 2
        ]

    def lose_win(self, result: str) -> None:
        from .animation import w_l
        colors: list[str] = [
            _theme[self._mode][0],
            _theme[self._mode][3]
        ]
        self.render(1, True)
        for loops in range(8):
            for x in range(2):
                print('\033[H', end='')
                print(self._display().replace('\n', '\r\n'))
                print(
                    (colors[x] + w_l(self, result)).replace('\n', '\r\n'),
                    end='')
                if result == 'win':
                    sleep(0.1)
                else:
                    sleep(0.3)
                    if loops == 3:
                        return

    def get_neighbors(self,
                      x: int, y: int, status: str) -> list[tuple[int, int]]:
        nb: list[tuple] = []
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

    def get_grid(self) -> None:
        self.grid = [
            [Cell() for _ in range(self.width)] for _ in range(self.height)]
        for pos_y, row in enumerate(self.grid):
            for pos_x, cell in enumerate(row):
                cell.x = pos_x
                cell.y = pos_y
                cell.matrix = [[Pixel() for _ in range(3)] for _ in range(3)]

    def get_dir(self, x: int, y: int, nx: int, ny: int) -> str:
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
        opposite: dict = {'E': 'W', 'W': 'E', 'N': 'S', 'S': 'N'}
        direction: str = self.get_dir(x, y, nx, ny)
        self.grid[y][x].walls[direction] = False
        self.grid[ny][nx].walls[opposite[direction]] = False

    def _display(self) -> str:
        maze = ''
        for y, row in enumerate(self.grid):
            for m_row in range(3):
                if m_row == 2 and y < self.height - 1:
                    continue
                for x, cell in enumerate(row):
                    for m_col in range(3):
                        if m_col == 0 and x > 0:
                            continue
                        maze += (cell.matrix[m_row][m_col].render_helper())
                maze += '\n'
        return maze

    def get_path(self, update: bool = False, ansi_mode: int = 1) -> None:
        is_ansi: list[list[str]] = [
            [(''), (''), (''), ('')],

            [(_theme[self._mode][0]), (_theme[self._mode][1]),
             (_theme[self._mode][2]), (_theme[self._mode][3])]]
        is_color: list[str] = [
            (is_ansi[ansi_mode][0]), (is_ansi[ansi_mode][1]),
            (is_ansi[ansi_mode][2]), (is_ansi[ansi_mode][3])
        ]

        _end: list[str] = [
            (''), (END)]
        bullet: str = is_color[3] + '█'
        for num, dot in enumerate(self._path):
            neighbors_in_path = [
                self._path[num + 1] if num + 1 < len(self._path) else None,
                self._path[num - 1] if num - 1 >= 0 else None,
            ]
            x, y = dot
            if ansi_mode and not update:
                print('\033[H', end='')
                sleep(0.0005)
            cell: Cell = self.grid[y][x]
            if dot != self.entry and dot != self.exit:
                cell.matrix[1][1].px = bullet * 2 + _end[ansi_mode]
            if cell.neighbors()['EAST'] in neighbors_in_path:
                cell.matrix[1][2].px = bullet * 2 + _end[ansi_mode]
            if cell.neighbors()['WEST'] in neighbors_in_path:
                cell.matrix[1][0].px = bullet * 2 + _end[ansi_mode]
            if cell.neighbors()['NORTH'] in neighbors_in_path:
                cell.matrix[0][1].px = bullet * 2 + _end[ansi_mode]
            if cell.neighbors()['SOUTH'] in neighbors_in_path:
                cell.matrix[2][1].px = bullet * 2 + _end[ansi_mode]
            if not update:
                print(self._display())

    def path_direction(self) -> str:
        path_dir: list[tuple[int, int]] = []
        direction: str = ''
        path_dir.append(self.entry)
        for n, step in enumerate(self._path):
            if n == 0:
                continue
            nx, ny = step
            x, y = path_dir[-1]
            direction += self.get_dir(x, y, nx, ny)
            path_dir.append(step)
        return direction

    def render(self,
               ansi: int = 1, update: bool = False,
               play: bool = False) -> None:
        is_ansi: list[list[str]] = [
            [(''), (''), (''), ('')],

            [(_theme[self._mode][0]), (_theme[self._mode][1]),
             (_theme[self._mode][2]), (_theme[self._mode][3])]]
        is_color: list[str] = [
            (is_ansi[ansi][0]), (is_ansi[ansi][1]),
            (is_ansi[ansi][2]), (is_ansi[ansi][3])
        ]
        background: str = is_color[1]
        _end: list[str] = [
            (''), (END)]
        en_ex: list[str] = [
            is_color[2] + '█',
            is_color[3] + '█',
            ' '
        ]
        for y in range(len(self.grid)):
            row = self.grid[y]
            wall = f'{is_color[0]}{self._wall}'
            for x in range(len(row)):
                cell_floor: str = background + ' '
                c: Cell = row[x]
                decimal: int = int(c.get_binary(), 2)
                for m_col in range(3):
                    if decimal & 1:
                        if m_col == 1:
                            c.matrix[0][m_col].px = f'{wall * 2}{_end[ansi]}'
                        else:
                            c.matrix[0][m_col].px = f'{wall * 2}{_end[ansi]}'
                    else:
                        if m_col == 1:
                            c.matrix[0][m_col].px = cell_floor * 2
                        else:
                            c.matrix[0][m_col].px = f'{wall * 2}{_end[ansi]}'
                    if decimal & 2:
                        c.matrix[1][2].px = f'{wall * 2}{_end[ansi]}'
                    else:
                        c.matrix[1][2].px = f'{cell_floor * 2}'

                    if decimal & 8:
                        c.matrix[1][0].px = f'{wall * 2}{_end[ansi]}'
                    else:
                        c.matrix[1][0].px = f'{cell_floor * 2}'

                    if decimal & 4:
                        if m_col == 1:
                            c.matrix[2][m_col].px = f'{wall * 2}{_end[ansi]}'
                        else:
                            c.matrix[2][m_col].px = f'{wall * 2}{_end[ansi]}'

                    if decimal == 15:
                        c.matrix[1][m_col].px = f'{wall * 2}{_end[ansi]}'
                    else:
                        c.matrix[1][1].px = cell_floor * 2
                    c.matrix[0][m_col].bg = background
                    c.matrix[1][2].bg = background
                    c.matrix[1][0].bg = background
                    c.matrix[2][m_col].bg = background
                    c.matrix[1][m_col].bg = background
                if (x, y) == self.entry:
                    c.matrix[1][1].px = en_ex[0] * 2 + _end[ansi]
                if (x, y) == self.exit:
                    c.matrix[1][1].px = en_ex[1] * 2 + _end[ansi]

        if self._show or play:
            self.get_path(ansi_mode=ansi, update=update)
            system('clear')
        termios.tcflush(sys.stdin, termios.TCIFLUSH)

    def saved(self) -> None:
        _save = GREEN + f'    file saved : {self.output_file}' + END
        self.render(update=True)
        system('clear')
        for x in range(3):
            print(self._display())
            sleep(0.5)
            print(f'{_save}\r', end='')
            if x == 2:
                sleep(0.2)
                break
            else:
                sleep(0.6)
            system('clear')

    def save(self) -> None:
        self.render(ansi=0, update=True)
        with open(self.output_file, 'w') as file:
            file.write(self._display())
        self.saved()

    def save_hex(self) -> None:
        hex_content: str = ''
        row: list[list[Cell]] = self.grid
        for collumn in row:
            for cell in collumn:
                hex_content += format(int(cell.get_binary(), 2), 'X')
            hex_content += '\n'
        hex_content += '\n'
        hex_content += (f'{str(self.entry[0])},{str(self.entry[1])}\n'
                        f'{str(self.exit[0])},{str(self.exit[1])}\n')
        hex_content += self.path_direction()
        with open(self.output_file, 'w') as file:
            file.write(hex_content)
        self.saved()

    def generate(self) -> None:
        if self.seed:
            seed(self.seed)
        if self.algorythm == 'dfs':
            self._dfs()
        else:
            self.prim()
        if not self.perfect:
            self.make_imperfect()
        self._path = []
        self._bfs(self.entry, self.exit)
        self.render()

    def init_static(self) -> None:
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
        print('\033[H', end='')
        self.render()
        print(self._display())
        sleep(0.001)

    def make_imperfect(self) -> None:
        s_e: dict[str, str] = {'E': 'EAST', 'S': 'SOUTH'}
        row = self.grid
        for collumn in row:
            for cell in collumn:
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
        '''Depth-first search (DFS) is an algorithm used to traverse
        or search through a data structure, such as a graph or tree.'''
        self.get_grid()
        self.init_static()
        stack: list[tuple] = []
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

    def prim(self) -> None:
        self.get_grid()
        self.init_static()
        frontiers: list[tuple[int, int]] = []
        cell = self.grid
        while True:
            x = randint(0, self.width - 1)
            y = randint(0, self.height - 1)
            if cell[y][x].static:
                continue
            break
        cell[y][x].visited = True
        frontiers.extend(self.get_neighbors(x, y, 'unvisited'))
        while frontiers:
            n = choice(frontiers)
            frontiers.remove(n)
            v = choice(self.get_neighbors(n[0], n[1], 'visited'))
            self.knock_wall(n[0], n[1], v[0], v[1])
            cell[n[1]][n[0]].visited = True
            frontiers.extend(
                [c for c in self.get_neighbors(n[0], n[1], 'unvisited') if
                 c not in frontiers])
            if self._animation:
                self._animate()
        system('clear')

    def _bfs(self, entry: tuple[int, int], exit: tuple[int, int]) -> None:
        opposite: dict[str, str] = {'E': 'W', 'W': 'E', 'N': 'S', 'S': 'N'}
        cell = self.grid
        x: int = 0
        y: int = 0
        visited: set[tuple[int, int]] = set()
        came_from: dict[tuple[int, int], tuple[int, int]] = {}
        queue: deque = deque()
        visited.add(entry)
        queue.append(entry)
        came_from[entry] = entry
        while queue:
            x, y = queue.popleft()
            if (x, y) == exit:
                break
            neighbours = [(x, y-1), (x+1, y), (x, y+1), (x-1, y)]
            for nx, ny in neighbours:
                if (nx >= 0 and nx < self.width and
                        ny >= 0 and ny < self.height):
                    if (nx, ny) not in visited:
                        direction: str = self.get_dir(x, y, nx, ny)
                        if not (cell[y][x].walls[direction]
                                and cell[ny][nx].walls[opposite[direction]]):
                            queue.append((nx, ny))
                            came_from[(nx, ny)] = (x, y)
                            visited.add((nx, ny))
        current = (exit)
        p: list[tuple[int, int]] = []
        p.append(current)
        while current != entry:
            current = came_from[current]
            p.append(current)
        self._path = list(reversed(p))

    def play(self) -> None:
        system('clear')
        fd: int = sys.stdin.fileno()
        old_setting = termios.tcgetattr(fd)

        tty.setraw(sys.stdin)

        x, y = self.entry
        self._path = []
        direction_map: dict[str, str] = {
            'N': 'NORTH', 'S': 'SOUTH', 'E': 'EAST', 'W': 'WEST'}
        self.render(update=True)
        print(self._display().replace('\n', '\r\n'), end='')
        self._path.append(self.entry)
        k: str = ''
        moves = {
            '[A': ('N', 0, -1),
            '[B': ('S', 0, +1),
            '[D': ('W', -1, 0),
            '[C': ('E', +1, 0)}
        j: str = str(sys.stdin.read(1))
        if j == '\x1b':
            k = str(sys.stdin.read(2))
        system('clear')
        try:
            while j != 'q':
                if j == '\x1b':
                    if k in moves:
                        w, dx, dy = moves[k]
                        nx, ny = x + dx, y + dy
                        if not self.grid[y][x].walls[w]:
                            if not (
                                (nx, ny) in self._path and
                                    self._g_mode == 'hard'):
                                x, y = nx, ny

                print('\033[H', end='')
                if len(self._path) >= 2 and (x, y) == self._path[-2]:
                    if self._g_mode == 'easy':
                        self._path.pop()
                    self.render(update=True, play=True)

                if (x, y) not in self._path:
                    self._path.append((x, y))
                    self.render(update=True, play=True)

                game_over: bool = True
                for direction, wall in self.grid[y][x].walls.items():
                    pos: tuple[int, int] = (
                        self.grid[y][x].neighbors()[direction_map[direction]])
                    if not wall and pos not in self._path:
                        game_over = False
                        break

                if (x, y) == self.exit:
                    self.lose_win(result='win')
                    break

                if self._g_mode == 'hard':
                    if game_over and (x, y) != self.exit:
                        self.lose_win(result='lose')
                        break
                print(self._display().replace('\n', '\r\n'), end='')

                j = str(sys.stdin.read(1))
                if j == '\x1b':
                    k = sys.stdin.read(2)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_setting)
