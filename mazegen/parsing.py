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
        x, y = (int(a) for a in params['ENTRY'].split(','))
        self._entry = (x, y)
        x, y = (int(a) for a in params['EXIT'].split(','))
        self._exit = (x, y)
        self._output_file = params['OUTPUT_FILE']
        self._perfect = bool(params['PERFECT'] == True)
        self._algorythm = params['ALGORYTHM']