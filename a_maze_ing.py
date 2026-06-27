from mazegen.generator import MazeGenerator
from mazegen.parsing import Parsing
from mazegen.colors import _theme
import sys
from os import system
from mazegen import menu


def run() -> None:
    maze = MazeGenerator(parsed)
    try:
        try:
            maze.generate()
            print(maze._display())
        except Exception as e:
            raise (e)
        while True:
            show_hide = 'Hide path' if maze._show else 'Show path'
            animation = 'Turn off' if maze._animation else 'Turn on'
            try:
                menu.user(maze, show_hide, animation)
                command = input(f'\n{' ' * 5}Enter command: ')
            except KeyboardInterrupt:
                raise KeyboardInterrupt
            if not command:
                system('clear')
                maze.generate()
                print(maze._display())
            elif command == '0':
                menu.algo(maze.algorythm, _theme[maze._mode][2])
                while True:
                    print(_theme[maze._mode][0])
                    algo_input = input(
                        (' ' * 20) + 'Chose your generator: ')
                    if (algo_input == '0' or
                        algo_input == '1' or
                        algo_input == 'b' or
                            not algo_input):
                        break
                    else:
                        print('please enter valid input')
                if algo_input == '0':
                    maze.algorythm = (
                        'dfs' if maze.algorythm == 'prim' else 'dfs')
                elif algo_input == '1':
                    maze.algorythm = (
                        'prim' if maze.algorythm == 'dfs' else 'prim')
                elif algo_input == 'b' or not algo_input:
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
                print(_theme[maze._mode][2])
                menu.theme()
                while True:
                    try:
                        print(_theme[maze._mode][0])
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
                maze.save()
                system('clear')
                maze.render(update=True)
                print(maze._display())
            elif command == '5':
                maze.save_hex()
                system('clear')
                maze.render(update=True)
                print(maze._display())
            elif command == '6':
                gm: dict = {
                    '0': 'easy',
                    '1': 'hard'
                }
                menu.game_mode(maze._mode, maze._g_mode)
                while True:
                    try:
                        gm_input = input(
                                    (' ' * 5) +
                                    'Choose your gaming mode '
                                    'or press ENTER to start: ')
                        if (gm_input == '0' or
                            gm_input == '1' or
                            gm_input == 'b' or
                                not gm_input):
                            break
                        else:
                            print('please enter valid input')
                    except KeyboardInterrupt:
                        raise KeyboardInterrupt
                if gm_input == 'b':
                    system('clear')
                    print(maze._display())
                    continue
                if gm_input:
                    maze._g_mode = gm[gm_input]
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
