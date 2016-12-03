import unittest

from day2 import solver

class Day2ASolverTest(unittest.TestCase):

    def test_offedges1(self):
        # try going off each of the cardinal edges
        example = ['UUU', 'DDDDD', 'ULLL', 'RRRRRR']
        code = solver(example)
        self.assertEqual(code, '2846')

    def test_offedges2(self):
        # try going off each of the corner edges in the vertical path
        example = ['ULU', 'RRU', 'DDD', 'LLD']
        code = solver(example)
        self.assertEqual(code, '1397')

    def test_offedges3(self):
        # try going off each of the corner edges in the horizontal path
        example = ['LUL', 'RRR', 'DDR', 'LLL']
        code = solver(example)
        self.assertEqual(code, '1397')

    def test_cycleclockwise(self):
        # try going around all the buttons around the outside
        example = ['U', 'R', 'D', 'D', 'L', 'L', 'U', 'U']
        code = solver(example)
        self.assertEqual(code, '23698741')


    def test_cyclecounterclockwise(self):
        # try going around all the buttons around the outside
        example = ['D', 'R', 'U', 'U', 'L', 'L', 'D', 'D']
        code = solver(example)
        self.assertEqual(code, '89632147')


    def test_example1(self):
        # Suppose your instructions are:
        #
        # ULL
        # RRDDD
        # LURDL
        # UUUUD
        #
        # So, in this example, the bathroom code is 1985.
        example = ['ULL',
                   'RRDDD',
                   'LURDL',
                   'UUUUD']

        code = solver(example)
        self.assertEqual(code, '1985')

if __name__ == '__main__':
    unittest.main()
