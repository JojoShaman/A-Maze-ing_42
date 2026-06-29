from .colors import GREEN, END
from time import sleep
from os import system
from .generator import MazeGenerator
from .renderer import render, display
from .cell import Cell


def save_confirmation(maze: MazeGenerator) -> None:
    """Print save confirmation with blinking animation.
    
    Args:
        maze: MazeGenerator instance to render, display and access output file.
    """
    _save = GREEN + f'    file saved: {maze.output_file}' + END
    render(maze, update=True)
    system('clear')
    for x in range(3):
        print(display(maze))
        sleep(0.5)
        print(f'{_save}\r', end='')
        if x == 2:
            sleep(0.2)
            break
        else:
            sleep(0.6)
        system('clear')

def save(maze: MazeGenerator) -> None:
    """Open the output file and writes the maze rendered.
    
    Args:
        maze: MazeGenerator instance to render,
            display and access output file.
    """
    render(maze, ansi=0, update=True)
    with open(maze.output_file, 'w') as file:
        file.write(display(maze))
    save_confirmation(maze)

def save_hex(maze: MazeGenerator) -> None:
    """Open the output file and writes the maze in hexadecimal,
    the entry/exit and the path.
    
    Args:
        maze: MazeGenerator instance to render,
            display and access output file.
    """
    hex_content: str = ''
    row: list[list[Cell]] = maze.grid
    for column in row:
        for cell in column:
            hex_content += format(int(cell.get_binary(), 2), 'X')
        hex_content += '\n'
    hex_content += '\n'
    hex_content += (f'{str(maze.entry[0])},{str(maze.entry[1])}\n'
                    f'{str(maze.exit[0])},{str(maze.exit[1])}\n')
    hex_content += path_direction(maze=maze)
    with open(maze.output_file, 'w') as file:
        file.write(hex_content)
    save_confirmation(maze=maze)

def path_direction(maze: MazeGenerator) -> str:
    """Get the path from entry to exit and returns a string.
    
    Args:
        maze: MazeGenerator instance to render,
            display and access output file.
    Returns:
        str: Return a string with the path in the following format
            -> (WSEN...).
    """
    path_dir: list[tuple[int, int]] = []
    direction: str = ''
    path_dir.append(maze.entry)
    for n, step in enumerate(maze._path):
        if n == 0:
            continue
        nx, ny = step
        x, y = path_dir[-1]
        direction += maze.get_direction(x, y, nx, ny)
        path_dir.append(step)
    return direction