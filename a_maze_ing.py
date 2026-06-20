from mazegen.generator import MazeGenerator
from mazegen.parsing import Parsing
import sys


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.stderr.write(f'Usage: python3 {sys.argv[0]} <file.txt>')
        sys.exit()
    parsed = Parsing()
    try:
        parsed.parse(sys.argv[1])
    except Exception as e:
        print(e, end='')
        exit()
    
    maze = MazeGenerator(parsed)
    try:
        maze.generate()
    except Exception as e:
        print(e)