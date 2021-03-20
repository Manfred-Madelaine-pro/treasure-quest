import unittest
from parameterized import parameterized

from src.player import Player


class PlayerTest(unittest.TestCase):
    @parameterized.expand([
        ["Player facing NORTH", (0, 0), "N", "(0, 0), NORTH"],
        ["Player facing SOUTH", (0, 0), "S", "(0, 0), SOUTH"],
        ["Player facing EAST", (0, 0), "E", "(0, 0), EAST"],
        ["Player facing WEST", (0, 0), "W", "(0, 0), WEST"],
        ["Player facing WEST (FR)", (0, 0), "O", "(0, 0), WEST"],
        ["Incorrect Direction", (0, 0), "Q", "(0, 0), NORTH"],
    ])
    def test_player_creation(self, name, pos, direction, expected):
        p = Player("Lara", pos, direction)
        assert str(p) == expected

    @parameterized.expand([
        ["Simple step to the NORTH", (2, 0), "N", "(1, 0), NORTH"],
        ["Simple step to the SOUTH", (1, 0), "S", "(2, 0), SOUTH"],
        ["Simple step to the EAST", (0, 1), "E", "(0, 2), EAST"],
        ["Simple step to the WEST", (0, 2), "W", "(0, 1), WEST"],
    ])
    def test_player_movements(self, name, pos, direction, expected):
        p = Player("Lara", pos, direction)
        p.move()
        assert str(p) == expected

    @parameterized.expand([
        ["Change on the Right when facing NORTH", (1, 0), "N", "R", "(1, 0), EAST"],
        ["Change on the Left when facing NORTH", (1, 0), "N", "L", "(1, 0), WEST"],
        ["Change on the Right when facing SOUTH", (1, 0), "S", "R", "(1, 0), WEST"],
        ["Change on the Left when facing SOUTH", (1, 0), "S", "L", "(1, 0), EAST"],
        ["Change on the Right when facing EAST", (1, 0), "E", "R", "(1, 0), SOUTH"],
        ["Change on the Left when facing EAST", (1, 0), "E", "L", "(1, 0), NORTH"],
        ["Change on the Right when facing WEST", (1, 0), "W", "R", "(1, 0), NORTH"],
        ["Change on the Left when facing WEST", (1, 0), "W", "L", "(1, 0), SOUTH"],
        ["Keep direction unchanged when incorrect orientation", (1, 0), "S", "Q", "(1, 0), SOUTH"],
    ])
    def test_player_orientation_changes(
            self, name, pos, direction, orientation_change, expected
    ):
        p = Player("Lara", pos, direction)
        p.turn(orientation_change)
        assert str(p) == expected

    @parameterized.expand([
        ["Face NORTH, Move, Turn Right and Move again", (1, 0), "N", "R", "(0, 1), EAST"],
        ["Face EAST, Move, Turn Right and Move again", (0, 0), "E", "R", "(1, 1), SOUTH"],
        ["Face SOUTH, Move, Turn Right and Move again", (0, 1), "S", "R", "(1, 0), WEST"],
        ["Face WEST, Move, Turn Right (FR) and Move again", (1, 1), "W", "D", "(0, 0), NORTH"],
        ["Face WEST, Move, Turn Left (FR) and Move again", (1, 1), "W", "G", "(2, 0), SOUTH"]
    ])
    def test_player_orientation_changes_and_movements(
            self, name, pos, direction, orientation_change, expected
    ):
        p = Player("Lara", pos, direction)
        p.move()
        p.turn(orientation_change)
        p.move()
        assert str(p) == expected


if __name__ == "__main__":
    unittest.main()
