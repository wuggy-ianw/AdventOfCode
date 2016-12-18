

def next_line_of_traps(traps):
    """
    Given a line of traps, follow the rules to determine the next line of traps.

    :param traps: a string containing '.' or '^' characters, for 'safe' and 'trap' places respectively
    :return: a string containing '.' or '^' characters, for the new layout of traps
    """
    traps_safe_sides = '.' + traps + '.'    # add 'safe' pseudosquares on either side
    next_traps = ''                         # next line starts empty
    for l, c, r in zip(traps_safe_sides[0:], traps_safe_sides[1:], traps_safe_sides[2:]):
        # Its left and center tiles are traps, but its right tile is not.
        # Its center and right tiles are traps, but its left tile is not.
        # Only its left tile is a trap.
        # Only its right tile is a trap
        if (l == '^' and c == '^' and r == '.') or \
                (c == '^' and r == '^' and l == '.') or \
                (l == '^' and c == '.' and r == '.') or \
                (r == '^' and l == '.' and c == '.'):
            next_traps += '^'
        else:
            next_traps += '.'

    return next_traps

def get_lines_of_traps(initial_line_of_traps, length):
    """
    Given an initial line, compute the traps for the grid up to the length.

    :param initial_line_of_traps: a string of '.' and '^' characters, denoting safe and trap places respectively
    :param length: integer of the length of the trap grid
    :return: a list of trap strings, starting with the initial line of traps
    """
    lines = [initial_line_of_traps]
    while len(lines) < length:
        lines.append(next_line_of_traps(lines[-1]))
    return lines

def count_safe_squares(initial_line_of_traps, length):
    lines_of_traps = get_lines_of_traps(initial_line_of_traps, length)
    return sum([l.count('.') for l in lines_of_traps])


def day18a_solver(length=40):
     print(count_safe_squares('.^..^....^....^^.^^.^.^^.^.....^.^..^...^^^^^^.^^^^.^.^^^^^^^.^^^^^..^.^^^.^^..^.^^.^....^.^...^^.^.', length))


def day18b_solver():
    day18a_solver(length=400000)


if __name__ == '__main__':
    day18a_solver()
    day18b_solver()

