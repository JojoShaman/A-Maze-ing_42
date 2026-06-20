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
        errors: list = []
        with open(file, 'r') as f:
            content = f.read()
        lines: list = [l for l in content.splitlines() if
                 l.strip() and not l.startswith('#')]
        p: dict = {key : value for key, value in
                   (line.split('=')for line in lines)}
        try:
            self._width = int(p['WIDTH'])
            if self._width < 0:
                errors.append(ValueError('width should not be negative'))
        except ValueError as e:
            errors.append(e)
        try:
            self._height = int(p['HEIGHT'])
            if self._height < 0:
                errors.append(ValueError('height should not be negative'))
        except ValueError as e:
            errors.append(e)
        try:
            x, y = (int(pos) for pos in p['ENTRY'].split(','))
            if (x >= 0 and x < self._width) and (y >= 0 and y < self._height):
                self._entry = (x, y)
            else:
                errors.append(ValueError('entry coordinates are out of bounds'))
        except ValueError as e:
            errors.append(e)
        try:
            x, y = (int(pos) for pos in p['EXIT'].split(','))
            if (x >= 0 and x < self._width) and (y >= 0 and y < self._height):
                self._exit = (x, y)
            else:
                errors.append(ValueError('exit coordinates are out of bounds'))
        except ValueError as e:
            errors.append(e)
        self._output_file = p['OUTPUT_FILE']
        if p['PERFECT'] == 'True' or p['PERFECT'] == 'False':
            self._perfect = bool(p['PERFECT'] == True)
        else:
            errors.append(ValueError(f"Incorrect value '{p['PERFECT']}'"
                        + " for variable 'PERFECT'"))
        if p['ALGORYTHM'] == 'dfs' or p['ALGORYTHM'] == 'prims':
            self._algorythm = p['ALGORYTHM']
        else:
            errors.append(f"Error: {p['ALGORYTHM']} algorythm not found")
        if errors:
            error: str = ''
            for err in errors:
                error += f'{type(err).__name__} : {str(err)}\n'
            raise Exception(error)
