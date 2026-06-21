from mazegen.generator import MazeGenerator
from mazegen.parsing import Parsing
from mazegen.colors import RED, END
import sys

def run() -> None:
    maze = MazeGenerator(parsed)
    try:
        error = False
        try:
            maze._dfs()
        except Exception as e:
            raise (e)
        maze._bfs(maze.entry, maze.exit)
        maze.render()
        while True:
            while True:
                show_hide = 'hide path' if maze._show else 'show path'
                try:
                    print(f'\n{maze._themes[maze._mode][0]}', end='')
                    print('enter: regenerate maze')
                    print(f'1) {show_hide}')
                    print('2) maze theme')
                    print('3) change wall type')
                    print('4) change maze size')
                    print('-' * 10)
                    print('q: quit')
                    command = input('\nEnter command: ')
                    break
                except KeyboardInterrupt:
                    error = True
                    break
            if error == True:
                raise KeyboardInterrupt
            if not command:
                maze.generate()
            elif command == '1':
                maze._show = False if maze._show else True
                maze.render()
            elif command == '2':
                print(maze._themes[maze._mode][2])
                maze.theme_menu()
                while True:
                    try:
                        print(maze._themes[maze._mode][0])
                        theme_input = input(
                            (' ' * 10) + 'Chose your theme: ')
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
                    continue
                elif not theme_input:
                    maze.render()
                    maze._mode = 0
                else:
                    maze.render()
            elif command == '3':
                while True:
                    print('          ', end='')
                    wall_input = input(
                        'insert new wall type (enter for default): ')
                    if wall_input == '':
                        break
                    elif len(wall_input) != 1:
                        print('invalid wall type, ',
                              'only one character is accepted')
                        continue
                    else:
                        maze._wall = wall_input
                        break
                maze.render() 
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
                    maze.generate()
                    break
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