import unittest

from day1 import solver

class Day1ASolverTest(unittest.TestCase):

    def test_example1(self):
        # "Following R2, L3 leaves you 2 blocks East and 3 blocks North, or 5 blocks away."
        dist, pos = solver('R2, L3')

        self.assertEqual(dist, 5)
        self.assertEqual(pos, [2,3])

    def test_example2(self):
        # R2, R2, R2 leaves you 2 blocks due South of your starting position, which is 2 blocks away.
        dist, pos = solver('R2, R2, R2')

        self.assertEqual(dist, 2)
        self.assertEqual(pos, [0, -2])

    def test_example3(self):
        # R5, L5, R5, R3 leaves you 12 blocks away.
        dist, pos = solver('R5, L5, R5, R3')

        self.assertEqual(dist, 12)
        self.assertEqual(pos, [10, 2])

class Day1BSolverTest(unittest.TestCase):

    def test_example1(self):
        # For example, if your instructions are R8, R4, R4, R8, the first location you visit twice is 4 blocks away, due East.
        dist, pos = solver('R8, R4, R4, R8', True)

        self.assertEqual(dist, 4)
        self.assertEqual(pos, [4, 0])

if __name__ == '__main__':
    unittest.main()
