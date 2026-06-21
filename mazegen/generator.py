from . import Parsing
from random import choice
from functools import reduce
from .colors import WHITE, BLACK, END, RED, BLUE, GREEN, MAGENTA, YELLOW, CYAN, ORANGE, BROWN
from collections import deque

class Cell:
    def __init__(self) -> None:
        self.walls: dict[str, bool] = {
            'W': True, 'S': True, 'E': True, 'N': True}
        self.visited: bool = False
        self.static: bool = False

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
        print('')
        for y in range(len(self.grid)):
            row = self.grid[y]
            wall = f'{self._themes[self._mode][0]}{self._wall}{END}'
            line1 = line2 = line3 = right = left = ''
            for x in range(len(row)):
                cell_floor = f'{self._themes[self._mode][1]}░'
                cell: Cell = row[x]
                decimal: int = int(cell.get_binary(), 2)
                if decimal & 1:
                    line1 += f'{wall * 5}'
                else:
                    line1 += f'{wall}{cell_floor * 3}{wall}'
                if decimal & 2:
                    right = f'{wall}'
                else:
                    right = f'{cell_floor}'
                if decimal & 8:
                    left = f'{wall}'
                else:
                    left = f'{cell_floor}'
                if decimal & 4:
                    line3 += f'{wall * 5}'
                if (x,y) == self.entry:
                    cell_floor = f'{self._themes[self._mode][2]} █ {END}'
                elif (x,y) == self.exit:
                    cell_floor = f'{self._themes[self._mode][3]} █ {END}'
                elif decimal == 15:
                    cell_floor = f'{self._themes[self._mode][0]}{wall * 3}{END}'
                if self._show == True:
                    if (x, y) in self._path and (x,y) != (0,0):
                        bullet = (self._themes[self._mode][2] if self._mode == 1 else
                                  self._themes[self._mode][3]) +'●'
                        c = f'{self._themes[self._mode][1]}░'
                        cell_floor = c + bullet + c
                if cell_floor == f'{self._themes[self._mode][1]}░':
                    cell_floor *= 3
                line2 += f'{left}{cell_floor}{right}'
            
            print(line1)
            print(line2)
        print(line3) 
    
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
        while current != entry:
            current = came_from[current]
            self._path.append(current)


    def _prims(self, x: int, y: int) -> None:
        ...
