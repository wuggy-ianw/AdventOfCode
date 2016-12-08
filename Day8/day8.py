import re
import numpy as np
import sys

# Command objects
#
# Two required methods:
#    match_and_create(commandtext): [static] if the command-text is valid for this command, create and return a command object, otherwise None.
#    perform(self,state): perform this command on state (in-place).

class DrawRectCommand(object):
    match_re = re.compile('rect ([0-9]+)x([0-9]+)')

    @staticmethod
    def match_and_create(commandtext):
        m = DrawRectCommand.match_re.match(commandtext)
        if not m:
            return None

        return DrawRectCommand(int(m.group(1)), int(m.group(2)))

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def perform(self, state):
        state[0:self.y, 0:self.x] = 1


class RotateRowCommand(object):
    match_re = re.compile('rotate row y=([0-9]+) by ([0-9]+)')

    @staticmethod
    def match_and_create(commandtext):
        m = RotateRowCommand.match_re.match(commandtext)
        if not m:
            return None

        return RotateRowCommand(int(m.group(1)), int(m.group(2)))

    def __init__(self, row, byrows):
        self.row = row
        self.byrows = byrows

    def perform(self, state):
        state[self.row,:] = np.roll(state[self.row,:], self.byrows)


class RotateColumnCommand(object):
    match_re = re.compile('rotate column x=([0-9]+) by ([0-9]+)')

    @staticmethod
    def match_and_create(commandtext):
        m = RotateColumnCommand.match_re.match(commandtext)
        if not m:
            return None

        return RotateColumnCommand(int(m.group(1)), int(m.group(2)))

    def __init__(self, column, bycolumns):
        self.column = column
        self.bycolumns = bycolumns

    def perform(self, state):
        state[:, self.column] = np.roll(state[:, self.column], self.bycolumns)

# list of the known command classes
command_classes = [DrawRectCommand, RotateRowCommand, RotateColumnCommand]


def get_command_object_or_fail(command):
    """
    Parses a string containing a command into a command object, or asserts if there's no matching command object

    :param command: string containing a command
    :return: A command object
    """
    for cmdclass in command_classes:
        cmd = cmdclass.match_and_create(command)
        if cmd:
            return cmd

    assert(False, "Command text didn't match any known commands")

def apply_draw_commands(state, commands):
    """
    Applies a list of command strings to an initial state

    :param state: A numpy array holding the state, zero for 'off', one for 'on', typically as an integer type
    :param commands: an array of strings containing display commands
    :return: nothing. state is updated 'in place'
    """
    # process the commands into command objects,
    commandobjs = [get_command_object_or_fail(command) for command in commands]

    # perform them all on the state
    for cmdobj in commandobjs:
        cmdobj.perform(state)

    return state

def print_state(state):
    """
    Pretty print the display, splitting it along expected character groups
    :param state: A numpy array holding the state
    :return: nothing. Writes to stdout.
    """
    statesize = state.shape
    for y in range(0,statesize[0]):
        sys.stdout.write('\r\n')
        for x in range(0,statesize[1]):
            if x != 0 and (x % 5) == 0:
                sys.stdout.write(' ')
            if state[y, x]:
                sys.stdout.write('#')
            else:
                sys.stdout.write('.')


if __name__ == '__main__':
    with(open('input_8a.txt', 'r')) as infile:
        commands = infile.read().splitlines()

    state = apply_draw_commands(np.zeros((6,50), dtype=np.int32), commands)
    print(sum(sum(state)))

    print_state(state)
