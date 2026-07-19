class Pixel:
    """Store a character and it's background.

    Attributes:
        px: visual represention of the pixel.
        bg: visual represention of the background of the pixel.
    """
    def __init__(self) -> None:
        self.px: str = ''
        self.bg: str = ''

    def render_helper(self) -> str:
        """Return a string with the background and the character of a pixel.

        Returns:
            str: concatenated string with the background and
            the character of the pixel
        """
        return self.bg + self.px


class Cell:
    """Store the data of a single maze cell.

    Attributes:
        walls: dict of wall states for each cardinal direction.
        visited: whether the cell has been visited during the generation.
        static: whether the cell is part of the 42 pattern.
        matrix: 3x3 grid of Pixel objects for rendering.
        x: column position in the maze grid.
        y: row position in the maze grid.
    """
    def __init__(self) -> None:
        self.walls: dict[str, bool] = {
            'W': True, 'S': True, 'E': True, 'N': True}
        self.visited: bool = False
        self.static: bool = False
        self.matrix: list[list[Pixel]] = []
        self.x: int = 0
        self.y: int = 0

    def get_binary(self) -> str:
        """Return the binary represation of the cell's walls.

        Returns:
            str: binary string where each bit represents a wall (W, S, E, N)
        """
        value: list[int] = [int(x) for x in self.walls.values()]
        binary: str = ''.join([str(x) for x in value])
        return (binary)

    def neighbors(self) -> dict[str, tuple[int, int]]:
        """Return each cardinal position of the cell's neighbors.

        Returns:
            dict[str, tuple[int, int]]: a dict with each the cell's neighbors
            and their position.
        """
        return {
            'NORTH': (self.x, self.y-1),
            'EAST': (self.x+1, self.y),
            'SOUTH': (self.x, self.y+1),
            'WEST': (self.x-1, self.y),
        }
