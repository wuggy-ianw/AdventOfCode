import unittest
from day15 import Disc, find_time_discs_are_aligned

class Day15test(unittest.TestCase):
    def test_example(self):
        discs = [Disc(5, 4),
                 Disc(2, 1)]

        time = find_time_discs_are_aligned(discs)
        self.assertEqual(time, 5)


if __name__ == '__main__':
    unittest.main()
