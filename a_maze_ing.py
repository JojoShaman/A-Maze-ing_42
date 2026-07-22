from mazegen import MazeGenerator, Parsing, game
from mazegen.colors import THEMES
import sys
from os import system
from mazegen import menu, render, save, hex, display


def run() -> None:
    "Run the maze generator program."
    maze = MazeGenerator(parsed)
    try:
        try:
            maze.generate()
            print(display(maze))
        except Exception as e:
            raise (e)
        while True:
            show_hide = 'Hide path' if maze._show else 'Show path'
            animate = 'Turn off' if maze._animation else 'Turn on'
            perfect = 'imperfect' if maze.perfect else 'perfect'
            try:
                menu.user(maze, show_hide, animate, perfect)
                command = input(f'\n{" " * 5}Enter command: ')
            except KeyboardInterrupt:
                raise KeyboardInterrupt
            if not command:
                system('clear')
                maze.generate()
                print(display(maze))
            elif command == '0':
                menu.algo(maze.algorithm, THEMES[maze._mode][2])
                while True:
                    print(THEMES[maze._mode][0])
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
                    maze.algorithm = (
                        'dfs' if maze.algorithm == 'prim' else 'dfs')
                elif algo_input == '1':
                    maze.algorithm = (
                        'prim' if maze.algorithm == 'dfs' else 'prim')
                elif algo_input == 'b' or not algo_input:
                    ...

                system('clear')
                print(display(maze))

            elif command == '1':
                maze._show = False if maze._show else True
                if maze._animation:
                    maze._animation = False
                system('clear')
                render(maze)
                print(display(maze))
            elif command == '2':
                print(THEMES[maze._mode][2])
                menu.show_themes()
                while True:
                    try:
                        print(THEMES[maze._mode][0])
                        THEMES_input = input(
                            (' ' * 18) + 'Chose your THEME: ')
                        if not THEMES_input or THEMES_input == 'b':
                            break
                        if int(THEMES_input) <= 4 and int(THEMES_input) > 0:
                            maze._mode = int(THEMES_input)
                            break
                        else:
                            raise ValueError
                    except ValueError:
                        print('please enter valid input')
                    except KeyboardInterrupt:
                        raise KeyboardInterrupt
                system('clear')
                if THEMES_input == 'b':
                    print(display(maze))
                    continue
                elif not THEMES_input:
                    maze._mode = 0
                    render(maze=maze, update=True)
                else:
                    render(maze=maze, update=True)
                print(display(maze))

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
                render(maze=maze, update=True)
                print(display(maze))
            elif command == '4':
                save(maze=maze)
                system('clear')
                render(maze=maze, update=True)
                print(display(maze))
            elif command == '5':
                hex(maze=maze, auto_save=False)
                system('clear')
                render(maze=maze, update=True)
                print(display(maze))
            elif command == '6':
                gm: dict[str, str] = {
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
                    print(display(maze))
                    continue
                if gm_input:
                    maze._g_mode = gm[gm_input]
                game.play(maze=maze)
                system('clear')
                print(display(maze))
                maze._bfs(maze.entry, maze.exit)
            elif command == '7':
                maze._animation = False if maze._animation else True
                if maze._show:
                    maze._show = False
                system('clear')
                print(display(maze))
                continue
            elif command == '8':
                maze.perfect = False if maze.perfect else True
                if maze._show:
                    maze._show = False
                system('clear')
                maze.generate()
                print(display(maze))
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
