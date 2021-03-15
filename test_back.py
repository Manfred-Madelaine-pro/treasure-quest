import unittest
from parameterized import parameterized

from back import TreasureMap


class TreasureMapTest(unittest.TestCase):
    @parameterized.expand([
        ["No map", 0, 0, (0, 0)],
        ["Small map", 1, 1, (1, 1)],
        ["Normal map", 3, 4, (3, 4)],
        ["Big map", 10, 20, (10, 20)],
        ["Impossible map", -1, -4, (0, 0)],
    ])
    def test_map_creation(self, name, width, height, expected):
        treasure_map = TreasureMap(width, height)
        assert (treasure_map.width, treasure_map.height) == expected

    @parameterized.expand([
        ["Normal map with no mountains", 3, 4, 0],
    ])
    def test_map_creation_with_only_plains(self, name, width, height, expected):
        treasure_map = TreasureMap(width, height)
        assert treasure_map.get_mountains_count() == expected

    @parameterized.expand([
        ["Normal map with 1 mountain", 3, 4, [(0, 0)], 1],
        ["Normal map with 2 mountains", 3, 4, [(0, 0), (1, 1)], 2],
        ["Ignore mountain creation when on same cell as another mountain", 3, 4, [(1, 1), (1, 1)], 1],
        ["Out of bound mountain in Positives", 3, 4, [(8, 8)], 0],
        ["Out of bound mountain in Positive for one coordinate", 3, 4, [(2, 8)], 0],
        ["Out of bound mountain in Negatives", 3, 4, [(-1, -1)], 0],
    ])
    def test_map_creation_with_plains_and_mountains(self, name, width, height, mountains, expected):
        treasure_map = TreasureMap(width, height, mountains)
        assert treasure_map.get_mountains_count() == expected

    @parameterized.expand([
        ["Normal map with 1 treasure", 3, 4, [(0, 0, 1)], 1],
        ["Normal map with 2 treasures on different cells", 3, 4, [(0, 0, 1), (1, 1, 1)], 2],
        ["Normal map with 3 treasure in one cell", 3, 4, [(0, 0, 3)], 3],
        ["Incorrect treasure amount (0)", 3, 4, [(0, 0, 0)], 0],
        ["Incorrect treasure amount (-3)", 3, 4, [(0, 0, -3)], 0],
        ["Ignore treasure's duplication (1 new)", 3, 4, [(0, 0, 1), (0, 0, 1)], 1],
        ["Ignore treasure's duplication (2 news)", 3, 4, [(0, 0, 1), (0, 0, 2), (0, 0, 3)], 1],
        ["Out of bound treasure in Positives", 3, 4, [(8, 8, 1)], 0],
        ["Out of bound treasure in Positive for one coordinate", 3, 4, [(2, 8, 2)], 0],
        ["Out of bound treasure in Negatives", 3, 4, [(-1, -1, 1)], 0],
    ])
    def test_map_creation_with_treasures(self, name, width, height, treasures, expected):
        treasure_map = TreasureMap(width, height, treasures=treasures)
        assert treasure_map.get_treasures_count() == expected

    @parameterized.expand([
        ["Normal map with 1 mountain and 1 treasure", 3, 4, [(0, 0)], [(0, 1, 1)], 1],
        ["Ignore treasure when on same cell as mountain", 3, 4, [(0, 0)], [(0, 0, 1)], 0],
    ])
    def test_map_creation_with_treasures_and_mountains(self, name, width, height, mountains, treasures, expected):
        treasure_map = TreasureMap(width, height, mountains, treasures)
        assert treasure_map.get_treasures_count() == expected

    @parameterized.expand([
        ["Add one player", 3, 4, [("Lara", 1, 1, "S", "AA")], 1],
        ["Add two players", 3, 4, [("Lara", 1, 1, "S", "AA"), ("Indiana", 2, 1, "S", "AA")], 2],
        ["Add two players on same cell", 3, 4, [("Lara", 1, 1, "S", "AA"), ("Indiana", 1, 1, "S", "AA")], 2],
        ["Add two players on same cell", 3, 4, [("Lara", 1, 1, "S", "AA"), ("Indiana", 1, 1, "S", "AA")], 2],
        ["Out of bound player in Positives", 3, 4, [("Lara", 10, 10, "S", "AA")], 0],
        ["Out of bound player in Positive for one coordinate", 3, 4, [("Lara", 1, 10, "S", "AA")], 0],
        ["Out of bound player in Negatives", 3, 4, [("Lara", -1, -1, "S", "AA")], 0],
    ])
    def test_map_and_players(self, name, width, height, players, expected):
        treasure_map = TreasureMap(width, height, players=players)
        assert treasure_map.get_players_count() == expected

    @parameterized.expand([
        ["Player moves on the map", 3, 4,  [("Lara", 1, 1, "E", "A")], "(2, 1), EAST"],
        ["Player tries to fall off the map's edge from the EAST", 1, 1, [("Lara", 0, 0, "E", "A")], "(0, 0), EAST"],
        ["Player tries to fall off the map's edge from the SOUTH", 1, 1, [("Lara", 0, 0, "S", "A")], "(0, 0), SOUTH"],
        ["Player tries to fall off the map's edge from the WEST", 1, 1, [("Lara", 0, 0, "W", "A")], "(0, 0), WEST"],
        ["Player tries to fall off the map's edge from the NORTH", 1, 1, [("Lara", 0, 0, "N", "A")], "(0, 0), NORTH"],
    ])
    def test_map_and_player_movements(self, name, width, height, players, expected):
        treasure_map = TreasureMap(width, height, players=players)
        treasure_map.next()
        assert str(list(treasure_map.players.keys())[0]) == expected

    @parameterized.expand([
        ["Add one player on mountain", 3, 4, [(0, 0)], [("Lara", 0, 0, "E", "AA")], 0],
    ])
    def test_map_and_player_with_mountains(self, name, width, height, mountains, players, expected):
        treasure_map = TreasureMap(width, height, mountains, players=players)
        assert treasure_map.get_players_count() == expected

    @parameterized.expand([
        ["Player is blocked by mountain on the EAST", 3, 4, [(1, 0)], [("Lara", 0, 0, "E", "A")], "(0, 0), EAST"],
        ["Player is blocked by mountain on the SOUTH", 3, 4, [(0, 1)], [("Lara", 0, 0, "S", "A")], "(0, 0), SOUTH"],
        ["Player is blocked by mountain on the WEST", 3, 4, [(0, 0)], [("Lara", 1, 0, "W", "A")], "(1, 0), WEST"],
        ["Player is blocked by mountain on the NORTH", 3, 4, [(0, 0)], [("Lara", 0, 1, "N", "A")], "(0, 1), NORTH"],
    ])
    def test_map_and_player_movements_with_mountains(self, name, width, height, mountains, players, expected):
        treasure_map = TreasureMap(width, height, mountains, players=players)
        treasure_map.next()
        assert str(list(treasure_map.players.keys())[0]) == expected

    @parameterized.expand([
        ["Player picks up a treasure", 3, 4, [(1, 0, 1)], [("Lara", 0, 0, "E", "A")], (1, 0)],
        ["Player picks up two treasures on different cells", 3, 4, [(1, 0, 1), (2, 0, 1)], [("Lara", 0, 0, "E", "AA")], (2, 0)],
        ["Player picks up two treasures on same cell", 3, 4, [(1, 0, 2)], [("Lara", 0, 0, "E", "AARRA")], (2, 0)],
        ["Player picks up two treasures on same cell", 3, 4, [(1, 0, 5)], [("Lara", 0, 0, "E", "AARRA")], (2, 3)],
    ])
    def test_map_and_players_with_treasures(self, name, width, height, treasures, players, expected):
        treasure_map = TreasureMap(width, height, treasures=treasures, players=players)
        treasure_map.next()
        treasure_map.next()
        treasure_map.next()
        treasure_map.next()
        treasure_map.next()
        p = list(treasure_map.players.keys())[0]
        picked_up, remaining = expected
        assert p.collected_treasures == picked_up
        assert treasure_map.get_treasures_count() == remaining


if __name__ == '__main__':
    unittest.main()
