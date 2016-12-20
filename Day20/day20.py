import re
from bitarray import bitarray


match_input_line_re = re.compile(r'([0-9]+)-([0-9]+)')

def parse_input_line(line):
    """
    Given a line, split it into the lower and upper range parts. Asserts that the input is a range
    and that it's in the right order.

    :param line: A string containing an input range (e.g. '123-345')
    :return: a tuple of (lower, upper), where lower and upper are integers
    """
    match = match_input_line_re.match(line)
    assert match, "Input did not contain a range?"

    lower = int(match.group(1))
    upper = int(match.group(2))

    assert lower<=upper, "Input range had a bad order?"
    return lower, upper


def merge_ranges(ranges):
    """
    Reduce a set of ranges into non-overlapping ranges, by merging overlaps into a single range.

    :param ranges: a list of tuples(lower,upper) for the range bounds (inclusive)
    :return: a new sorted list of ranges without any overlaps, strictly range[n].upper < range[n+1].lower will be true for all 'n'
    """
    sorted_ranges = sorted(ranges)
    merged_ranges = []

    current_lower, current_upper = sorted_ranges[0]
    for lower,upper in sorted_ranges[1:]:
        if lower>current_upper+1:
            # the new range is not overlapping
            merged_ranges.append((current_lower, current_upper))
            current_lower, current_upper = lower, upper
        else:
            # this must be an overlapping range (or directly adjacent)
            current_upper = max(current_upper, upper)

    # append the 'last' current range since there's no more ranges to try and merge it with
    merged_ranges.append((current_lower, current_upper))

    return merged_ranges


def invert_nonoverlapping_sorted_ranges(ranges, limit=(2 ** 32) - 1):
    """
    Given some nonoverlapping sorted ranges, invert them (i.e. invert an 'excluded' set
    of ranges to be an 'included' set of ranges).

    :param ranges: A list of tuple(lower,upper) of ranges, such that no range overlaps with another and they're
                    sorted in increasing order of 'lower'
    :param limit: The last value in the permitted set of value. Used to create a 'final' included range if ranges
                    doesn't exclude all the way to the limit value.
    :return: A list of tuples(lower,upper) of ranges which are the values between 0 and limit that are NOT in
                any of the input ranges.
    """
    inverted_ranges = []
    current_first_included = 0
    for lower, upper in ranges:
        if lower>current_first_included:
            # we need to include a range from first_included to lower-1
            inverted_ranges.append((current_first_included, lower - 1))
            current_first_included = upper + 1

        current_first_included = upper + 1

    # check if we have to include a range at the end up to the limit
    if current_first_included<=limit:
        inverted_ranges.append((current_first_included, limit))

    return inverted_ranges


def find_smallest_permitted_value(ranges):
    """
    Find the first value from the first range.

    :param ranges: A list of tuples (lower,upper) ranges, non-overlapping, sorted in ascending order.
    :return: the first value in the first (lowest) range
    """
    lower, upper = ranges[0]
    return lower


def count_permitted_values(ranges):
    """
    Count the number of values that are included across the list of ranges.

    :param ranges:A list of tuples(lower,upper) ranges, non-overlapping, sorting in ascending order.
    :return: an integer, the number of values that the ranges include
    """
    included = 0
    for lower,upper in ranges:
        included += (upper - lower) + 1

    return included


if __name__ == '__main__':
    with(open('input_20a.txt', 'r')) as infile:
        range_lines = infile.read().splitlines()

    excluded_ranges_raw = [parse_input_line(l) for l in range_lines]
    excluded_ranges_merged = merge_ranges(excluded_ranges_raw)
    included_ranges = invert_nonoverlapping_sorted_ranges(excluded_ranges_merged)

    print(find_smallest_permitted_value(included_ranges))
    print(count_permitted_values(included_ranges))

