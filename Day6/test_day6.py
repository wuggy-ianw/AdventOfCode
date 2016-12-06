import unittest

from day6 import day6a_solver

class Day6Tests(unittest.TestCase):
    def test_decode_example1(self):
        example = ['eedadn',
                   'drvtee',
                   'eandsr',
                   'raavrd',
                   'atevrs',
                   'tsrnev',
                   'sdttsa',
                   'rasrtv',
                   'nssdts',
                   'ntnada',
                   'svetve',
                   'tesnvt',
                   'vntsnd',
                   'vrdear',
                   'dvrsen',
                   'enarar']

        decoded = day6a_solver(example)
        self.assertEqual(decoded,'easter')


if __name__ == '__main__':
    unittest.main()
