import unittest
from parameterized import parameterized

from player import Player


class PlayerTest(unittest.TestCase):
    @parameterized.expand([
        ["Simple NORTH", (0, 0), "N", "(0, 0), NORTH"],
        ["Simple SOUTH", (0, 0), "S", "(0, 0), SOUTH"],
        ["Simple EAST", (0, 0), "E", "(0, 0), EAST"],
        ["Simple WEST", (0, 0), "W", "(0, 0), WEST"],
        ["Incorrect Direction", (0, 0), "Q", "(0, 0), NORTH"],
    ])
    def test_player_creation(self, name, pos, direction, expected):
        p = Player(pos, direction)
        assert str(p) == expected


if __name__ == '__main__':
    unittest.main()
