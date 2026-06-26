from .generator import MazeGenerator
from .colors import END

def theme() -> None:
    print((' ' * 20) + '┏' + ('━' * 12) + '┓')
    print((' ' * 20) + '┃ ' + '* THEMES * ┃')
    print((' ' * 20) + '┗' + ('━' * 12) + '┛' + '\n')
    print((' ' * 18) + '↵    Default')
    print((' ' * 18) + '1    Sao Paolo')
    print((' ' * 18) + '2    Bumblebee')
    print((' ' * 18) + '3    Cotton Candy')
    print((' ' * 18) + '4    Snake\n')
    print((' ' * 18) + 'b    go back', END)

def algo(algorythm: str, theme: str) -> None:
    dfs = 'x' if algorythm == 'dfs' else ' '
    prim = 'x' if algorythm == 'prim' else ' '
    print(theme)
    print((' ' * 20) + '┏' + ('━' * 15) + '┓')
    print((' ' * 20) + '┃ ' + '* ALGORYTHM * ┃')
    print((' ' * 20) + '┗' + ('━' * 15) + '┛' + '\n')
    print((' ' * 20) + f'0     dfs     [{dfs}]')
    print((' ' * 20) + f'1     prim    [{prim}]\n')
    print((' ' * 20) + 'b    go back', END)

def game_mode(theme: list[list[str]], color_mode: int) -> None:
    print(theme[color_mode][2])
    print((' ' * 20) + '┏' + ('━' * 15) + '┓')
    print((' ' * 20) + '┃ ' + '* PLAY MODE * ┃')
    print((' ' * 20) + '┗' + ('━' * 15) + '┛' + '\n')
    print((' ' * 20) + f'0     easy')
    print((' ' * 20) + f'1     hard\n')
    print((' ' * 20) + 'b    go back\n', END)

def user(maze: MazeGenerator, show: str, animation: str) -> None:
    s = ' ' * 4
    space = ' '
    nb = maze._themes[maze._mode][2]
    colo = maze._themes[maze._mode][0]
    print(f'\n{maze._themes[maze._mode][0]}', end='')
    print(f'{s}┏{"━" * 9}  A-Maze-ing  {"━" * 9}┓')
    print(f'{s}┃{space * 32}┃')
    print(f'{s}┃{s}{nb}↵{s}{colo}regenerate maze{space * 8}┃')
    print(f'{s}┃{s}{nb}0{s}{colo}chose generator{space * 8}┃')
    print(f'{s}┃{s}{nb}1{s}{colo}{show}{space * 14}┃')
    print(f'{s}┃{s}{nb}2{s}{colo}maze theme{space * 13}┃')
    print(f'{s}┃{s}{nb}3{s}{colo}change wall type{space * 7}┃')
    print(f'{s}┃{s}{nb}4{s}{colo}change maze size{space * 7}┃')
    print(f'{s}┃{s}{nb}5{s}{colo}save rending{space * 11}┃')
    print(f'{s}┃{s}{nb}6{s}{colo}Game{space * 19}┃')
    print(f'{s}┃{s}{nb}7{s}{colo}{animation} ' +
            f'animation{space * 5 if maze._animation else space * 6}┃')
    print(f'{s}┃{space * 32}┃')
    print(f'{s}┃{s}{nb}q{s}{colo}quit{space * 19}┃')
    print(f'{s}┃{space * 32}┃')
    print(f'{s}┗{"━" * 32}┛')