from .colors import THEMES, END
from os import system
from time import sleep
import termios
import sys
from .generator import MazeGenerator
from .cell import Cell


def display(maze: MazeGenerator) -> str:
    """Return the maze visual representation.

    Args:
        maze: MazeGenerator instance to access the maze grid and dimensions.
    Returns:
        str: Returns a string with the visual represention of the maze."""
    matrix = ''
    for y, row in enumerate(maze.grid):
        for m_row in range(3):
            if m_row == 2 and y < maze.height - 1:
                continue
            for x, cell in enumerate(row):
                for m_col in range(3):
                    if m_col == 0 and x > 0:
                        continue
                    matrix += (cell.matrix[m_row][m_col].render_helper())
            matrix += '\n'
    return matrix


def render(maze: MazeGenerator, ansi: int = 1, update: bool = False,
           play: bool = False) -> None:
    """Render the maze with ANSI code and characters.

    Args:
        maze: MazeGenerator instance to access maze data.
        ansi: 1 for ANSI colors, 0 for plain text.
        update: whether to skip path animation and update silently.
        play: whether it's game mode """
    is_ansi: list[list[str]] = [
        [(''), (''), (''), ('')],

        [(THEMES[maze._mode][0]), (THEMES[maze._mode][1]),
            (THEMES[maze._mode][2]), (THEMES[maze._mode][3])]]
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
    for y in range(len(maze.grid)):
        row = maze.grid[y]
        wall = f'{is_color[0]}{maze._wall}'
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
            if (x, y) == maze.entry:
                c.matrix[1][1].px = en_ex[0] * 2 + _end[ansi]
            if (x, y) == maze.exit:
                c.matrix[1][1].px = en_ex[1] * 2 + _end[ansi]

    if maze._show or play:
        draw_path(maze, ansi_mode=ansi, update=update)
        system('clear')
    termios.tcflush(sys.stdin, termios.TCIFLUSH)


def draw_path(maze: MazeGenerator, update: bool = False,
              ansi_mode: int = 1) -> None:
    """Draw visual representation of the path.

    Args:
        maze: MazeGenerator instance to access maze data and display.
        update: whether to skip path animation and update silently.
        ansi_mode: 1 for ANSI colors, 0 for plain text.
    """
    is_ansi: list[list[str]] = [
        [(''), (''), (''), ('')],

        [(THEMES[maze._mode][0]), (THEMES[maze._mode][1]),
            (THEMES[maze._mode][2]), (THEMES[maze._mode][3])]]
    is_color: list[str] = [
        (is_ansi[ansi_mode][0]), (is_ansi[ansi_mode][1]),
        (is_ansi[ansi_mode][2]), (is_ansi[ansi_mode][3])
    ]

    _end: list[str] = [
        (''), (END)]
    bullet: str = is_color[3] + '█'
    for num, dot in enumerate(maze._path):
        neighbors_in_path = [
            maze._path[num + 1] if num + 1 < len(maze._path) else None,
            maze._path[num - 1] if num - 1 >= 0 else None,
        ]
        x, y = dot
        if ansi_mode and not update:
            print('\033[H', end='')
            sleep(0.0005)
        cell: Cell = maze.grid[y][x]
        if dot != maze.entry and dot != maze.exit:
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
            print(display(maze))
