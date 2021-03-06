import unittest
from parameterized import parameterized

from src.back import TreasureMap


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
        ["Add one adventurer", 3, 4, [("Lara", 1, 1, "S", "AA")], 1],
        ["Add two adventurers", 3, 4, [("Lara", 1, 1, "S", "AA"), ("Indiana", 2, 1, "S", "AA")], 2],
        ["Forbid two adventurers on same cell", 3, 4, [("Lara", 1, 1, "S", "AA"), ("Indiana", 1, 1, "S", "AA")], 1],
        ["Out of bound adventurer in Positives", 3, 4, [("Lara", 10, 10, "S", "AA")], 0],
        ["Out of bound adventurer in Positive for one coordinate", 3, 4, [("Lara", 1, 10, "S", "AA")], 0],
        ["Out of bound adventurer in Negatives", 3, 4, [("Lara", -1, -1, "S", "AA")], 0],
    ])
    def test_map_and_adventurers(self, name, width, height, adventurers, expected):
        treasure_map = TreasureMap(width, height, adventurers=adventurers)
        assert treasure_map.get_adventurers_count() == expected

    @parameterized.expand([
        ["adventurer moves on the map", 3, 4, [("Lara", 1, 1, "E", "A")], "(1, 2), EAST"],
        ["adventurer tries to fall off the map's edge from the EAST", 1, 1, [("Lara", 0, 0, "E", "A")], "(0, 0), EAST"],
        ["adventurer tries to fall off the map's edge from the SOUTH", 1, 1, [("Lara", 0, 0, "S", "A")], "(0, 0), SOUTH"],
        ["adventurer tries to fall off the map's edge from the WEST", 1, 1, [("Lara", 0, 0, "W", "A")], "(0, 0), WEST"],
        ["adventurer tries to fall off the map's edge from the NORTH", 1, 1, [("Lara", 0, 0, "N", "A")], "(0, 0), NORTH"],
    ])
    def test_map_and_adventurer_movements(self, name, width, height, adventurers, expected):
        treasure_map = TreasureMap(width, height, adventurers=adventurers)
        treasure_map.next()
        assert str(list(treasure_map.adventurers.keys())[0]) == expected

    @parameterized.expand([
        ["Add one adventurer on mountain", 3, 4, [(0, 0)], [("Lara", 0, 0, "E", "AA")], 0],
    ])
    def test_map_and_adventurer_with_mountains(self, name, width, height, mountains, adventurers, expected):
        treasure_map = TreasureMap(width, height, mountains, adventurers=adventurers)
        assert treasure_map.get_adventurers_count() == expected

    @parameterized.expand([
        ["adventurer is blocked by mountain on the EAST", 3, 4, [(0, 1)], [("Lara", 0, 0, "E", "A")], "(0, 0), EAST"],
        ["adventurer is blocked by mountain on the SOUTH", 3, 4, [(1, 0)], [("Lara", 0, 0, "S", "A")], "(0, 0), SOUTH"],
        ["adventurer is blocked by mountain on the WEST", 3, 4, [(0, 0)], [("Lara", 1, 0, "W", "A")], "(1, 0), WEST"],
        ["adventurer is blocked by mountain on the NORTH", 3, 4, [(0, 0)], [("Lara", 0, 1, "N", "A")], "(0, 1), NORTH"],
    ])
    def test_map_and_adventurer_movements_with_mountains(self, name, width, height, mountains, adventurers, expected):
        treasure_map = TreasureMap(width, height, mountains, adventurers=adventurers)
        treasure_map.next()
        assert str(list(treasure_map.adventurers.keys())[0]) == expected

    @parameterized.expand([
        ["adventurer picks up a treasure", 3, 4, [(0, 1, 1)], [("Lara", 0, 0, "E", "A")], (1, 0)],
        ["adventurer picks up two treasures on different cells", 3, 4, [(0, 1, 1), (0, 2, 1)], [("Lara", 0, 0, "E", "AA")], (2, 0)],
        ["adventurer picks up two treasures on same cell", 3, 4, [(0, 1, 2)], [("Lara", 0, 0, "E", "AARRA")], (2, 0)],
        ["adventurer picks up two treasures on same cell", 3, 4, [(0, 1, 5)], [("Lara", 0, 0, "E", "AARRA")], (2, 3)],
    ])
    def test_map_and_adventurers_with_treasures(self, name, width, height, treasures, adventurers, expected):
        treasure_map = TreasureMap(width, height, treasures=treasures, adventurers=adventurers)
        treasure_map.next()
        treasure_map.next()
        treasure_map.next()
        treasure_map.next()
        treasure_map.next()
        p = list(treasure_map.adventurers.keys())[0]
        picked_up, remaining = expected
        assert p.collected_treasures == picked_up
        assert treasure_map.get_treasures_count() == remaining


if __name__ == "__main__":
    unittest.main()
