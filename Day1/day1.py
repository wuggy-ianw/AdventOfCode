#
# solution for the first puzzle of Advent of Code: http://adventofcode.com/2016/day/1
#

import numpy as np      # for vector maths

# the permitted cardinal directions
cardinal_directions = ['north', 'south', 'east', 'west']

# the permitted turn directions (as expected from input)
turn_directions = ['L', 'R']

# mapping from cardinal direction to new direction after applying a given turn
cardinal_direction_turn_map = {'north': {'L': 'west', 'R': 'east'},
                               'south': {'L': 'east', 'R': 'west'},
                               'east':  {'L': 'north', 'R': 'south'},
                               'west':  {'L': 'south', 'R': 'north'}}


# mapping from cardinal direction to position update
# positions are such that moving eastwards and northwards are considered +ive
cardinal_direction_position_delta_map = {'north': np.array([ 0,  1]),
                                         'south': np.array([ 0, -1]),
                                         'east':  np.array([ 1,  0]),
                                         'west':  np.array([-1,  0])}


def apply_turn_to_cardinal_direction(turn, direction):
    """
    Perform a turn from one cardinal direction to a new

    :param turn: A turn direction, must be 'L' or 'R'
    :param direction: The facing direction
    :return: The new facing direction after turning
    """
    assert(turn in turn_directions)
    assert(direction in cardinal_directions)

    return cardinal_direction_turn_map[direction][turn]


def apply_cardinal_direction_to_position(position, direction, distance, onvisit):
    """
    Perform a move in a given cardinal direction to a position.

    :param position: an [x,y] ndarray with the current position to apply the directional move from
    :param direction: the cardinal direction to move toward
    :param distance: the distance to move
    :param onvisit: callable that will be called for every position crossed taking this move
    :return: a new [x,y] ndarray with the updated position
    """
    assert(direction in cardinal_directions)

    # take the steps one at a time so that we touch all [x,y] positions along the path
    newpos = position
    for i in range(distance):
        newpos = newpos + cardinal_direction_position_delta_map[direction]
        if onvisit:
            onvisit(newpos)

    return newpos


def apply_step_instruction(step, position, direction, onvisit):
    """
    Applies a step from a given position and facing direction

    :param step: step descriptor (e.g 'L20' for left-then-20-steps)
    :param position: an [x,y] ndarray with the current position
    :param direction: the current facing cardinal direction
    :param onvisit: callable that will be called for every position crossed taking this move
    :return: a tuple of (newpos, newdir) where newpos is the updated position and newdir is the updated facing position after applying the step
    """
    # parse the step into turn and distance parts
    assert(len(step) >= 2)

    turn = step[0]
    assert(turn in turn_directions)

    distance = int(step[1:])

    # apply the turn to get the updated cardinal facing direction
    newdirection = apply_turn_to_cardinal_direction(turn, direction)

    # update the position by heading the distance in that direction
    newpos = apply_cardinal_direction_to_position(position, newdirection, distance, onvisit)

    return newpos, newdirection


def solver(stepinstructions, stop_at_crossing=False):
    """
    Solver for the first puzzle: find the distance to the end-point of a sequence of step instructions.
    The step instructions are a comma-seperated string of steps, where each step is left or right turn
    denoted by 'L' and 'R', followed by a given number of steps forward. (E.g. 'L2, R10, L2').

    The endpoint co-ordinates are [x,y] where East is +ive x and North is +ive y.

    :param stepinstructions: String holding the comma separated list of step instructions
    :param core: a callable specific solver for todays a/b variants
    :return: A tuple of (distance, position) where distance is the grid-distance (i.e. L1-norm) to the end point, and position is an [x,y] list holding the endpoint.
    """
    # initial state is facing north at the origin position
    direction = 'north'
    pos=np.array([0,0])

    # split the input into a list of step instructions
    steps = [x.strip() for x in stepinstructions.split(',')]

    solutionpos = None
    onvisit = None
    if stop_at_crossing:
        visited = set()

        def capture_first_crossing(pos):
            nonlocal solutionpos
            if solutionpos is None:
                if tuple(pos) in visited:
                    solutionpos = pos
                else:
                    visited.add(tuple(pos))

        onvisit = capture_first_crossing
    else:
        def capture_last_position(pos):
            nonlocal solutionpos
            solutionpos = pos
        onvisit = capture_last_position

    # apply the steps
    # onvisit will have set the solutionpos
    for step in steps:
        pos, direction = apply_step_instruction(step, pos, direction, onvisit)

    # the distance from the origin is the L1-norm of the position
    dist = np.sum(np.abs(solutionpos))

    return dist, list(solutionpos)


if __name__ == '__main__':
    puzzleinput = 'R2, L5, L4, L5, R4, R1, L4, R5, R3, R1, L1, L1, R4, L4, L1, R4, L4, R4, L3, R5, R4, R1, R3, L1, ' +\
                  'L1, R1, L2, R5, L4, L3, R1, L2, L2, R192, L3, R5, R48, R5, L2, R76, R4, R2, R1, L1, L5, L1, ' +\
                  'R185, L5, L1, R5, L4, R1, R3, L4, L3, R1, L5, R4, L4, R4, R5, L3, L1, L2, L4, L3, L4, R2, R2, ' +\
                  'L3, L5, R2, R5, L1, R1, L3, L5, L3, R4, L4, R3, L1, R5, L3, R2, R4, R2, L1, R3, L1, L3, L5, R4, ' +\
                  'R5, R2, R2, L5, L3, L1, L1, L5, L2, L3, R3, R3, L3, L4, L5, R2, L1, R1, R3, R4, L2, R1, L1, R3, ' +\
                  'R3, L4, L2, R5, R5, L1, R4, L5, L5, R1, L5, R4, R2, L1, L4, R1, L1, L1, L5, R3, R4, L2, R1, R2, ' +\
                  'R1, R1, R3, L5, R1, R4'
    print(solver(puzzleinput))
    print(solver(puzzleinput, True))
