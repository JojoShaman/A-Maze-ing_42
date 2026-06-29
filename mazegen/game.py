from os import system
import sys
import termios
import tty
from .generator import MazeGenerator
from .renderer import render, display
from .colors import THEMES, END
from time import sleep

def game_animation(maze: MazeGenerator, status: str) -> str:
    """Return an ANSI string displaying 'YOU WIN' or 'GAME OVER'.

    Args:
        maze: MazeGenerator instance to access the maze dimensions.
        status: game result, either 'win' or 'lose'.
    Returns:
        str: formatted ANSI string matching the game result.
    """
    space: str = ''
    if status == 'win':
        space = (' ' * (((maze.width * 4) - 64) // 2)
                 if ((maze.width * 4) - 64) > 0 else '')
    else:
        space = (' ' * (((maze.width * 4) - 74) // 2)
                 if ((maze.width * 4) - 74) > 0 else '')
    w = maze._wall

    win = (
            f'{space} {w * 2}╗   {w * 2}╗ ' +
            f'{w * 6}╗ {w * 2}╗   {w * 2}╗     ' +
            f'{w * 2}╗    {w * 2}╗{w * 2}╗{w * 3}╗ ' +
            f'  {w * 2}╗  {w * 2}╗\n' +
            f'{space} ╚{w * 2}╗ {w * 2}╔╝{w * 2}╔═══' +
            f'{w * 2}╗{w * 2}║   {w * 2}║   ' +
            f'  {w * 2}║    {w * 2}║{w * 2}║{w * 4}╗ ' +
            f' {w * 2}║  {w * 2}║\n' +
            f'{space}  ╚{w * 4}╔╝ {w * 2}║   {w * 2}║{w * 2}║' +
            f'   {w * 2}║    ' +
            f' {w * 2}║ {w}╗ {w * 2}║{w * 2}║{w * 2}╔{w * 2}╗ ' +
            f'{w * 2}║  {w * 2}║\n' +
            f'{space}   ╚{w * 2}╔╝  {w * 2}║   {w * 2}║{w * 2}║ ' +
            f'  {w * 2}║  ' +
            f'   {w * 2}║{w * 3}╗{w * 2}║{w * 2}║{w * 2}║╚{w * 2}╗' +
            f'{w * 2}║  ╚═╝\n' +
            f'{space}    {w * 2}║   ╚{w * 6}╔╝╚{w * 6}╔╝     ' +
            f'╚{w * 3}╔{w * 3}' +
            f'╔╝{w * 2}║{w * 2}║ ╚{w * 4}║  {w * 2}╗\n' +
            f'{space}    ╚═╝    ╚═════╝  ╚═════╝       ╚══╝╚══╝ ' +
            '╚═╝╚═╝  ╚═══╝  ╚═╝\n' + END)

    lose = (
            f'{space} {w*6}╗  {w*5}╗ {w*3}╗   {w*3}╗{w*7}╗     ' +
            f'{w*6}╗ {w*2}╗   ' +
            f'{w*2}╗{w*7}╗{w*6}╗ \n' +
            f'{space}{w*2}╔════╝ {w*2}╔══{w*2}╗{w*4}╗ {w*4}║{w*2}' +
            f'╔════╝    {w*2}' +
            f'╔═══{w*2}╗{w*2}║   {w*2}║{w*2}╔════╝{w*2}╔══{w*2}╗\n' +
            f'{space}{w*2}║  {w*3}╗{w*7}║{w*2}╔{w*4}╔{w*2}║{w*5}╗   ' +
            f'   {w*2}║   ' +
            f'{w*2}║{w*2}║   {w*2}║{w*5}╗  {w*6}╔╝\n' +
            f'{space}{w*2}║   {w*2}║{w*2}╔══{w*2}║{w*2}║╚{w*2}' +
            f'╔╝{w*2}║{w*2}╔══╝   '
            f'   {w*2}║   {w*2}║╚{w*2}╗ {w*2}╔╝{w*2}╔══╝  {w*2}' +
            f'╔══{w*2}╗\n' +
            f'{space}╚{w*6}╔╝{w*2}║  {w*2}║{w*2}║ ╚═╝ {w*2}║{w*7}╗' +
            f'    ╚{w*6}╔╝ ' +
            f'╚{w*4}╔╝ {w*7}╗{w*2}║  {w*2}║\n' +
            f'{space} ╚═════╝ ╚═╝  ╚═╝╚═╝     ╚═╝╚══════╝     ╚═════╝' +
            '   ╚═══╝  ' +
            '╚══════╝╚═╝  ╚═╝\n' + END)
    if status == 'win':
        return win
    return lose

def game_result(maze: MazeGenerator, result: str) -> None:
    """Display the game result with the right ANSI string and animation
    
    Args:
        maze: MazeGenerator instance to render and display the maze.
        result: game result, either 'win' or 'lose'.
    """
    from . import render, display
    colors: list[str] = [
        THEMES[maze._mode][0],
        THEMES[maze._mode][3]
    ]
    render(maze=maze, ansi=1, update=True)
    for loops in range(8):
        for x in range(2):
            print('\033[H', end='')
            print(display(maze).replace('\n', '\r\n'))
            print(
                (colors[x] + game_animation(maze, result)).replace('\n', '\r\n'),
                end='')
            if result == 'win':
                sleep(0.1)
            else:
                sleep(0.3)
                if loops == 3:
                    return

def play(maze: MazeGenerator) -> None:
        """Detect key and move in the maze.

        Args:
            maze: MazeGenerator instance to render, display and access maze data
        """
        system('clear')
        fd: int = sys.stdin.fileno()
        old_setting = termios.tcgetattr(fd)

        tty.setraw(sys.stdin)

        x, y = maze.entry
        maze._path = []
        direction_map: dict[str, str] = {
            'N': 'NORTH', 'S': 'SOUTH', 'E': 'EAST', 'W': 'WEST'}
        render(maze=maze, update=True)
        print(display(maze).replace('\n', '\r\n'), end='')
        maze._path.append(maze.entry)
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
                        if not maze.grid[y][x].walls[w]:
                            if not (
                                (nx, ny) in maze._path and
                                    maze._g_mode == 'hard'):
                                x, y = nx, ny

                print('\033[H', end='')
                if len(maze._path) >= 2 and (x, y) == maze._path[-2]:
                    if maze._g_mode == 'easy':
                        maze._path.pop()
                    render(maze=maze, update=True, play=True)

                if (x, y) not in maze._path:
                    maze._path.append((x, y))
                    render(maze=maze, update=True, play=True)

                game_over: bool = True
                for direction, wall in maze.grid[y][x].walls.items():
                    pos: tuple[int, int] = (
                        maze.grid[y][x].neighbors()[direction_map[direction]])
                    if not wall and pos not in maze._path:
                        game_over = False
                        break

                if (x, y) == maze.exit:
                    game_result(maze=maze, result='win')
                    break

                if maze._g_mode == 'hard':
                    if game_over and (x, y) != maze.exit:
                        game_result(maze=maze, result='lose')
                        break
                print(display(maze).replace('\n', '\r\n'), end='')

                j = str(sys.stdin.read(1))
                if j == '\x1b':
                    k = sys.stdin.read(2)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_setting)
