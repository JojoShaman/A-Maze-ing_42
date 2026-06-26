from mazegen.generator import MazeGenerator
from mazegen.parsing import Parsing
from mazegen.colors import RED, END
import sys
from os import system
from time import sleep
from mazegen import menu

def run() -> None:
    maze = MazeGenerator(parsed)
    try:
        error = False
        try:
            maze.generate()
            print(maze._display())
        except Exception as e:
            raise (e)
        while True:
            while True:
                show_hide = 'hide path' if maze._show else 'show path'
                animation = 'Turn off' if maze._animation else 'Turn on'
                try:
                    menu.user(maze, show_hide, animation)
                    command = input(f'\n{' ' * 5}Enter command: ')
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
            elif command == '0':
                menu.algo(maze.algorythm, maze._themes[maze._mode][2])
                while True:
                    print(maze._themes[maze._mode][0])
                    algo_input = input(
                        (' ' * 20) + 'Chose your generator: ')
                    if (algo_input == '0' or
                        algo_input == '1' or
                        algo_input == 'b'):
                        break
                    else:
                        print('please enter valid input')
                if algo_input == '0':
                    maze.algorythm = (
                        'dfs' if maze.algorythm == 'prim' else 'dfs')
                elif algo_input == '1':
                    maze.algorythm = (
                        'prim' if maze.algorythm == 'dfs' else 'prim')
                elif algo_input == 'b':
                    ...
                system('clear')
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
                menu.theme()
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
                system('clear')
                if theme_input == 'b':
                    print(maze._display())
                    continue
                elif not theme_input:
                    maze._mode = 0
                    maze.render(update=True)
                else:
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
                gm: dict = {
                    '0': 'easy',
                    '1': 'hard'
                }
                menu.game_mode(maze._themes, maze._mode)
                while True:
                    try:
                        game_mode_input = input(
                                    (' ' * 18) + 'Chose your gaming mode: ')
                        if (game_mode_input == '0' or
                            game_mode_input == '1' or
                            game_mode_input == 'b'):
                            break
                        else:
                            print('please enter valid input')
                    except KeyboardInterrupt:
                        raise KeyboardInterrupt
                if game_mode_input == 'b':
                    system('clear')
                    print(maze._display())
                    continue
                maze.play(mode=gm[game_mode_input])
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