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


def find_smallest_permitted_value(input_lines):
    # parse all the input_lines
    ranges = [parse_input_line(i) for i in input_lines]

    # sort them by lowest bound!
    #

    # scan through the list of ranges until we've not changed out lowest_permitted
    lowest_permitted = 0
    done = False        # we need to do one pass where we don't change the permitted to be done
    while not done:
        done = True     # assume we're done, will change this back to False if we change lowest_permitted
        for lower, upper in ranges:
            if lowest_permitted>=lower and lowest_permitted<=upper:
                lowest_permitted = upper+1
                done = False        # need another pass because we may be in another (lower starting) range

    return lowest_permitted


def count_permitted_values(input_lines):
    # parse all the input_lines
    ranges = [parse_input_line(i) for i in input_lines]

    # use a 4GB long bitarray
    address_space = bitarray(2**32)
    address_space[:]=True       # use True to be 'allowed'

    # disallow all excluded ranges
    for lower, upper in ranges:
        address_space[lower:upper+1]=False

    # count the allowed...
    return address_space.count(True)


if __name__ == '__main__':
    #print(find_smallest_permitted_value(['5-8', '0-2', '4-7']))

    with(open('input_20a.txt', 'r')) as infile:
        range_lines = infile.read().splitlines()

    print(find_smallest_permitted_value(range_lines))
    print(count_permitted_values(range_lines))

