from enum import Enum


class Direction(Enum):
    NORTH = (-1, 0)
    SOUTH = (1, 0)
    EAST = (0, 1)
    WEST = (0, -1)


CHAR_TO_DIRECTION = {
    "N": Direction.NORTH,
    "S": Direction.SOUTH,
    "E": Direction.EAST,
    "W": Direction.WEST,
    "O": Direction.WEST,
}

DIRECTION_TO_CHAR = {
    Direction.NORTH: "N",
    Direction.SOUTH: "S",
    Direction.EAST: "E",
    Direction.WEST: "O",
}


class RelativeDirection(Enum):
    RIGHT = 1
    LEFT = -1


CHAR_TO_RELATIVE_DIRECTION = {
    "L": RelativeDirection.LEFT,
    "G": RelativeDirection.LEFT,
    "R": RelativeDirection.RIGHT,
    "D": RelativeDirection.RIGHT,
}

DIRECTIONS_CLOCKWISE = [
    Direction.NORTH,
    Direction.EAST,
    Direction.SOUTH,
    Direction.WEST,
]


class Adventurer:
    def __init__(self, name, pos, direction):
        self.name = name
        self.pos = pos
        self.direction = CHAR_TO_DIRECTION.get(direction, Direction.NORTH)

        self.collected_treasures = 0

    def __str__(self):
        return f"{self.pos}, {self.direction.name}"

    def move(self):
        """
        Moves the adventurer in the direction he is facing, i.e. (North, South, East, West).
        """
        self.pos = self.get_next_pos()

    def get_next_pos(self):
        """
        It simply sums the current position with the direction's value in order to define the adventurer's next position.

        :return: The next position coordinates.
        """
        return tuple(map(sum, zip(self.pos, self.direction.value)))

    def turn(self, relative_direction_char):
        """
        Turns the adventurer clockwise or anticlockwise (i.e. to the right or to the left).

        :param relative_direction_char: either left or right ("L" or "R")
        :return: new direction (North, South, East, West).
        """
        relative_direction = CHAR_TO_RELATIVE_DIRECTION.get(relative_direction_char)
        if not relative_direction:
            return

        dir_index = DIRECTIONS_CLOCKWISE.index(self.direction)
        new_dir_index = (dir_index + relative_direction.value) % len(
            DIRECTIONS_CLOCKWISE
        )
        self.direction = DIRECTIONS_CLOCKWISE[new_dir_index]

    def pickup_treasure(self):
        self.collected_treasures += 1


if __name__ == "__main__":
    p = (0, 0)
    lara = Adventurer("Lara", p, "E")
    print(lara)

    actions = "ADAAGAGA"
    for a in actions:
        if a == "A":
            print(f"{lara.name} moves to the {lara.direction.name}.")
            lara.move()
            print(lara)  # (2, 1)
        else:
            print(f"{lara.name} turns to the {CHAR_TO_RELATIVE_DIRECTION.get(a).name}")
            lara.turn(a)
