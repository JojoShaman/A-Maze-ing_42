from .colors import RED, END
from typing import Any


class Parsing():
    """Store parsed data from configuration file.

    Attributes:
        _width: number of columns in the maze.
        _height: number of rows in the maze.
        _entry: coordinates of the maze entry point.
        _exit: coordinates of the maze exit point.
        _output_file: path to the output file.
        _perfect: whether the has a unique path between entry and exit.
        _algorithm: generation algorithm ('dfs' or 'prim').
        _seed: optional seed for reproducible generation.
    """
    def __init__(self) -> None:
        self._width: int = 0
        self._height: int = 0
        self._entry: tuple[int, int] = (0, 0)
        self._exit: tuple[int, int] = (0, 0)
        self._output_file: str = ""
        self._perfect: bool = False
        self._algorithm: str = ""
        self._seed: int = 0

    def parse(self, file: str) -> None:
        """Parse the configuration file parameters with error management.

        Args:
            file: path to configuration file."""
        errors: list[Any] = []
        with open(file, 'r') as f:
            content = f.read()
        lines: list[str] = [line for line in content.splitlines() if
                            line.strip() and not line.startswith('#')]
        p: dict[str, str] = {key: value for key, value in
                             (line.split('=')for line in lines)}
        try:
            self._width = int(p['WIDTH'])
            if self._width < 0:
                errors.append(ValueError('width should not be negative'))
            if self._width < 7:
                raise Exception(
                    f"{RED}Error: Maze size too small for '42' pattern.{END}")
        except ValueError as e:
            errors.append(e)
        try:
            self._height = int(p['HEIGHT'])
            if self._height < 0:
                errors.append(ValueError('height should not be negative'))
            if self._height < 5:
                raise Exception(
                    f"{RED}Error: Maze size too small for '42' pattern.{END}")
        except ValueError as e:
            errors.append(e)
        try:
            x, y = (int(pos) for pos in p['ENTRY'].split(','))
            if (x >= 0 and x < self._width) and (y >= 0 and y < self._height):
                self._entry = (x, y)
            else:
                errors.append(
                    ValueError('entry coordinates are out of bounds'))
        except ValueError as e:
            errors.append(e)
        try:
            x, y = (int(pos) for pos in p['EXIT'].split(','))
            if ((x >= 0 and x < self._width) and
                    (y >= 0 and y < self._height)):
                self._exit = (x, y)
            else:
                errors.append(
                    ValueError('exit coordinates are out of bounds'))
        except ValueError as e:
            errors.append(e)
        self._output_file = p['OUTPUT_FILE']
        if p['PERFECT'] == 'True' or p['PERFECT'] == 'False':
            self._perfect = p['PERFECT'] == 'True'
        else:
            errors.append(ValueError(f"Incorrect value '{p['PERFECT']}'"
                                     + " for variable 'PERFECT'"))
        if p['ALGORITHM'] == 'dfs' or p['ALGORITHM'] == 'prim':
            self._algorithm = p['ALGORITHM']
        else:
            errors.append(f"Error: {p['ALGORITHM']} algorithm not found")
        if p.get('SEED'):
            try:
                self._seed = int(p['SEED'])
            except ValueError:
                errors.append(ValueError(f"Incorrect value '{p['SEED']}'"
                                         + " for variable 'SEED'"))
        if errors:
            error: str = ''
            for err in errors:
                error += f'{type(err).__name__} : {str(err)}\n'
            raise Exception(error)
