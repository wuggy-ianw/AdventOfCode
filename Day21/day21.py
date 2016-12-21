import re


def rotate_string_left(s, shift):
    shift %= len(s)
    return s[shift:] + s[0:shift]


def rotate_string_right(s, shift):
    shift %= len(s)
    return s[-shift:] + s[:-shift]


class swap_by_position_directive(object):
    # 'swap position X with position Y' means that the letters at indexes X and Y (counting from 0) should be swapped.
    match_re = re.compile(r'swap position ([0-9]+) with position ([0-9]+)')

    @classmethod
    def match_and_create(cls, directive_text):
        match = cls.match_re.match(directive_text)
        if not match:
            return None

        return cls(int(match.group(1)), int(match.group(2)))

    def __init__(self, from_position, to_position):
        self.from_position = min(from_position, to_position)
        self.to_position = max(from_position, to_position)

    def perform(self, s):
        t = s[0:self.from_position] + s[self.to_position] + s[self.from_position+1:self.to_position] + s[self.from_position] + s[self.to_position+1:]
        return t

    def perform_inverted(self, s):
        # swap by position is it's own inverse
        return self.perform(s)


class swap_by_letter_directive(object):
    # 'swap letter X with letter Y' means that the letters X and Y should be swapped (regardless of where they appear in the string).
    match_re = re.compile(r'swap letter ([a-z]) with letter ([a-z])')

    @classmethod
    def match_and_create(cls, directive_text):
        match = cls.match_re.match(directive_text)
        if not match:
            return None

        return cls(match.group(1), match.group(2))

    def __init__(self, a_char, b_char):
        self.transtable = str.maketrans(a_char + b_char, b_char + a_char)

    def perform(self, s):
        return s.translate(self.transtable)

    def perform_inverted(self, s):
        # swap by letter is it's own inverse
        return self.perform(s)


class rotate_right_directive(object):
    # 'rotate left/right X steps' means that the whole string should be rotated; for example, one right rotation would turn abcd into dabc.
    match_re = re.compile(r'rotate right ([0-9]+) steps?')

    @classmethod
    def match_and_create(cls, directive_text):
        match = cls.match_re.match(directive_text)
        if not match:
            return None

        return cls(int(match.group(1)))

    def __init__(self, steps):
        self.right_steps = steps

    def perform(self, s):
        return rotate_string_right(s, self.right_steps)

    def perform_inverted(self, s):
        return rotate_string_left(s, self.right_steps)


class rotate_left_directive(object):
    # 'rotate left/right X steps' means that the whole string should be rotated; for example, one right rotation would turn abcd into dabc.
    match_re = re.compile(r'rotate left ([0-9]+) steps?')

    @classmethod
    def match_and_create(cls, directive_text):
        match = cls.match_re.match(directive_text)
        if not match:
            return None

        return cls(int(match.group(1)))

    def __init__(self, steps):
        self.left_steps = steps

    def perform(self, s):
        return rotate_string_left(s, self.left_steps)

    def perform_inverted(self, s):
        return rotate_string_right(s, self.left_steps)


