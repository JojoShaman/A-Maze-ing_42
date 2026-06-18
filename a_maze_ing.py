from mazegen.generator import MazeGenerator
from typing import Any
import sys

class Parsing():
    def __init__(self) -> None:
        self._width: int = 0
        self._height: int = 0
        self._entry: tuple[int, int] = (0, 0)
        self._exit: tuple[int, int] = (0, 0)
        self._output_file: str = ""
        self._perfect: bool = False
        self._algorythm: str = ""

    def parse(self, file: str) -> None:
        with open(file, 'r') as f:
            content = f.read()
        lines = [l for l in content.splitlines() if l.strip() and not l.startswith('#')]
        params: dict = {key : value for key, value in (line.split('=') for line in lines)}
        self._width = int(params['WIDTH'])
        self._height = int(params['HEIGHT'])
        self._entry = tuple(params['ENTRY'].split(','))
        self._exit = tuple(params['EXIT'].split(','))
        self._output_file = params['OUTPUT_FILE']
        self._perfect = bool(params['PERFECT'] == True)
        self._algorythm = params['ALGORYTHM']


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.stderr.write(f'Usage: python3 {sys.argv[0]} <file.txt>')
        sys.exit()
    parsed = Parsing()
    parsed.parse(sys.argv[1])
    x, y = parsed._exit
    print(isinstance(x, int)) #needs fix
    