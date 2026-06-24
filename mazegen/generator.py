from . import Parsing
from random import choice
from functools import reduce
from .colors import WHITE, BLACK, END, RED, BLUE, GREEN, MAGENTA, YELLOW, CYAN, ORANGE, BG_GREEN, BG_BLUE, BG_MAGENTA, BG_BLACK
from collections import deque
from time import sleep
from os import system
import sys, termios, tty

class Pixel:
    def __init__(self) -> None:
        self.pixel: str = ''
        self.bg: str = ''
    
    def render_helper(self) -> str:
        return self.bg + self.pixel 

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
        binary: str = ''
        value: list = [int(x) for x in self.walls.values()]
        binary += str(reduce(lambda a, b: (a * 10) + b, value))
        return (binary)
    
    def neighbors(self) -> dict[str, tuple[int, int]]:
        return {
            'NORTH': (self.x, self.y-1),
            'EAST': (self.x+1, self.y),
            'SOUTH': (self.x, self.y+1),
            'WEST': (self.x-1, self.y),
        }

class MazeGenerator:
    # maze = ''
    def __init__(self, config: Parsing):
        self.width = config._width
        self.height = config._height
        self.entry = config._entry
        self.exit = config._exit
        self.output_file = config._output_file
        self.perfect = config._perfect
        self.algorythm = config._algorythm
        self.grid: list[list[Cell]] = [] 
        self._path: list[tuple[int, int]] = []
        self._show = False
        self._wall = '█'
        self._mode = 0
        self._themes: list[list[str]] = [
                [WHITE, BG_BLUE, RED, GREEN],
                [YELLOW, BG_GREEN, MAGENTA, CYAN],
                [ORANGE, BG_BLACK, WHITE, WHITE],
                [CYAN, BG_MAGENTA, YELLOW, YELLOW],
                [GREEN, BG_BLUE, RED, RED]
                ]
    

    def display_win(self) -> None:
        space: str = ''
        if ((self.width * 4) - 60) > 0:
            space += ' ' * (((self.width * 4) - 64) // 2)
        w = self._wall
        self.render(1, True)
        winner: list[str] = [
            (
                f'{self._themes[self._mode][0]}' +
                f'{space} {w * 2}╗   {w * 2}╗ {w * 6}╗ {w * 2}╗   {w * 2}╗     ' +
                f'{w * 2}╗    {w * 2}╗{w * 2}╗{w * 3}╗   {w * 2}╗  {w * 2}╗\n' + 
                f'{space} ╚{w * 2}╗ {w * 2}╔╝{w * 2}╔═══{w * 2}╗{w * 2}║   {w * 2}║   ' +
                f'  {w * 2}║    {w * 2}║{w * 2}║{w * 4}╗  {w * 2}║  {w * 2}║\n' +
                f'{space}  ╚{w * 4}╔╝ {w * 2}║   {w * 2}║{w * 2}║   {w * 2}║    ' +
                f' {w * 2}║ {w}╗ {w * 2}║{w * 2}║{w * 2}╔{w * 2}╗ {w * 2}║  {w * 2}║\n' +
                f'{space}   ╚{w * 2}╔╝  {w * 2}║   {w * 2}║{w * 2}║   {w * 2}║  ' +
                f'   {w * 2}║{w * 3}╗{w * 2}║{w * 2}║{w * 2}║╚{w * 2}╗{w * 2}║  ╚═╝\n' +
                f'{space}    {w * 2}║   ╚{w * 6}╔╝╚{w * 6}╔╝     ╚{w * 3}╔{w * 3}' +
                f'╔╝{w * 2}║{w * 2}║ ╚{w * 4}║  {w * 2}╗\n' +
                f'{space}    ╚═╝    ╚═════╝  ╚═════╝       ╚══╝╚══╝ ' +
                '╚═╝╚═╝  ╚═══╝  ╚═╝\n' + END),
            (
                f'{self._themes[self._mode][3]}'
                f'{space} {w * 2}╗   {w * 2}╗ {w * 6}╗ {w * 2}╗   {w * 2}╗     ' +
                f'{w * 2}╗    {w * 2}╗{w * 2}╗{w * 3}╗   {w * 2}╗  {w * 2}╗\n' + 
                f'{space} ╚{w * 2}╗ {w * 2}╔╝{w * 2}╔═══{w * 2}╗{w * 2}║   {w * 2}║   ' +
                f'  {w * 2}║    {w * 2}║{w * 2}║{w * 4}╗  {w * 2}║  {w * 2}║\n' +
                f'{space}  ╚{w * 4}╔╝ {w * 2}║   {w * 2}║{w * 2}║   {w * 2}║    ' +
                f' {w * 2}║ {w}╗ {w * 2}║{w * 2}║{w * 2}╔{w * 2}╗ {w * 2}║  {w * 2}║\n' +
                f'{space}   ╚{w * 2}╔╝  {w * 2}║   {w * 2}║{w * 2}║   {w * 2}║  ' +
                f'   {w * 2}║{w * 3}╗{w * 2}║{w * 2}║{w * 2}║╚{w * 2}╗{w * 2}║  ╚═╝\n' +
                f'{space}    {w * 2}║   ╚{w * 6}╔╝╚{w * 6}╔╝     ╚{w * 3}╔{w * 3}' +
                f'╔╝{w * 2}║{w * 2}║ ╚{w * 4}║  {w * 2}╗\n' +
                f'{space}    ╚═╝    ╚═════╝  ╚═════╝       ╚══╝╚══╝ ' +
                '╚═╝╚═╝  ╚═══╝  ╚═╝\n')]
        for _ in range(8):
            for win in winner:
                print('\033[H', end='')
                print(self._display().replace('\n', '\r\n'))
                print(win.replace('\n', '\r\n'), end='')
                sleep(0.1)
        system('clear')


    def get_unvisited(self, x: int, y: int) -> list[tuple[int, int]]:
        unvisited: list[tuple] = []
        cell = self.grid
        neighbors = [(x, y-1), (x+1, y), (x, y+1), (x-1, y)]
        for nx, ny in neighbors:
            if (nx >= 0 and nx < self.width) and (ny >= 0 and ny < self.height):
                if not cell[ny][nx].visited:
                    unvisited.append((nx, ny))
        return unvisited
    
    def get_grid(self) -> None:
        self.grid = [[Cell() for _ in range(self.width)] for _ in range(self.height)]
        for pos_y, row in enumerate(self.grid) :
            for pos_x, cell in enumerate(row):
                cell.x = pos_x
                cell.y = pos_y
        for row in self.grid :
            for cell in row:
                cell.matrix = [[Pixel() for _ in range(3)] for _ in range(3)]


    def knock_wall(self, x: int, y: int, nx: int, ny: int) -> None:
        opposite: dict = {'E':'W', 'W':'E', 'N':'S', 'S':'N'}
        direction: str = ''
        if nx > x:
            direction = 'E'
        elif nx < x:
            direction = 'W'
        elif ny > y:
            direction = 'S'
        elif ny < y:
            direction = 'N'
        self.grid[y][x].walls[direction] = False
        self.grid[ny][nx].walls[opposite[direction]] = False


    def _display(self) -> str:
        maze = ''
        for y, row in enumerate(self.grid):
            for matrix_row in range(3):
                if matrix_row == 2 and y < self.height - 1:
                    continue
                for x, cell in enumerate(row):
                    for matrix_col in range(3):
                        if matrix_col == 0 and x > 0:
                            continue
                        maze += cell.matrix[matrix_row][matrix_col].render_helper()
                maze += '\n'
        return maze

    def get_path(self, is_new: bool = False, ansi_mode: int = 1) -> None:
        is_ansi: list[list[str]] = [
            [(''), (''), (''), ('')],

            [(self._themes[self._mode][0]), (self._themes[self._mode][1]),
            (self._themes[self._mode][2]), (self._themes[self._mode][3])]]
        is_color: list[str] = [
            (is_ansi[ansi_mode][0]), (is_ansi[ansi_mode][1]),
            (is_ansi[ansi_mode][2]), (is_ansi[ansi_mode][3])
        ]
        
        _end: list[str] = [
            (''), (END)]
        bullet = is_color[3] + '█'
        for num, dot in enumerate(self._path):
            neighbors_in_path = [
                self._path[num + 1] if num + 1 < len(self._path) else None,
                self._path[num - 1] if num - 1 >= 0 else None,
            ]
            x, y = dot
            if ansi_mode == 1 and is_new == False:
                print('\033[H', end='')
                # sleep(0.0009)
            cell = self.grid[y][x]
            if dot != self.entry and dot != self.exit:
                cell.matrix[1][1].pixel = bullet * 2 + _end[ansi_mode]
            if cell.neighbors()['EAST'] in neighbors_in_path:
                cell.matrix[1][2].pixel =  bullet * 2 + _end[ansi_mode]
            if cell.neighbors()['WEST'] in neighbors_in_path:
                cell.matrix[1][0].pixel =  bullet * 2 + _end[ansi_mode]
            if cell.neighbors()['NORTH'] in neighbors_in_path:
                cell.matrix[0][1].pixel = bullet * 2 + _end[ansi_mode]
            if cell.neighbors()['SOUTH'] in neighbors_in_path:
                cell.matrix[2][1].pixel = bullet * 2 + _end[ansi_mode]
            
            if is_new == False:
                print(self._display())

    def render(self, ansi: int = 1, update: bool = False, play: bool = False) -> None:
        is_ansi: list[list[str]] = [
            [(''), (''), (''), ('')],

            [(self._themes[self._mode][0]), (self._themes[self._mode][1]),
            (self._themes[self._mode][2]), (self._themes[self._mode][3])]]
        is_color: list[str] = [
            (is_ansi[ansi][0]), (is_ansi[ansi][1]),
            (is_ansi[ansi][2]), (is_ansi[ansi][3])
        ]
        background: str = is_color[1]
        
        _end: list[str] = [
            (''), (END)]

        en_ex: list[str] = [
            is_color[2] +'█',
            is_color[3] +'█',
            ' '
        ]
        for y in range(len(self.grid)):
            row = self.grid[y]
            wall = f'{is_color[0]}{self._wall}'

            for x in range(len(row)):
                cell_floor = background + ' '
                cell: Cell = row[x]
                decimal: int = int(cell.get_binary(), 2)

                for matrix_col in range(3):
                    if decimal & 1:
                        if matrix_col == 1:
                            cell.matrix[0][matrix_col].pixel = f'{wall * 2}{_end[ansi]}'
                        else:
                            cell.matrix[0][matrix_col].pixel = f'{wall * 2}{_end[ansi]}'
                    else:
                        if matrix_col == 1:
                            cell.matrix[0][matrix_col].pixel = cell_floor * 2
                        else:
                            cell.matrix[0][matrix_col].pixel = f'{wall * 2}{_end[ansi]}'
                    if decimal & 2:
                        cell.matrix[1][2].pixel = f'{wall  * 2}{_end[ansi]}'
                    else:
                        cell.matrix[1][2].pixel = f'{cell_floor * 2}'

                    if decimal & 8:
                        cell.matrix[1][0].pixel = f'{wall * 2}{_end[ansi]}'
                    else:
                        cell.matrix[1][0].pixel = f'{cell_floor * 2}'

                    if decimal & 4:
                        if matrix_col == 1:
                            cell.matrix[2][matrix_col].pixel = f'{wall * 2}{_end[ansi]}'
                        else:
                            cell.matrix[2][matrix_col].pixel = f'{wall * 2}{_end[ansi]}'

                    if decimal == 15:
                        cell.matrix[1][matrix_col].pixel = f'{wall * 2}{_end[ansi]}'
                    else:
                        cell.matrix[1][1].pixel = cell_floor * 2
                    cell.matrix[0][matrix_col].bg = background
                    cell.matrix[1][2].bg = background
                    cell.matrix[1][0].bg = background
                    cell.matrix[2][matrix_col].bg = background
                    cell.matrix[1][matrix_col].bg = background

                if (x,y) == self.entry:
                    cell.matrix[1][1].pixel = en_ex[0] * 2 + _end[ansi]

                if (x,y) == self.exit:
                    cell.matrix[1][1].pixel = en_ex[1] * 2 + _end[ansi]

        if self._show == True or play == True:
            self.get_path(ansi_mode=ansi, is_new=update)
            system('clear')
            # if update == False:
            #     self.display_win()
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
        with open (self.output_file, 'w') as file:
            file.write(self._display())
        self.saved()
    
    def theme_menu(self) -> None:
        print((' ' * 20) + '┏' + ('━' * 12) + '┓')
        print((' ' * 20) + '┃ ' + '* THEMES * ┃')
        print((' ' * 20) + '┗' + ('━' * 12) + '┛' + '\n')
        print((' ' * 18) + '↵    Default')
        print((' ' * 18) + '1    Sao Paolo')
        print((' ' * 18) + '2    Bumblebee')
        print((' ' * 18) + '3    Cotton Candy')
        print((' ' * 18) + '4    Snake\n')
        print((' ' * 18) + 'b    go back', END)
    
    def generate(self) -> None:
        self._dfs()
        self._path = []
        self._bfs(self.entry, self.exit)
        self.render()

    def _dfs(self) -> None:
        '''Depth-first search (DFS) is an algorithm used to traverse 
        or search through a data structure, such as a graph or tree.'''
        self.get_grid()
        stack: list[tuple] = []
        stack.append(self.entry)
        cell = self.grid
        cell[self.entry[1]][self.entry[0]].visited = True
        offset_x = (self.width - 7) // 2
        offset_y = (self.height - 5) // 2
        pattern42: list[tuple] = [
            (0, 0), (0,1), (0,2), (1,2), (2,2),
            (2,3), (2,4), #4
            (4, 0), (5, 0), (6, 0), (6, 1), (6, 2),
            (5, 2), (4,2), (4,3), (4,4), (5,4), (6, 4) #2
        ]
        for rel_x, rel_y in pattern42:
            tx: int = offset_x + rel_x
            ty: int = offset_y + rel_y
            if tx == self.entry[0] and ty == self.entry[1] or tx == self.exit[0] and ty == self.exit[1]:
                raise Exception(f'{RED}Entry & Exit must not be in 42 position{END}')
            cell[ty][tx].static = True
            cell[ty][tx].visited = True
        while stack:
            x, y = stack[-1]
            neighbors = self.get_unvisited(x, y)
            if neighbors:
                n = choice(neighbors)
                if not cell[n[1]][n[0]].static:
                    self.knock_wall(x, y, n[0], n[1])
                cell[n[1]][n[0]].visited = True
                stack.append(n)

            else:
                stack.pop()


    def _bfs(self, entry: tuple[int, int], exit: tuple[int, int]) -> None:
        opposite: dict = {'E':'W', 'W':'E', 'N':'S', 'S':'N'}
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
                        direction: str = ''
                        if nx > x:
                            direction = 'E'
                        elif nx < x:
                            direction = 'W'
                        elif ny > y:
                            direction = 'S'
                        elif ny < y:
                            direction = 'N'
                        if (cell[y][x].walls[direction] == False and
                            cell[ny][nx].walls[opposite[direction]] == False):
                            queue.append((nx, ny))
                            came_from[(nx, ny)] = (x, y)
                            visited.add((nx, ny))
        current = (exit)
        p: list = []
        p.append(current)
        while current != entry:
            current = came_from[current]
            p.append(current)
        self._path = list(reversed(p))


    def _prims(self, x: int, y: int) -> None:
        ...

    def play(self) -> None:
        fd= sys.stdin.fileno()
        old_setting = termios.tcgetattr(fd)

        tty.setraw(sys.stdin)

        x, y = self.entry
        self._path = []
        self.render(update=True)
        print(self._display().replace('\n', '\r\n'), end='')
        self._path.append(self.entry)
        k = ''
        j = str(sys.stdin.read(1))
        if j == '\x1b':
                k = str(sys.stdin.read(2))
        system('clear')
        while j != 'q':
            if j == '\x1b':
                if k == '[A':
                    if self.grid[y][x].walls['N'] == False:
                        y -= 1
                elif k == '[B':
                    if self.grid[y][x].walls['S'] == False:
                        y += 1
                elif k == '[D':
                    if self.grid[y][x].walls['W'] == False:
                        x -= 1
                elif k == '[C':
                    if self.grid[y][x].walls['E'] == False:
                        x += 1
            print('\033[H', end='')
            if len(self._path) >= 2 and (x,y) == self._path[-2]:
                self._path.pop()
                self.render(update=True, play=False)
                self.get_path(is_new=True)

            if (x,y) not in self._path:
                self._path.append((x, y))
                self.render(update=True, play=False)
                self.get_path(is_new=True)
            
            if (x,y) == self.exit:
                self.display_win()
                break

            print(self._display().replace('\n', '\r\n'), end='')

            j = str(sys.stdin.read(1))
            if j == '\x1b':
                k = sys.stdin.read(2)

        termios.tcsetattr(fd, termios.TCSADRAIN, old_setting)
        # print("\r\033[0K up", end='')
        # print("\r\033[0K down", end='')
        # print("\r\033[0K left", end='')
        # print("\r\033[0K right", end='')