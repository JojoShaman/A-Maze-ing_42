from . import Parsing
from random import choice
from functools import reduce
from .colors import WHITE, BLACK, END, RED, BLUE, GREEN, MAGENTA, YELLOW, CYAN, ORANGE, BROWN
from collections import deque
from time import sleep
from os import system
class Cell:
    def __init__(self) -> None:
        self.walls: dict[str, bool] = {
            'W': True, 'S': True, 'E': True, 'N': True}
        self.visited: bool = False
        self.static: bool = False
        self.top: str = ''
        self.left: str = ''
        self.right: str = ''
        self.middle: str = ''
        self.bottom: str = ''
        self.bullet: str = ''

    def get_binary(self) -> str:
        binary: str = ''
        value: list = [int(x) for x in self.walls.values()]
        binary += str(reduce(lambda a, b: (a * 10) + b, value))
        return (binary)

class MazeGenerator:
    def __init__(self, config: Parsing):
        self.width = config._width
        self.height = config._height
        self.entry = config._entry
        self.exit = config._exit
        self.output_file = config._output_file
        self.perfect = config._perfect
        self.algorythm = config._algorythm
        self.grid: list[list[Cell]] = [] 
        self._path: list = []
        self._show = False
        self._wall = '█'
        self._mode = 0
        self._themes: list[list[str]] = [
                [WHITE, BLUE, RED, GREEN],
                [YELLOW, GREEN, MAGENTA, CYAN],
                [ORANGE, BLACK, WHITE, WHITE],
                [CYAN, MAGENTA, YELLOW, YELLOW],
                [GREEN, BLUE, RED, RED]
                ]

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


    def render(self) -> None:
        # print('')
        # pathway = ''
        # maze = ''

        rendered: str = ''
        for y in range(len(self.grid)):
            row = self.grid[y]
            wall = f'{self._themes[self._mode][0]}{self._wall}{END}'
            line1: str = ''
            line2: str = ''
            line3: str = ''
            right = left = ''
            for x in range(len(row)):
                cell_floor = f'{self._themes[self._mode][1]}░'
                cell: Cell = row[x]
                decimal: int = int(cell.get_binary(), 2)
                if decimal & 1:
                    cell.top = f'{wall * 5}'
                else:
                    cell.top = f'{wall}{cell_floor * 3}{wall}'
                if decimal & 2:
                    cell.right = f'{wall}'
                else:
                    cell.right = f'{cell_floor}'
                if decimal & 8:
                    cell.left = f'{wall}'
                else:
                    cell.left = f'{cell_floor}'
                if decimal & 4:
                    cell.bottom = f'{wall * 5}'
                if (x,y) == self.entry:
                    cell_floor = f'{self._themes[self._mode][2]} █ {END}'
                elif (x,y) == self.exit:
                    cell_floor = f'{self._themes[self._mode][3]} █ {END}'
                elif decimal == 15:
                    cell_floor = f'{self._themes[self._mode][0]}{wall * 3}{END}'
                if (x, y) in self._path and (x,y) != (0,0):
                    bullet = (self._themes[self._mode][2] if self._mode == 1 else
                                self._themes[self._mode][3]) +'●'
                    c = f'{self._themes[self._mode][1]}░'
                    dot = c + bullet + c
                    cell.bullet = f'{cell.left}{dot}{cell.right}'
                if cell_floor == f'{self._themes[self._mode][1]}░':
                    cell_floor *= 3
                cell.middle = f'{cell.left}{cell_floor}{cell.right}'
                line1 += cell.top
                line2 += cell.middle
                line3 += cell.bottom
            rendered += line1 + '\n' + line2 + '\n'
        rendered += line3
        if self._show == True:
            for dot in self._path:
                print('\033[H', end='')
                sleep(0.005)
                # print('test')
                for y in range(self.height):
                    for x in range(self.width):
                        print(self.grid[y][x].top, end='')
                    print('')
                    for x in range(self.width):
                        if (x,y) == dot and (x,y) != (0,0):
                            self.grid[y][x].middle = self.grid[y][x].bullet
                        print(self.grid[y][x].middle, end='')
                    print('')
                for x in range(self.width):
                    print(self.grid[y][x].bottom, end='')
                print('')
        else:
            print(rendered)

    
    def theme_menu(self) -> None:
        print((' ' * 11) + '╭' + ('-' * 12) + '╮')
        print((' ' * 11) + '| ' + '* THEMES * |')
        print((' ' * 11) + '╰' + ('-' * 12) + '╯' + '\n')
        print((' ' * 10) + 'enter) default theme')
        print((' ' * 10) + '1) sao paolo theme')
        print((' ' * 10) + '2) Orange is the new black theme')
        print((' ' * 10) + '3) BubbleGum theme')
        print((' ' * 10) + '4) Snake theme')
        print((' ' * 10) + '-' * 10)
        print((' ' * 10) + 'b) go back', END)
    
    def generate(self) -> None:
        self._dfs()
        self._path = []
        self._bfs(self.entry, self.exit)
        self.render()

    def _dfs(self) -> None:
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
        while current != entry:
            current = came_from[current]
            p.append(current)
        self._path = list(reversed(p))


    def _prims(self, x: int, y: int) -> None:
        ...
