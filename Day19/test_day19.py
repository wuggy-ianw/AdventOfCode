import unittest
from day19 import day19b_shuffle_presents_slow_one_level, day19b_shuffle_presents_one_level

class Day19PatternTests(unittest.TestCase):
    def test_19b_triple_array_mod_zero(self):
        # there is a pattern for n*3 sized arrays
        # use the slow shuffle to check this
        expected = day19b_shuffle_presents_slow_one_level(list(range(1,10)))
        result = day19b_shuffle_presents_one_level(list(range(1,10)))
        self.assertEqual(expected, result)

        # try for some bigger multiples of 3
        expected = day19b_shuffle_presents_slow_one_level(list(range(1,1+(3*50))))
        result = day19b_shuffle_presents_one_level(list(range(1,1+(3*50))))
        self.assertEqual(expected, result)

        # try for some bigger multiples of 3
        expected = day19b_shuffle_presents_slow_one_level(list(range(1,1+(3 * 97))))
        result = day19b_shuffle_presents_one_level(list(range(1,1+(3 * 97))))
        self.assertEqual(expected, result)


    def test_19b_triple_array_mod_one(self):
        # there is a pattern for (n*3)+1 sized arrays
        # use the slow shuffle to check this
        expected = day19b_shuffle_presents_slow_one_level(list(range(1,11)))
        result = day19b_shuffle_presents_one_level(list(range(1,11)))
        self.assertEqual(expected, result)

        # try for some bigger multiples of 3
        expected = day19b_shuffle_presents_slow_one_level(list(range(1, 2 + (3 * 50))))
        result = day19b_shuffle_presents_one_level(list(range(1, 2 + (3 * 50))))
        self.assertEqual(expected, result)

        # try for some bigger multiples of 3
        expected = day19b_shuffle_presents_slow_one_level(list(range(1, 2 + (3 * 97))))
        result = day19b_shuffle_presents_one_level(list(range(1, 2 + (3 * 97))))
        self.assertEqual(expected, result)

    def test_19b_triple_array_mod_two(self):
        # there is a pattern for (n*3)+2 sized arrays
        # use the slow shuffle to check this
        expected = day19b_shuffle_presents_slow_one_level(list(range(1,12)))
        result = day19b_shuffle_presents_one_level(list(range(1,12)))
        self.assertEqual(expected, result)

        # try for some bigger multiples of 3
        expected = day19b_shuffle_presents_slow_one_level(list(range(1, 3 + (3 * 50))))
        result = day19b_shuffle_presents_one_level(list(range(1, 3 + (3 * 50))))
        self.assertEqual(expected, result)

        # try for some bigger multiples of 3
        expected = day19b_shuffle_presents_slow_one_level(list(range(1, 3 + (3 * 97))))
        result = day19b_shuffle_presents_one_level(list(range(1, 3 + (3 * 97))))
        self.assertEqual(expected, result)


if __name__ == '__main__':
    unittest.main()
