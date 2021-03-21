import random as rnd
import logging as log
from enum import Enum
from collections import namedtuple

from src.adventurer import Adventurer, CHAR_TO_RELATIVE_DIRECTION, DIRECTION_TO_CHAR

Cell = namedtuple("Cell", ["i", "j"])


class CellType(Enum):
    PLAIN = 1
    MOUNTAIN = 2


class TreasureMap:
    def __init__(self, width, height, mountains=[], treasures=[], adventurers=[]):
        self.width = width if width >= 0 else 0
        self.height = height if height >= 0 else 0

        self.grid = {}
        self.mountains = mountains
        self.treasures = {}
        self.adventurers = {}

        self.iteration = 0
        self.turns = 0

        self.create_map(mountains)
        self.add_treasures(treasures)
        self.add_adventurers(adventurers)

        self.initial_state = None

    def __str__(self):
        """
        Represents all the plains, mountains, treasures and adventurers present on an ASCII art version's of the map !

        :return: The map visualization on ASCII art
        """
        mountain_char = "/V\\"
        plain_char = ",,,"
        adventurer_char = "\\o/ "

        txt = ""
        for i in range(self.width):
            txt += "\n\t"
            for j in range(self.height):
                background = (
                    plain_char if self.grid[(i, j)] is CellType.PLAIN else mountain_char
                )
                foreground = (
                    f"[{str(self.treasures.get((i, j)))}]"
                    if self.treasures.get((i, j))
                    else ""
                )
                adventurer = adventurer_char if self.is_occupied((i, j)) else ""
                txt += adventurer or (foreground or background) + " "
            txt += "\n"

        leader_board = self.get_leader_board()

        return "The Madre de Dios Treasure Quest !" + txt + leader_board

    def get_leader_board(self):
        txt = f"\nTurn: {self.iteration:>3}"
        txt += f'\t\t\t\t\tTreasures: {self.get_treasures_count():>3}\n\n'
        txt += f'\t\t|\\/o\\/|   Leader Board   |\\/o\\/|\n'
        txt += "_".join([".:*~*:."] * 8) + "\n"
        for i, adventurer in zip(range(len(self.adventurers)), sorted(self.adventurers.keys(), key=lambda a: a.collected_treasures, reverse=True)):
            txt += f"#{i+1}\t" + str(adventurer) + "\n"

        return txt

    # ----- Initialization ---------

    def create_map(self, mountains):
        """
        Creates the map based on the width and height stored in the instance while handling the mountains.

        :param mountains: List of mountains coordinates which should be present on the map, example [(0, 0), (0, 1)]
        """
        for j in range(self.height):
            for i in range(self.width):
                self.grid[Cell(i, j)] = (
                    CellType.MOUNTAIN if (i, j) in mountains else CellType.PLAIN
                )

    def add_treasures(self, treasures):
        """
        Creates a dictionary of :
            - key: treasures coordinates (example: (x, y))
            - Value: Amount of treasures available at this coordinate (amount > 0)

        :param treasures: List of tuples representing adventurers (example: [(1, 1, 3)])
        """
        for x, y, treasures_amount in treasures:
            if self.is_accessible(position=(x, y)):
                if treasures_amount < 1:
                    log.debug(
                        f"Trying to set treasures on cell({(x, y)}) but amount is invalid (amount={treasures_amount})."
                    )
                elif self.treasures.get((x, y)):
                    log.debug(
                        f"Treasures already set for cell({(x, y)}). Skipping treasure's definition."
                    )
                else:
                    self.treasures[(x, y)] = treasures_amount

    def add_adventurers(self, adventurers):
        """
        Creates a dictionary of :
            - key: The adventurers
            - Value: All adventurer's movements (example: "AADAGA")

        :param adventurers: List of tuples representing adventurers (example: [("Lara", 1, 1, "S", "AA")])
        """
        for name, x, y, direction, movements in adventurers:
            if self.is_accessible(position=(x, y)) and not self.is_occupied(
                    position=(x, y)
            ):
                adventurer = Adventurer(name, (x, y), direction)
                self.adventurers[adventurer] = [c for c in movements]
                self.turns = (
                    len(movements) if self.turns < len(movements) else self.turns
                )

    def is_accessible(self, position):
        """
        Checks the out of bound exception and the mountain ban (Mountains are forbidden cells).

        :param position: The requested position (i.e. a tuple made of two coordinates x and y)
        :return: True if position is accessible, False otherwise.
        """
        return position in self.grid and self.grid[position] is CellType.PLAIN

    def update_initial_state(self):
        for adv in self.initial_state.adventurers.keys():
            self.initial_state.adventurers[adv] = self.get_adventurer(adv.name).previous_moves

    # ----- Core ---------

    def play(self):
        import os, time
        clear = lambda: os.system('clear')
        clear()

        while self.turns > 0 and self.treasures:
            self.next()
            print(self)
            time.sleep(0.5)
            clear()

            self.turns -= 1

    def next(self):
        for adventurer, movements in self.adventurers.items():
            if self.iteration >= len(movements):
                movements += get_random_move()
                # continue
            next_movement = movements[self.iteration]
            self.handle_adventurer(adventurer, next_movement)

        self.iteration += 1

    def handle_adventurer(self, adventurer, next_movement):
        if next_movement == "A":
            self.handle_adventurer_moves(adventurer)
        else:
            adventurer.turn(next_movement)
            if CHAR_TO_RELATIVE_DIRECTION.get(next_movement):
                log.info(
                    f"{adventurer.name} turns to the {CHAR_TO_RELATIVE_DIRECTION.get(next_movement).name}"
                )
        adventurer.previous_moves += [next_movement]

    def handle_adventurer_moves(self, adventurer):
        next_pos = adventurer.get_next_pos()

        if self.is_accessible(next_pos) and not self.is_occupied(next_pos):
            log.info(f"{adventurer.name} moves to the {adventurer.direction.name}.")
            adventurer.move()

            if self.treasures.get(next_pos):
                self.treasures[next_pos] -= 1
                adventurer.collected_treasures += 1
                if self.treasures[next_pos] == 0:
                    self.treasures.pop(next_pos)

    def is_occupied(self, position):
        return position in [adventurer.pos for adventurer in self.adventurers.keys()]

    # ----- Getters ---------

    def get_mountains_count(self):
        return sum(
            [
                self.grid[Cell(i, j)] == CellType.MOUNTAIN
                for i in range(self.width)
                for j in range(self.height)
            ]
        )

    def get_treasures_count(self):
        return sum([treasures for treasures in self.treasures.values()])

    def get_adventurers_count(self):
        return len(self.adventurers)

    def get_adventurer(self, name):
        for adv in self.adventurers.keys():
            if adv.name == name:
                return adv

    def get_data(self):
        return {
            "Map": (self.width, self.height),
            "Mountains": self.mountains,
            "Treasures": [(k, v) for k, v in self.treasures.items()],
            "adventurers": [(adventurer.name, adventurer.pos, DIRECTION_TO_CHAR[adventurer.direction],
                             adventurer.collected_treasures) for
                            adventurer, _ in self.adventurers.items()]
        }

    def get_initial_state(self):
        self.update_initial_state()
        return {
            "Map": (self.width, self.height),
            "Mountains": self.initial_state.mountains,
            "Treasures": [(k, v) for k, v in self.initial_state.treasures.items()],
            "adventurers": [(adventurer.name, (adventurer.pos[1], adventurer.pos[0]), DIRECTION_TO_CHAR[adventurer.direction],
                             "".join(moves)) for
                            adventurer, moves in self.initial_state.adventurers.items()]
        }


def get_random_move():
    return rnd.choice(["A", "A", "A", "L", "R"])


if __name__ == "__main__":
    w, h = 3, 4
    mtn = [(1, 1), (2, 2)]
    tsr = [(0, 3, 2), (1, 3, 1)]
    plyr = [("Lara", 1, 1, "S", "AA")]
    tm = TreasureMap(width=w, height=h, mountains=mtn, treasures=tsr, adventurers=plyr)
    print(tm)
