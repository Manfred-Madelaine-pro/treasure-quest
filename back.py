import logging as log
from enum import Enum
from collections import namedtuple

Cell = namedtuple("Cell", ["i", "j"])


class CellType(Enum):
    PLAIN = 1
    MOUNTAIN = 2


class Map:

    def __init__(self, width, height, mountains=[], treasures=[]):
        self.width = width if width >= 0 else 0
        self.height = height if height >= 0 else 0

        self.grid = {}
        self.treasures = {}

        self.create_map(mountains)
        self.handle_treasures(treasures)

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
        """
        Creates the map based on the width and height stored in the instance while handling the mountains.
        :param mountains: List of mountains coordinates which should be present on the map, example [(0, 0), (0, 1)]
        """
        for i in range(self.width):
            for j in range(self.height):
                self.grid[Cell(i, j)] = CellType.MOUNTAIN if (i, j) in mountains else CellType.PLAIN

    def handle_treasures(self, treasures):
        for x, y, treasures_amount in treasures:
            if (x, y) in self.grid and self.grid[(x, y)] is not CellType.MOUNTAIN:
                if treasures_amount < 1:
                    log.debug(f"Trying to set treasures on cell({(x, y)}) but amount is invalid (amount={treasures_amount}).")
                elif self.treasures.get((x, y)):
                    log.debug(f"Treasures already set for cell({(x, y)}). Skipping treasure's definition.")
                else:
                    self.treasures[(x, y)] = treasures_amount

    def get_mountains_count(self):
        return sum([self.grid[Cell(i, j)] == CellType.MOUNTAIN for i in range(self.width) for j in range(self.height)])

    def get_treasures_count(self):
        return sum([treasures for treasures in self.treasures.values()])


if __name__ == "__main__":
    m = Map(3, 4)
    print(m)
