import unittest

from day24 import day24a_solver, day24b_solver

class Day24Tests(unittest.TestCase):
    def test_example1(self):
        maze_lines = ['###########',
                      '#0.1.....2#',
                      '#.#######.#',
                      '#4.......3#',
                      '###########']

        result = day24a_solver(maze_lines)
        self.assertEqual(result, 14)

    def test_example2(self):
        maze_lines = ['###########',
                      '#0.1.....2#',
                      '#.#######.#',
                      '#4.......3#',
                      '###########']

        result = day24b_solver(maze_lines)
        self.assertEqual(result, 20)    # shortest start/end path is one trip all the way around


if __name__ == '__main__':
    unittest.main()
