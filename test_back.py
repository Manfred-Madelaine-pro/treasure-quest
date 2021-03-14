import unittest
from parameterized import parameterized

from back import Map


class MapTest(unittest.TestCase):
    @parameterized.expand([
        ["Limit", 0, 0, (0, 0)],
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
        ["Impossible 2 mountains on same cell", 3, 4, [(1, 1), (1, 1)], 1],
        ["Out of bound mountain in Positives", 3, 4, [(8, 8)], 0],
        ["Out of bound mountain in Positive for one coordinate", 3, 4, [(2, 8)], 0],
        ["Out of bound mountain in Negatives", 3, 4, [(-1, -1)], 0],
    ])
    def test_map_creation_with_plains_and_mountains(self, name, width, height, mountains, expected):
        quest_map = Map(width, height, mountains)
        assert quest_map.get_mountains_count() == expected


if __name__ == '__main__':
    unittest.main()
