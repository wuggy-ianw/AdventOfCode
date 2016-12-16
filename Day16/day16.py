import numpy as np

def dragon_extend(a):
    """
    Extend a boolean array following the rules similar to the 'dragon' fractal

    :param a: numpy array
    :return: numpy array of double length + 1, extended following the rules
    """
    # Call the data you have at this point "a".
    # Make a copy of "a"; call this copy "b".
    # Reverse the order of the characters in "b".
    # In "b", replace all instances of 0 with 1 and all 1s with 0.
    # The resulting data is "a", then a single 0, then "b".

    ab = np.zeros( 1 + (len(a)*2) )
    ab[0:len(a)] = a
    ab[len(a)+1:] = np.logical_not(a[::-1])

    return ab

def collapse(a):
    """
    Collapse a boolean array following the checksum rules

    :param a: numpy array
    :return: numpy array of half the lengh
    """
    # The checksum for some given data is created by considering each non-overlapping pair of
    # characters in the input data. If the two characters match (00 or 11), the next checksum
    # character is a 1. If the characters do not match (01 or 10), the next checksum character
    # is a 0. This should produce a new string which is exactly half as long as the original.

    b = (a[::2] == a[1::2])
    return b


def day16_solver(fill_len, state):
    while len(state)<fill_len:
        state = dragon_extend(state)

    truncated_state = state[0:fill_len]
    while len(truncated_state) % 2 == 0:
        truncated_state = collapse(truncated_state)

    return ''.join([str(int(x)) for x in truncated_state])



def day16a_solver():
    return day16_solver(272, np.array([0,1,1,1,0,1,1,0,1,0,1,0,0,1,0,0,0]))

def day16b_solver():
    return day16_solver(35651584, np.array([0,1,1,1,0,1,1,0,1,0,1,0,0,1,0,0,0]))


if __name__ == '__main__':
    print(day16a_solver())
    print(day16b_solver())

