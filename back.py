from collections import namedtuple
from enum import Enum

Cell = namedtuple("Cell", ["i", "j"])


class CellType(Enum):
    PLAIN = 1
    MOUNTAIN = 2


class Map:
    grid = {}

    def __init__(self, width, height, mountains=[]):
        self.width = width if width >= 0 else 0
        self.height = height if height >= 0 else 0

        self.create_map(mountains)

    def __str__(self):
        mountain_char = "/\\"
        plain_char = ",,"

        txt = ""
        for i in range(self.width):
            txt += "\n"
            for j in range(self.height):
                txt += plain_char if self.grid[(i, j)] == CellType.PLAIN else mountain_char

        return "The Madre de Dios Map !" + txt

    def create_map(self, mountains):
        for i in range(self.width):
            for j in range(self.height):
                self.grid[Cell(i, j)] = CellType.MOUNTAIN if (i, j) in mountains else CellType.PLAIN

    def get_mountains_count(self):
        m_count = 0
        for i in range(self.width):
            for j in range(self.height):
                m_count += self.grid[Cell(i, j)] == CellType.MOUNTAIN
        return m_count


if __name__ == "__main__":
    m = Map(3, 4)
    print(m)
