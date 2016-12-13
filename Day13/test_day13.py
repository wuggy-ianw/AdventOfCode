import unittest
from day13 import Day13PathFinder

class Day13Tests(unittest.TestCase):

    def test_example_visualise_maze(self):
        # For example, if the office designer's favorite number were 10
        # drawing walls as # and open spaces as ., the corner of the building containing 0,0 would look like this:

        expected = ['  0123456789',
                    '0 .#.####.##',
                    '1 ..#..#...#',
                    '2 #....##...',
                    '3 ###.#.###.',
                    '4 .##..#..#.',
                    '5 ..##....#.',
                    '6 #...##.###']

        dest_pos = (7,4)
        df = Day13PathFinder(10, dest_pos)

        result = df.visualise_maze(10,7)
        self.assertEqual(result, expected)


    def test_example_visualise_path(self):
        # Now, suppose you wanted to reach 7,4. The shortest route you could take is marked as O:
        expected1 = ['  0123456789',
                     '0 .#.####.##',
                     '1 .O#..#...#',
                     '2 #OOO.##...',
                     '3 ###O#.###.',
                     '4 .##OO#OO#.',
                     '5 ..##OOO.#.',
                     '6 #...##.###']

        # there's a second, equal length alternative
        expected2 = ['  0123456789',
                     '0 .#.####.##',
                     '1 .O#..#...#',
                     '2 #OOO.##...',
                     '3 ###O#.###.',
                     '4 .##OO#.O#.',
                     '5 ..##OOOO#.',
                     '6 #...##.###']

        dest_pos = (7, 4)
        df = Day13PathFinder(10, dest_pos)
        path = df.find_shortest_path()

        result = df.visualise_maze(10, 7, path)
        self.assertTrue(result == expected1 or result == expected2)


if __name__ == '__main__':
    unittest.main()
