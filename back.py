from enum import Enum
import logging as log
from collections import namedtuple

from player import Player, CHAR_TO_RELATIVE_DIRECTION

Cell = namedtuple("Cell", ["i", "j"])


class CellType(Enum):
    PLAIN = 1
    MOUNTAIN = 2


class TreasureMap:
    def __init__(self, width, height, mountains=[], treasures=[], players=[]):
        self.width = width if width >= 0 else 0
        self.height = height if height >= 0 else 0

        self.grid = {}
        self.treasures = {}
        self.players = {}

        self.create_map(mountains)
        self.add_treasures(treasures)
        self.add_players(players)

        self.iteration = 0

    def __str__(self):
        """
        Represents all the plains, mountains, treasures and players present on an ASCII art version's of the map !

        :return: The map visualization on ASCII art
        """
        mountain_char = "/\\,"
        plain_char = ",,,"

        txt = ""
        for i in range(self.width):
            txt += "\n\t"
            for j in range(self.height):
                background = plain_char if self.grid[(i, j)] is CellType.PLAIN else mountain_char
                foreground = f"[{str(self.treasures.get((i, j)))}]" if self.treasures.get((i, j)) else ''
                txt += foreground or background
            txt += "\n"

        return "The Madre de Dios Map !" + txt

    # ----- Initialization ---------

    def create_map(self, mountains):
        """
        Creates the map based on the width and height stored in the instance while handling the mountains.

        :param mountains: List of mountains coordinates which should be present on the map, example [(0, 0), (0, 1)]
        """
        for i in range(self.width):
            for j in range(self.height):
                self.grid[Cell(i, j)] = CellType.MOUNTAIN if (i, j) in mountains else CellType.PLAIN

    def add_treasures(self, treasures):
        """
        Creates a dictionary of :
            - key: treasures coordinates (example: (x, y))
            - Value: Amount of treasures available at this coordinate (amount > 0)

        :param treasures: List of tuples representing players (example: [(1, 1, 3)])
        """
        for x, y, treasures_amount in treasures:
            if self.is_accessible(position=(x, y)):
                if treasures_amount < 1:
                    log.debug(
                        f"Trying to set treasures on cell({(x, y)}) but amount is invalid (amount={treasures_amount}).")
                elif self.treasures.get((x, y)):
                    log.debug(f"Treasures already set for cell({(x, y)}). Skipping treasure's definition.")
                else:
                    self.treasures[(x, y)] = treasures_amount

    def add_players(self, players):
        """
        Creates a dictionary of :
            - key: The players
            - Value: All player's movements (example: "AADAGA")

        :param players: List of tuples representing players (example: [("Lara", 1, 1, "S", "AA")])
        """
        for name, x, y, direction, movements in players:
            if self.is_accessible(position=(x, y)):
                player = Player(name, (x, y), direction)
                self.players[player] = movements

    def is_accessible(self, position):
        """
        Checks the out of bound exception and the mountain ban (Mountains are forbidden cells).

        :param position: The requested position (i.e. a tuple made of two coordinates x and y)
        :return: True if position is accessible, False otherwise.
        """
        return position in self.grid and self.grid[position] is CellType.PLAIN

    # ----- Core ---------

    def next(self):
        for player, movements in self.players.items():
            if self.iteration >= len(movements):
                continue
            next_movement = movements[self.iteration]
            self.handle_player(player, next_movement)

        self.iteration += 1

    def handle_player(self, player, next_movement):
        if next_movement == "A":
            self.handle_player_moves(player)
        else:
            player.turn(next_movement)
            if CHAR_TO_RELATIVE_DIRECTION.get(next_movement):
                log.info(f"{player.name} turns to the {CHAR_TO_RELATIVE_DIRECTION.get(next_movement).name}")

    def handle_player_moves(self, player):
        next_pos = player.get_next_pos()

        if self.is_accessible(next_pos):
            log.info(f"{player.name} moves to the {player.direction.name}.")
            player.move()
            # pick up treasure
            if self.treasures.get(next_pos):
                self.treasures[next_pos] -= 1
                player.collected_treasures += 1

    # ----- Getters ---------

    def get_mountains_count(self):
        return sum([self.grid[Cell(i, j)] == CellType.MOUNTAIN for i in range(self.width) for j in range(self.height)])

    def get_treasures_count(self):
        return sum([treasures for treasures in self.treasures.values()])

    def get_players_count(self):
        return len(self.players)


if __name__ == "__main__":
    w, h = 3, 4
    mtn = [(1, 1), (2, 2)]
    tsr = [(0, 3, 2), (1, 3, 1)]
    plyr = [("Lara", 1, 1, "S", "AA")]
    tm = TreasureMap(width=w, height=h, mountains=mtn, treasures=tsr, players=plyr)
    print(tm)
