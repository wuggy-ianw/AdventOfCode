import unittest

from day9 import decompressed_length

class Day9aTests(unittest.TestCase):
    def test_example1(self):
        # ADVENT contains no markers and decompresses to itself with no changes, resulting in a decompressed length of 6.
        resultlen = decompressed_length('ADVENT')
        self.assertEqual(resultlen, len('ADVENT'))

    def test_example2(self):
        # A(1x5)BC repeats only the B a total of 5 times, becoming ABBBBBC for a decompressed length of 7.
        resultlen = decompressed_length('A(1x5)BC')
        self.assertEqual(resultlen, len('ABBBBBC'))

    def test_example3(self):
        # (3x3)XYZ becomes XYZXYZXYZ for a decompressed length of 9.
        resultlen = decompressed_length('(3x3)XYZ')
        self.assertEqual(resultlen, len('XYZXYZXYZ'))

    def test_example4(self):
        # A(2x2)BCD(2x2)EFG doubles the BC and EF, becoming ABCBCDEFEFG for a decompressed length of 11.
        resultlen = decompressed_length('A(2x2)BCD(2x2)EFG')
        self.assertEqual(resultlen, len('ABCBCDEFEFG'))

    def test_example5(self):
        # (6x1)(1x3)A simply becomes (1x3)A - the (1x3) looks like a marker, but because it's within a data section of another marker, it is not treated any differently from the A that comes after it. It has a decompressed length of 6.
        resultlen = decompressed_length('(6x1)(1x3)A')
        self.assertEqual(resultlen, len('(1x3)A'))

    def test_example6(self):
        # X(8x2)(3x3)ABCY becomes X(3x3)ABC(3x3)ABCY (for a decompressed length of 18), because the decompressed data from the (8x2) marker (the (3x3)ABC) is skipped and not processed further.
        resultlen = decompressed_length('X(8x2)(3x3)ABCY')
        self.assertEqual(resultlen, len('X(3x3)ABC(3x3)ABCY'))


class Day9bTests(unittest.TestCase):
    def test_example1(self):
        # (3x3)XYZ still becomes XYZXYZXYZ, as the decompressed section contains no markers.
        resultlen = decompressed_length('(3x3)XYZ', v2=True)
        self.assertEqual(resultlen, len('XYZXYZXYZ'))

    def test_example2(self):
        # X(8x2)(3x3)ABCY becomes XABCABCABCABCABCABCY, because the decompressed data from the (8x2) marker is then further decompressed, thus triggering the (3x3) marker twice for a total of six ABC sequences.
        resultlen = decompressed_length('X(8x2)(3x3)ABCY', v2=True)
        self.assertEqual(resultlen, len('XABCABCABCABCABCABCY'))

    def test_example3(self):
        # (27x12)(20x12)(13x14)(7x10)(1x12)A decompresses into a string of A repeated 241920 times.
        resultlen = decompressed_length('(27x12)(20x12)(13x14)(7x10)(1x12)A', v2=True)
        self.assertEqual(resultlen, 241920)

    def test_example4(self):
        # (25x3)(3x3)ABC(2x3)XY(5x2)PQRSTX(18x9)(3x2)TWO(5x7)SEVEN becomes 445 characters long.
        resultlen = decompressed_length('(25x3)(3x3)ABC(2x3)XY(5x2)PQRSTX(18x9)(3x2)TWO(5x7)SEVEN', v2=True)
        self.assertEqual(resultlen, 445)



if __name__ == '__main__':
    unittest.main()
