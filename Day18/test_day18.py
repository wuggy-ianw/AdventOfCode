import unittest
from day18 import next_line_of_traps, get_lines_of_traps, count_safe_squares

class Day18Tests(unittest.TestCase):
    def test_next_line_example1(self):
        # Then, starting with the row ..^^.
        # we now know the next row of tiles in the room: .^^^^
        result = next_line_of_traps('..^^.')
        expected = '.^^^^'
        self.assertEqual(result, expected)

        # Then, we continue on to the next row, using the same rules, and get ^^..^
        result = next_line_of_traps('.^^^^')
        expected = '^^..^'
        self.assertEqual(result, expected)

    def test_get_lines_example1(self):
        # Here's a larger example with ten tiles per row and ten rows:
        expected = ['.^^.^.^^^^',
                    '^^^...^..^',
                    '^.^^.^.^^.',
                    '..^^...^^^',
                    '.^^^^.^^.^',
                    '^^..^.^^..',
                    '^^^^..^^^.',
                    '^..^^^^.^^',
                    '.^^^..^.^^',
                    '^^.^^^..^^']
        result = get_lines_of_traps('.^^.^.^^^^', 10)
        self.assertEqual(result, expected)

    def test_count_safe_squares(self):
        # In ten rows, this larger example (starting with .^^.^.^^^^ for 10 rows) has 38 safe tiles.
        result = count_safe_squares('.^^.^.^^^^', 10)
        self.assertEqual(result, 38)

if __name__ == '__main__':
    unittest.main()
