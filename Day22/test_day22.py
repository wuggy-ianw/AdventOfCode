import unittest

from day22 import PuzzleState, GridNode, parse_df_input_line, day22b_solver

class Day22Tests(unittest.TestCase):

    def test_generate_state_from_lines(self):
        node_lines = ['/dev/grid/node-x0-y0   10T    8T     2T   80%',
                      '/dev/grid/node-x0-y1   11T    6T     5T   54%',
                      '/dev/grid/node-x0-y2   32T   28T     4T   87%',
                      '/dev/grid/node-x1-y0    9T    7T     2T   77%',
                      '/dev/grid/node-x1-y1    8T    0T     8T    0%',
                      '/dev/grid/node-x1-y2   11T    7T     4T   63%',
                      '/dev/grid/node-x2-y0   10T    6T     4T   60%',
                      '/dev/grid/node-x2-y1    9T    8T     1T   88%',
                      '/dev/grid/node-x2-y2    9T    6T     3T   66%']

        nodes = [parse_df_input_line(l) for l in node_lines]
        expected = [GridNode(x=0, y=0, size=10, used=8, avail=2),
                    GridNode(x=0, y=1, size=11, used=6, avail=5),
                    GridNode(x=0, y=2, size=32, used=28, avail=4),
                    GridNode(x=1, y=0, size=9, used=7, avail=2),
                    GridNode(x=1, y=1, size=8, used=0, avail=8),
                    GridNode(x=1, y=2, size=11, used=7, avail=4),
                    GridNode(x=2, y=0, size=10, used=6, avail=4),
                    GridNode(x=2, y=1, size=9, used=8, avail=1),
                    GridNode(x=2, y=2, size=9, used=6, avail=3)
                    ]
        self.assertEqual(nodes, expected)

        state = PuzzleState(nodes)
        self.assertEqual(state.zero_pos, (1,1))
        self.assertEqual(state.data_pos, (2,0))

        for x, y, size, used, avail in nodes:
            self.assertEqual(state.available_grid[x,y], avail)
            self.assertEqual(state.used_grid[x,y], used)

        lines = state.visualise()
        expected = ['..G',
                    '._.',
                    '#..']
        self.assertEqual(lines, expected)


    def test_sliding_puzzle_solver(self):
        node_lines = ['/dev/grid/node-x0-y0   10T    8T     2T   80%',
                      '/dev/grid/node-x0-y1   11T    6T     5T   54%',
                      '/dev/grid/node-x0-y2   32T   28T     4T   87%',
                      '/dev/grid/node-x1-y0    9T    7T     2T   77%',
                      '/dev/grid/node-x1-y1    8T    0T     8T    0%',
                      '/dev/grid/node-x1-y2   11T    7T     4T   63%',
                      '/dev/grid/node-x2-y0   10T    6T     4T   60%',
                      '/dev/grid/node-x2-y1    9T    8T     1T   88%',
                      '/dev/grid/node-x2-y2    9T    6T     3T   66%']

        nodes = [parse_df_input_line(l) for l in node_lines]
        result = day22b_solver(nodes)
        expected = 7
        self.assertEqual(result, expected)





if __name__ == '__main__':
    unittest.main()
