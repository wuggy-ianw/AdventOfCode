import unittest
from day21 import swap_by_position_directive, swap_by_letter_directive, rotate_right_directive, \
                  rotate_left_directive, rotate_based_on_position_directive, reverse_positions_directive, \
                  move_positions_directive, parse_directive

class Day21Tests(unittest.TestCase):

    def test_swap_by_position_directive(self):
        # 'swap position X with position Y' means that the letters at indexes X and Y (counting from 0) should be swapped.
        directive = swap_by_position_directive.match_and_create('swap position 0 with position 7')
        result = directive.perform('abcdefgh')
        expected = 'hbcdefga'
        self.assertEqual(result, expected)

        directive = swap_by_position_directive.match_and_create('swap position 4 with position 2')
        result = directive.perform('abcdefg')
        expected = 'abedcfg'
        self.assertEqual(result, expected)

    def test_swap_by_letter_directive(self):
        # 'swap letter X with letter Y' means that the letters X and Y should be swapped (regardless of where they appear in the string).
        directive = swap_by_letter_directive.match_and_create('swap letter a with letter f')
        result = directive.perform('abcdefgh')
        expected = 'fbcdeagh'
        self.assertEqual(result, expected)

        directive = swap_by_letter_directive.match_and_create('swap letter z with letter b')
        result = directive.perform('abcdefgh')
        expected = 'azcdefgh'
        self.assertEqual(result, expected)

        directive = swap_by_letter_directive.match_and_create('swap letter p with letter a')
        result = directive.perform('pppaaaapp')
        expected = 'aaappppaa'
        self.assertEqual(result, expected)

    def test_rotate_right_directive(self):
        # 'rotate left/right X steps' means that the whole string should be rotated; for example, one right rotation would turn abcd into dabc.
        directive = rotate_right_directive.match_and_create('rotate right 0 steps')
        result = directive.perform('abcdefgh')
        expected = 'abcdefgh'
        self.assertEqual(result, expected)

        directive = rotate_right_directive.match_and_create('rotate right 1 step')
        result = directive.perform('abcdefgh')
        expected = 'habcdefg'
        self.assertEqual(result, expected)

        directive = rotate_right_directive.match_and_create('rotate right 5 steps')
        result = directive.perform('abcdefgh')
        expected = 'defghabc'
        self.assertEqual(result, expected)

    def test_rotate_left_directive(self):
        # 'rotate left/right X steps' means that the whole string should be rotated; for example, one right rotation would turn abcd into dabc.
        directive = rotate_left_directive.match_and_create('rotate left 0 steps')
        result = directive.perform('abcdefgh')
        expected = 'abcdefgh'
        self.assertEqual(result, expected)

        directive = rotate_left_directive.match_and_create('rotate left 1 step')
        result = directive.perform('abcdefgh')
        expected = 'bcdefgha'
        self.assertEqual(result, expected)

        directive = rotate_left_directive.match_and_create('rotate left 4 steps')
        result = directive.perform('abcdefgh')
        expected = 'efghabcd'
        self.assertEqual(result, expected)

    def test_rotate_based_on_position_directive(self):
        # 'rotate based on position of letter X' means that the whole string should be
        # rotated to the right based on the index of letter X (counting from 0) as
        # determined before this instruction does any rotations. Once the index is
        # determined, rotate the string to the right one time, plus a number of times
        # equal to that index, plus one additional time if the index was at least 4.
        directive = rotate_based_on_position_directive.match_and_create('rotate based on position of letter a')
        result = directive.perform('abcdefgh')
        expected = 'habcdefg'
        self.assertEqual(result, expected)

        directive = rotate_based_on_position_directive.match_and_create('rotate based on position of letter d')
        result = directive.perform('abcdefgh')
        expected = 'efghabcd'
        self.assertEqual(result, expected)

        directive = rotate_based_on_position_directive.match_and_create('rotate based on position of letter e')
        result = directive.perform('abcdefgh')
        expected = 'cdefghab'
        self.assertEqual(result, expected)

        directive = rotate_based_on_position_directive.match_and_create('rotate based on position of letter d')
        result = directive.perform('ecabd')
        expected = 'decab'
        self.assertEqual(result, expected)

    def test_reverse_positions_directive(self):
        # 'reverse positions X through Y' means that the span of letters at indexes
        # X through Y (including the letters at X and Y) should be reversed in order.
        directive = reverse_positions_directive.match_and_create('reverse positions 0 through 7')
        result = directive.perform('abcdefgh')
        expected = 'hgfedcba'
        self.assertEqual(result, expected)

        directive = reverse_positions_directive.match_and_create('reverse positions 2 through 4')
        result = directive.perform('abcdefgh')
        expected = 'abedcfgh'
        self.assertEqual(result, expected)

    def test_move_positions_directive(self):
        # 'move position X to position Y' means that the letter which is at index X should be
        # removed from the string, then inserted such that it ends up at index Y.
        directive = move_positions_directive.match_and_create('move position 0 to position 0')
        result = directive.perform('abcdefgh')
        expected = 'abcdefgh'
        self.assertEqual(result, expected)

        directive = move_positions_directive.match_and_create('move position 2 to position 4')
        result = directive.perform('abcdefgh')
        expected = 'abdecfgh'
        self.assertEqual(result, expected)

    def test_solver_example(self):
        s = 'abcde'
        directive_lines_and_expected = [('swap position 4 with position 0', 'ebcda'),
                                        ('swap letter d with letter b', 'edcba'),
                                        ('reverse positions 0 through 4', 'abcde'),
                                        ('rotate left 1 step', 'bcdea'),
                                        ('move position 1 to position 4', 'bdeac'),
                                        ('move position 3 to position 0', 'abdec'),
                                        ('rotate based on position of letter b', 'ecabd'),
                                        ('rotate based on position of letter d', 'decab')]

        directives_and_expected = [(parse_directive(d), e) for d,e in directive_lines_and_expected]

        for d, e in directives_and_expected:
            s = d.perform(s)
            self.assertEqual(s, e)


    def test_solver_example_inverted(self):
        s = 'decab'
        directive_lines_and_expected = reversed([('swap position 4 with position 0', 'abcde'),
                                        ('swap letter d with letter b', 'ebcda'),
                                        ('reverse positions 0 through 4', 'edcba'),
                                        ('rotate left 1 step', 'abcde'),
                                        ('move position 1 to position 4', 'bcdea'),
                                        ('move position 3 to position 0', 'bdeac'),
                                        ('rotate based on position of letter b', 'abdec'),
                                        ('rotate based on position of letter d', 'ecabd')])

        directives_and_expected = [(parse_directive(d), e) for d,e in directive_lines_and_expected]

        for d, e in directives_and_expected:
            s = d.perform_inverted(s)
            self.assertEqual(s, e)


if __name__ == '__main__':
    unittest.main()
