import unittest
from parameterized import parameterized

from back import Map


class MapTest(unittest.TestCase):
    @parameterized.expand([
        ["No map", 0, 0, (0, 0)],
        ["Small map", 1, 1, (1, 1)],
        ["Normal map", 3, 4, (3, 4)],
        ["Big map", 10, 20, (10, 20)],
        ["Impossible map", -1, -4, (0, 0)],
    ])
    def test_map_creation(self, name, width, height, expected):
        quest_map = Map(width, height)
        assert (quest_map.width, quest_map.height) == expected

    @parameterized.expand([
        ["Normal map with no mountains", 3, 4, 0],
    ])
    def test_map_creation_with_only_plains(self, name, width, height, expected):
        quest_map = Map(width, height)
        assert quest_map.get_mountains_count() == expected

    @parameterized.expand([
        ["Normal map with 1 mountain", 3, 4, [(0, 0)], 1],
        ["Normal map with 2 mountains", 3, 4, [(0, 0), (1, 1)], 2],
        ["Ignore mountain creation when on same cell as another mountain", 3, 4, [(1, 1), (1, 1)], 1],
        ["Out of bound mountain in Positives", 3, 4, [(8, 8)], 0],
        ["Out of bound mountain in Positive for one coordinate", 3, 4, [(2, 8)], 0],
        ["Out of bound mountain in Negatives", 3, 4, [(-1, -1)], 0],
    ])
    def test_map_creation_with_plains_and_mountains(self, name, width, height, mountains, expected):
        quest_map = Map(width, height, mountains)
        assert quest_map.get_mountains_count() == expected

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
        quest_map = Map(width, height, treasures=treasures)
        assert quest_map.get_treasures_count() == expected

    @parameterized.expand([
        ["Normal map with 1 mountain and 1 treasure", 3, 4, [(0, 0)], [(0, 1, 1)], 1],
        ["Ignore treasure when on same cell as mountain", 3, 4, [(0, 0)], [(0, 0, 1)], 0],
    ])
    def test_map_creation_with_treasures_and_mountains(self, name, width, height, mountains, treasures, expected):
        quest_map = Map(width, height, mountains, treasures)
        assert quest_map.get_treasures_count() == expected


if __name__ == '__main__':
    unittest.main()
