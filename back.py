import logging as log
from collections import namedtuple
from enum import Enum

from player import Player, CHAR_TO_RELATIVE_DIRECTION, DIRECTION_TO_CHAR

Cell = namedtuple("Cell", ["i", "j"])


class CellType(Enum):
    PLAIN = 1
    MOUNTAIN = 2


class TreasureMap:
    def __init__(self, width, height, mountains=[], treasures=[], players=[]):
        self.width = width if width >= 0 else 0
        self.height = height if height >= 0 else 0

        self.grid = {}
        self.mountains = mountains
        self.treasures = {}
        self.players = {}

        self.iteration = 0
        self.turns = 0

        self.create_map(mountains)
        self.add_treasures(treasures)
        self.add_players(players)

    def __str__(self):
        """
        Represents all the plains, mountains, treasures and players present on an ASCII art version's of the map !

        :return: The map visualization on ASCII art
        """
        mountain_char = "/V\\"
        plain_char = ",,,"
        player_char = "\\o/ "

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
                player = player_char if self.is_occupied((i, j)) else ""
                txt += player or (foreground or background) + " "
            txt += "\n"

        return "The Madre de Dios Treasure Quest !" + txt

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

        :param treasures: List of tuples representing players (example: [(1, 1, 3)])
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

    def add_players(self, players):
        """
        Creates a dictionary of :
            - key: The players
            - Value: All player's movements (example: "AADAGA")

        :param players: List of tuples representing players (example: [("Lara", 1, 1, "S", "AA")])
        """
        for name, x, y, direction, movements in players:
            if self.is_accessible(position=(x, y)) and not self.is_occupied(
                    position=(x, y)
            ):
                player = Player(name, (x, y), direction)
                self.players[player] = movements
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

    # ----- Core ---------

    def play(self):
        import os, time
        clear = lambda: os.system('clear')
        clear()

        while self.turns > 0:
            self.next()
            print(self)
            time.sleep(0.5)
            clear()

            self.turns -= 1

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
                log.info(
                    f"{player.name} turns to the {CHAR_TO_RELATIVE_DIRECTION.get(next_movement).name}"
                )

    def handle_player_moves(self, player):
        next_pos = player.get_next_pos()

        if self.is_accessible(next_pos) and not self.is_occupied(next_pos):
            log.info(f"{player.name} moves to the {player.direction.name}.")
            player.move()

            if self.treasures.get(next_pos):
                self.treasures[next_pos] -= 1
                player.collected_treasures += 1
                if self.treasures[next_pos] == 0:
                    self.treasures.pop(next_pos)

    def is_occupied(self, position):
        return position in [player.pos for player in self.players.keys()]

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

    def get_players_count(self):
        return len(self.players)

    def get_data(self):
        return {
            "Map": (self.width, self.height),
            "Mountains": self.mountains,
            "Treasures": [(k, v) for k, v in self.treasures.items()],
            "Players": [(player.name, player.pos, DIRECTION_TO_CHAR[player.direction], player.collected_treasures) for
                        player, _ in self.players.items()]
        }


if __name__ == "__main__":
    w, h = 3, 4
    mtn = [(1, 1), (2, 2)]
    tsr = [(0, 3, 2), (1, 3, 1)]
    plyr = [("Lara", 1, 1, "S", "AA")]
    tm = TreasureMap(width=w, height=h, mountains=mtn, treasures=tsr, players=plyr)
    print(tm)
