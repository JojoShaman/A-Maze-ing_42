from mazegen.generator import MazeGenerator
from mazegen.parsing import Parsing
from mazegen.colors import RED, END
import sys
from os import system
from time import sleep

def run() -> None:
    maze = MazeGenerator(parsed)
    try:
        error = False
        try:
            maze.algorythm = 'prim'
            maze.generate()
            print(maze._display())
        except Exception as e:
            raise (e)
        while True:
            while True:
                show_hide = 'hide path' if maze._show else 'show path'
                animation = 'Turn off' if maze._animation else 'Turn on'
                try:
                    s = ' ' * 4
                    space = ' '
                    nb = maze._themes[maze._mode][2]
                    colo = maze._themes[maze._mode][0]
                    print(f'\n{maze._themes[maze._mode][0]}', end='')
                    print(f'{s}┏{"━" * 9}  A-Maze-ing  {"━" * 9}┓')
                    print(f'{s}┃{space * 32}┃')
                    print(f'{s}┃{s}{nb}↵{s}{colo}regenerate maze{space * 8}┃')
                    print(f'{s}┃{s}{nb}1{s}{colo}{show_hide}{space * 14}┃')
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
                    command = input(f'\n{space * 5}Enter command: ')
                    break
                except KeyboardInterrupt:
                    error = True
                    break
            if error == True:
                raise KeyboardInterrupt
            if not command:
                system('clear')
                maze.generate()
                print(maze._display())
            elif command == '1':
                maze._show = False if maze._show else True
                if maze._animation:
                    maze._animation = False
                system('clear')
                maze.render()
                print(maze._display())
            elif command == '2':
                print(maze._themes[maze._mode][2])
                maze.theme_menu()
                while True:
                    try:
                        print(maze._themes[maze._mode][0])
                        theme_input = input(
                            (' ' * 18) + 'Chose your theme: ')
                        if not theme_input or theme_input == 'b':
                            break
                        if int(theme_input) <= 4:
                            maze._mode = int(theme_input)
                            break
                        else:
                            raise ValueError
                    except ValueError:
                        print('please enter valid input')
                    except KeyboardInterrupt:
                        raise KeyboardInterrupt
                if theme_input == 'b':
                    system('clear')
                    print(maze._display())
                    continue
                elif not theme_input:
                    system('clear')
                    maze._mode = 0
                    maze.render(update=True)
                    print(maze._display())
                else:
                    system('clear')
                    maze.render(update=True)
                    print(maze._display())

            elif command == '3':
                while True:
                    print('          ', end='')
                    wall_input = input(
                        'insert new wall type (enter for default): ')
                    if wall_input == '':
                        maze._wall = '█'
                        break
                    elif len(wall_input.strip()) != 1:
                        print('invalid wall type, ',
                              'only one character is accepted')
                        continue
                    else:
                        maze._wall = wall_input.strip()
                        break
                system('clear')
                maze.render(update=True) 
                print(maze._display())
            elif command == '4':
                while True:
                    while True:
                        print('          ', end='')
                        width_input = input(
                            'insert width: ')
                        if width_input == '':
                            break
                        try:
                            maze.width = int(width_input)
                            break
                        except ValueError as e:
                            print(e)
                            continue
                    while True:
                        print('          ', end='')
                        height_input = input(
                            'insert height: ')
                        if height_input == '':
                            break
                        try:
                            maze.height = int(height_input)
                            break
                        except ValueError as e:
                            print(e)
                            continue
                    if maze.width < 7 or maze.height < 5:
                        print(f"{RED}Error: Maze size too small for '42' pattern.{END}")
                        continue
                    maze.exit = (maze.width - 1, maze.height - 1)
                    maze._show = False
                    maze.generate()
                    print(maze._display())
                    break
            elif command == '5':
                maze.save()
                system('clear')
                maze.render(update=True)
                print(maze._display())
            elif command == '6':
                maze.play()
                system('clear')
                print(maze._display())
                maze._bfs(maze.entry, maze.exit)
            elif command == '7':
                maze._animation = False if maze._animation else True
                if maze._show:
                    maze._show = False
                system('clear')
                print(maze._display())
                continue
            elif command == 'q':
                print('Program closed')
                return
            else:
                print('please enter valid input')
    
    except Exception as e:
        print(e)
    except KeyboardInterrupt:
        print('\nCtrl+c detected: Program closed', end='')

if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.stderr.write(f'Usage: python3 {sys.argv[0]} <file.txt>')
        sys.exit()
    parsed = Parsing()
    try:
        parsed.parse(sys.argv[1])
    except Exception as e:
        print(e, end='')
        sys.exit()
    run()