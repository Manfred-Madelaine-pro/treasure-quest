from enum import Enum


class Direction(Enum):
    EAST = (0, 1),
    WEST = (1, 0),
    NORTH = (-1, 0),
    SOUTH = (0, -1)


CHAR_TO_DIRECTION = {
    "N": Direction.NORTH,
    "S": Direction.SOUTH,
    "E": Direction.EAST,
    "W": Direction.WEST,
}


class RelativeDirection(Enum):
    RIGHT = 1
    LEFT = -1


DIRECTIONS_CLOCKWISE = [Direction.NORTH, Direction.EAST, Direction.SOUTH, Direction.WEST]


class Player:
    def __init__(self, pos, direction):
        self.pos = pos
        self.direction = CHAR_TO_DIRECTION.get(direction, Direction.NORTH)

    def __str__(self):
        return f"{self.pos}, {self.direction.name}"

    def move(self):
        self.pos = self.pos + self.direction

    def turn(self, relative_direction):
        """
        Allows to turn clockwise or anticlockwise (i.e. to the right or the left).

        :param relative_direction: either left or right
        :return: new direction (North, South, East, West).
        """
        dir_index = DIRECTIONS_CLOCKWISE.index(self.direction)
        new_dir_index = (dir_index + relative_direction) % len(DIRECTIONS_CLOCKWISE)
        return DIRECTIONS_CLOCKWISE[new_dir_index]
