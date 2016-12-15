import collections

Disc = collections.namedtuple('Disc', ['n_pos', 'pos'])

def gcd(a,b):
    """
    Compute the greatest common divisor of a pair of numbers.

    :param a: integer
    :param b: integer
    :return: the gcd of a and b
    """
    while b:
        a, b = b, a % b
    return a


def lcm(nums):
    """
    Compute the lowest common multiple of a list of numbers

    :param nums: list of integers
    :return: the lcm of nums
    """
    lcm = nums[0]
    for i in nums[1:]:
        lcm = (lcm * i) / gcd(lcm, i)
    return int(lcm)     # the division converts this to float, but it will always be an integer


def aligned_pos(npos, index):
    """
    Get the position a disc with a given number of positions at a given (zero-based) index would need to be
    at in order for a ball to pass through.

    :param npos: number of positions for this disc
    :param index: the index (into out disc array, zero-based) for the disc
    :return: the aligned position
    """
    ap = npos - (index + 1)  # +1 since the time to the first disc is 1 second
    while ap < 0:
        ap = ((npos * 100) + ap) % npos

    return ap


def indices_of_aligned_discs(discs):
    return [i for i,d in enumerate(discs) if d.pos == aligned_pos(d.n_pos, i)]


def move_discs_forward(time_steps, discs):
    """
    Move all the discs forward to their position after adding a number of time_steps

    :param time_steps: number of time steps to move forward
    :param discs: the current state of the discs
    :return: Nothing, discs is updated in place
    """
    for i, d in enumerate(discs):
        discs[i] = Disc( d.n_pos, (d.pos + time_steps) % d.n_pos )


def find_time_discs_are_aligned(initial_discs):
    """
    Determine the time that all discs are aligned.

    :param initial_discs: a list of Disc objects in their initial positions
    :return: an integer, the time step (seconds) at which the ball will pass through all the discs
    """
    # get a time-adjusted copy of the discs so that we can process things without time-delta between discs
    discs = initial_discs[:]        # copy, since we'll be updating in-place
    t = 0

    # check if we're already aligned
    aligned_i = indices_of_aligned_discs(discs)
    done = (len(aligned_i) == len(discs))

    while not done:
        # if we don't have any aligned discs, then just step by 1
        if len(aligned_i) == 0:
            step = 1
        else:
            # move forward by the lcm of the aligned disc sizes
            # this will keep those discs aligned...
            step = lcm([discs[i].n_pos for i in aligned_i])

        # move the position forward
        move_discs_forward(step, discs)
        t += step

        # check for aligned discs
        aligned_i = indices_of_aligned_discs(discs)
        done = (len(aligned_i) == len(discs))

    return t


def day15a_solver():
    # Disc #1 has 17 positions; at time=0, it is at position 15.
    # Disc #2 has 3 positions; at time=0, it is at position 2.
    # Disc #3 has 19 positions; at time=0, it is at position 4.
    # Disc #4 has 13 positions; at time=0, it is at position 2.
    # Disc #5 has 7 positions; at time=0, it is at position 2.
    # Disc #6 has 5 positions; at time=0, it is at position 0.
    discs = [ Disc(17, 15),
              Disc(3, 2),
              Disc(19, 4),
              Disc(13, 2),
              Disc(7, 2),
              Disc(5, 0) ]

    return find_time_discs_are_aligned(discs)

def day15b_solver():
    # When it's done, the discs are back in their original configuration
    # as if it were time=0 again, but a new disc with 11 positions and starting
    # at position 0 has appeared exactly one second below the previously-bottom disc.
    discs = [ Disc(17, 15),
              Disc(3, 2),
              Disc(19, 4),
              Disc(13, 2),
              Disc(7, 2),
              Disc(5, 0),
              Disc(11, 0)]

    return find_time_discs_are_aligned(discs)


if __name__ == '__main__':
    print(day15a_solver())
    print(day15b_solver())


