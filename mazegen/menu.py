from .generator import MazeGenerator
from .colors import END, THEMES


def show_themes() -> None:
    """Display the theme selection menu."""
    print((' ' * 20) + '┏' + ('━' * 12) + '┓')
    print((' ' * 20) + '┃ ' + '* THEMES * ┃')
    print((' ' * 20) + '┗' + ('━' * 12) + '┛' + '\n')
    print((' ' * 18) + '↵    Default')
    print((' ' * 18) + '1    Sao Paolo')
    print((' ' * 18) + '2    Bumblebee')
    print((' ' * 18) + '3    Cotton Candy')
    print((' ' * 18) + '4    Snake\n')
    print((' ' * 18) + 'b    go back', END)


def algo(algorithm: str, theme: str) -> None:
    """Display the algorithm selection menu
    with the current selection highlighted.
    
    Args:
        algorithm: currently selected generation algorithm ('dfs' or 'prim').
        theme: ANSI color code string for the current theme.
    """
    dfs = 'x' if algorithm == 'dfs' else ' '
    prim = 'x' if algorithm == 'prim' else ' '
    print(theme)
    print((' ' * 20) + '┏' + ('━' * 15) + '┓')
    print((' ' * 20) + '┃ ' + '* ALGORITHM * ┃')
    print((' ' * 20) + '┗' + ('━' * 15) + '┛' + '\n')
    print((' ' * 20) + f'0     dfs     [{dfs}]')
    print((' ' * 20) + f'1     prim    [{prim}]\n')
    print((' ' * 20) + 'b    go back', END)


def game_mode(color_mode: int, game: str) -> None:
    """Display the difficulty selection menu
    with the current selection highlighted.
    
    Args:
        color_mode: index of the current theme in THEMES.
        game: currently selected difficulty ('easy' or 'hard').
    """
    easy = 'x' if game == 'easy' else ' '
    hard = 'x' if game == 'hard' else ' '
    print(THEMES[color_mode][2])
    print((' ' * 20) + '┏' + ('━' * 15) + '┓')
    print((' ' * 20) + '┃ ' + '* PLAY MODE * ┃')
    print((' ' * 20) + '┗' + ('━' * 15) + '┛' + '\n')
    print((' ' * 20) + f'0     easy    [{easy}]')
    print((' ' * 20) + f'1     hard    [{hard}]\n')
    print((' ' * 20) + 'b    go back\n', END)


def user(maze: MazeGenerator, show: str, animation: str) -> None:
    """Display the main menu with all available commands.
    
    Args:
        maze: MazeGenerator instance to access theme and animation state.
        show: label for the show/hide path option.
        animation: label for the animation toggle option.
    """
    s = ' ' * 4
    space = ' '
    nb = THEMES[maze._mode][2]
    colo = THEMES[maze._mode][0]
    print(f'\n{THEMES[maze._mode][0]}', end='')
    print(f'{s}┏{"━" * 9}  A-Maze-ing  {"━" * 9}┓')
    print(f'{s}┃{space * 32}┃')
    print(f'{s}┃{s}{nb}↵{s}{colo}Generate maze{space * 10}┃')
    print(f'{s}┃{s}{nb}0{s}{colo}Choose generator{space * 7}┃')
    print(f'{s}┃{s}{nb}1{s}{colo}{show}{space * 14}┃')
    print(f'{s}┃{s}{nb}2{s}{colo}Maze themes{space * 13}┃')
    print(f'{s}┃{s}{nb}3{s}{colo}Change wall type{space * 7}┃')
    print(f'{s}┃{s}{nb}4{s}{colo}Save rending{space * 11}┃')
    print(f'{s}┃{s}{nb}5{s}{colo}Save hex{space * 15}┃')
    print(f'{s}┃{s}{nb}6{s}{colo}Game{space * 19}┃')
    print(f'{s}┃{s}{nb}7{s}{colo}{animation} ' +
          f'animation{space * 5 if maze._animation else space * 6}┃')
    print(f'{s}┃{space * 32}┃')
    print(f'{s}┃{s}{nb}q{s}{colo}quit{space * 19}┃')
    print(f'{s}┃{space * 32}┃')
    print(f'{s}┗{"━" * 32}┛')
