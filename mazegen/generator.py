from . import Parsing
from random import choice
from functools import reduce
from .colors import WHITE, BLACK, END, RED, BLUE, GREEN, MAGENTA, YELLOW, CYAN, ORANGE, BROWN

class Cell:
    def __init__(self) -> None:
        self.walls: dict[str, bool] = {
            'W': True, 'S': True, 'E': True, 'N': True}
        self.visited: bool = False
        self.static: bool = False

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
        self.colors: list[list[str]] = [
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


    def render(self, wall_type: str = '█', color_mode: int = 0) -> None:
        for y in range(len(self.grid)):
            row = self.grid[y]
            wall = f'{self.colors[color_mode][0]}{wall_type}{END}'
            line1 = ''
            line2 = ''
            line3 = ''
            right = ''
            left = ''
            for x in range(len(row)):
                cell_rep = f'{self.colors[color_mode][1]}░'
                cell: Cell = row[x]
                binary: str = ''
                value: list = [int(x) for x in cell.walls.values()]
                binary += str(reduce(lambda a, b: (a * 10) + b, value))
                decimal: int = int(binary, 2)
                if decimal & 1:
                    line1 += f'{wall * 5}'
                else:
                    line1 += f'{wall}{cell_rep * 3}{wall}'
                if decimal & 2:
                    right = f'{wall}'
                else:
                    right = f'{cell_rep}'
                if decimal & 8:
                    left = f'{wall}'
                else:
                    left = f'{cell_rep}'
                if decimal & 4:
                    line3 += f'{wall * 5}'
                if x == self.entry[0] and y == self.entry[1]:
                    cell_rep = f'{self.colors[color_mode][2]} █ {END}'
                elif x == self.exit[0] and y == self.exit[1]:
                    cell_rep = f'{self.colors[color_mode][3]} █ {END}'
                elif decimal == 15:
                    cell_rep = f'{self.colors[color_mode][0]}███{END}'
                if cell_rep == f'{self.colors[color_mode][1]}░':
                    cell_rep *= 3
                line2 += f'{left}{cell_rep}{right}'
            
            print(line1)
            print(line2)
        print(line3) 

    def generate(self) -> None:
        error = False
        if self.width < 7 or self.height < 5:
            raise Exception(f"{RED}Error: Maze size too small for '42' pattern.{END}")
        try:
            self._dfs()
        except Exception as e:
            raise (e)
        self.render()
        mode = 0
        while True:
            while True:
                try:
                    print(f'\n{self.colors[mode][0]}enter: regenerate maze')
                    print('2: maze theme')
                    print('q: quit')
                    choice = input('\nEnter command: ')
                    print('▁' * 20)
                    break
                except KeyboardInterrupt:
                    error = True
                    break
            if error == True:
                print('\nCtrl+c detected: Program closed')
                exit()
            if choice == '1' or not choice:
                self._dfs()
                self.render(color_mode=mode)
            elif choice == '2':
                print('\nenter: default theme')
                print('1: sombrero theme')
                print('2: Orange is the new black theme')
                print('3: BubbleGum theme')
                print('4: Snake theme')
                print('b: go back')
                while True:
                    try:
                        color_mode = input('\nMake your choice: ')
                        if not color_mode or color_mode == 'b':
                            break
                        mode = int(color_mode)
                        break
                    except ValueError:
                        print('please enter valid input')
                    except KeyboardInterrupt:
                        return
                print('\n')
                if color_mode == 'b':
                    continue
                elif not color_mode:
                    self.render()
                    mode = 0
                else:
                    self.render(color_mode=mode)
            elif choice == 'q':
                print('\nProgram closed')
                exit()
            else:
                print('please enter valid input')


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
            

    def _prims(self, x: int, y: int) -> None:
        ...

    # def solution(self) -> list[int]:
    #     pass
