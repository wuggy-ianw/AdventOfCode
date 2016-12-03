#
# solution for the second puzzle of Advent of Code: http://adventofcode.com/2016/day/2
#

import numpy as np

# permitted keypad move directions
keypad_move_offsets = {'U': np.array([ 0, -1]),
                       'D': np.array([ 0,  1]),
                       'L': np.array([-1,  0]),
                       'R': np.array([ 1,  0])}
keypad_move_directions = keypad_move_offsets.keys()


def keypad_to_state_machine(keypad):
    """
    Build a state-machine dictionary from a 2D description of the keypad

    :param keypad: a list of strings (top to bottom) describing the keypad. Spaces are blank. Should be rectangular, but blank parts at the ends may be trimmed.
    :return: a dictionary d such that d[key][direction], if present, gives the key we reach after moving in direction
    """
    def key_at_pos(pos):
        if pos[1]<0 or pos[1]>=len(keypad):
            return None

        l = keypad[pos[1]]
        if (pos[0]<0 or pos[0]>=len(l)):
            return None

        k=l[pos[0]]
        if k==' ': return None

        return k

    statemachine={}

    # for each key in the grid
    for y in range(len(keypad)):
        for x in range(len(keypad[y])):
            pos = np.array([x,y])
            keyhere = key_at_pos(pos)
            if keyhere is not None:
                statemachine[keyhere]={}

                # check each of the move directions for another key
                for move, moveoffset in keypad_move_offsets.items():
                    key_at_move = key_at_pos(pos+moveoffset)
                    if key_at_move is not None:
                        # add a transition from keyhere to key_at_move in the move direction
                        statemachine[keyhere][move]=key_at_move

    return statemachine

# state machine of which key is arrived at after following each move
keypad_position_after_move_9digit = keypad_to_state_machine(['123',
                                                             '456',
                                                             '789'])
keypad_position_after_move_13digit = keypad_to_state_machine(['  1  ',
                                                              ' 234 ',
                                                              '56789',
                                                              ' ABC ',
                                                              '  D  '])

def solver(instructionlist, keypad_position_after_move = keypad_position_after_move_9digit):
    """
    Process a keycode instruction list and determine the keycode.

    :param instructionlist: a list of strings containing keypad moves
    :return: a string containing the keypad code
    """

    # start at key '5' and an empty keycode
    currentkey = '5'
    keycode = []

    # for each line, perform the moves
    for instructionline in instructionlist:

        # for each move, update the current key position following the state machine
        for move in instructionline:
            if move in keypad_position_after_move[currentkey]:
                currentkey = keypad_position_after_move[currentkey][move]

        # the key we're currently at once we've made all the moves on the line is the digit to press
        keycode.append(currentkey)

    return "".join(keycode)



if __name__ == '__main__':
    with(open('input_2a.txt', 'r')) as infile:
        instructionlist = infile.read().splitlines()

    print(solver(instructionlist))
    print(solver(instructionlist, keypad_position_after_move_13digit))