class rotate_based_on_position_directive(object):
    # 'rotate based on position of letter X' means that the whole string should be rotated to
    # the right based on the index of letter X (counting from 0) as determined before this
    # instruction does any rotations. Once the index is determined, rotate the string to the
    # right one time, plus a number of times equal to that index, plus one additional time if
    # the index was at least 4.
    match_re = re.compile(r'rotate based on position of letter ([a-z])')

    @classmethod
    def match_and_create(cls, directive_text):
        match = cls.match_re.match(directive_text)
        if not match:
            return None

        return cls(match.group(1))

    def __init__(self, letter):
        self.letter = letter
        self.inversion_table = None

    def steps_right_for_index(self, index):
        """
        Compute the number of right-shifts to perform for a character found at a given index.

        :param index: integer index
        :return: integer, the number of right-steps to shift
        """
        right_steps = index + 1
        if index >= 4:
            right_steps += 1
        return right_steps

    def perform(self, s):
        index = s.index(self.letter)
        right_steps = self.steps_right_for_index(index)
        return rotate_string_right(s, right_steps)

    def compute_inversion(self, length):
        """
        Compute the mapping from 'end' position to the shift left required to get back to the 'start' position.
        Will assert if there is no unique mapping

        :param length: length of strings to be inverted
        :return: None, updates self.inversion_table, a map indexed by 'end' positions
        """
        if self.inversion_table==None:
            inversion_table = {}
            for index in range(length):
                right_steps = self.steps_right_for_index(index)
                endpos = (right_steps + index) % length

                if endpos in inversion_table:
                    print("Warning: multiple possible rotations can arrive at the same end position...")

                inversion_table[endpos]=right_steps

            self.inversion_table = inversion_table

    def perform_inverted(self, s):
        self.compute_inversion(len(s))
        end_index = s.index(self.letter)
        left_steps = self.inversion_table[end_index]
        return rotate_string_left(s, left_steps)



class reverse_positions_directive(object):
    # 'reverse positions X through Y' means that the span of letters at indexes X through Y
    # (including the letters at X and Y) should be reversed in order.
    match_re = re.compile(r'reverse positions ([0-9]+) through ([0-9]+)')

    @classmethod
    def match_and_create(cls, directive_text):
        match = cls.match_re.match(directive_text)
        if not match:
            return None

        return cls(int(match.group(1)), int(match.group(2)))

    def __init__(self, from_position, to_position):
        self.from_position = from_position
        self.to_position = to_position

    def perform(self, s):
        return s[0:self.from_position] + "".join(reversed(s[self.from_position:self.to_position+1])) + s[self.to_position+1:]

    def perform_inverted(self, s):
        # this directive is it's own inverse
        return self.perform(s)


class move_positions_directive(object):
    # 'move position X to position Y' means that the letter which is at index X should be
    # removed from the string, then inserted such that it ends up at index Y.
    match_re = re.compile(r'move position ([0-9]+) to position ([0-9]+)')

    @classmethod
    def match_and_create(cls, directive_text):
        match = cls.match_re.match(directive_text)
        if not match:
            return None

        return cls(int(match.group(1)), int(match.group(2)))

    def __init__(self, from_position, to_position):
        self.from_position = from_position
        self.to_position = to_position

    def perform(self, s):
        removed = s[0:self.from_position] + s[self.from_position+1:]
        inserted = removed[0:self.to_position] + s[self.from_position] + removed[self.to_position:]

        return inserted

    def perform_inverted(self, s):
        removed = s[0:self.to_position] + s[self.to_position + 1:]
        inserted = removed[0:self.from_position] + s[self.to_position] + removed[self.from_position:]

        return inserted


directive_classes = [swap_by_position_directive, swap_by_letter_directive, rotate_right_directive,
                     rotate_left_directive, rotate_based_on_position_directive, reverse_positions_directive,
                     move_positions_directive]

def parse_directive(directive_line):
    for candidate_directive_class in directive_classes:
        directive = candidate_directive_class.match_and_create(directive_line)
        if directive:
            return directive

    assert False, "Directive line didn't match any known directives?"


def day21a_solver(directive_lines, s):
    directives = [parse_directive(l) for l in directive_lines]
    for directive in directives:
        s = directive.perform(s)
    return s


def day21b_solver(directive_lines, s):
    directives = reversed([parse_directive(l) for l in directive_lines])
    for directive in directives:
        s = directive.perform_inverted(s)
    return s


if __name__ == '__main__':
    with(open('input_day21a.txt', 'r')) as infile:
        directives = infile.read().splitlines()

    print(day21a_solver(directives, 'abcdefgh'))
    print(day21b_solver(directives, 'fbgdceah'))
