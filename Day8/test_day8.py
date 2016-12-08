import unittest
import numpy as np

from day8 import DrawRectCommand, RotateRowCommand, RotateColumnCommand, apply_draw_commands


# For example, here is a simple sequence on a smaller screen:
#
#     rect 3x2 creates a small rectangle in the top-left corner:
#
#     ###....
#     ###....
#     .......
#
#     rotate column x=1 by 1 rotates the second column down by one pixel:
#
#     #.#....
#     ###....
#     .#.....
#
#     rotate row y=0 by 4 rotates the top row right by four pixels:
#
#     ....#.#
#     ###....
#     .#.....
#
#     rotate column x=1 by 1 again rotates the second column down by one pixel, causing the bottom pixel to wrap back to the top:
#
#     .#..#.#
#     #.#....
#     .#.....

class Day8Tests(unittest.TestCase):

    def tstcore_command(self, cls, matchtext, state, expected):
        # given a non-match, it should return None
        result = cls.match_and_create('nonsense')
        self.assertEqual(result, None)

        # given a valid command, should produce a command object
        command = cls.match_and_create(matchtext)
        self.assertIsInstance(command, cls)

        # performing the command on an empty state should draw a rectangle of the right size
        command.perform(state)
        self.assertTrue(np.array_equal(state, expected))


    def test_DrawRectCommand(self):
        # test follows the first rect command in the example
        matchtext = 'rect 3x2'
        state = np.zeros((3,7))
        expected = np.array([[1, 1, 1, 0, 0, 0, 0],
                             [1, 1, 1, 0, 0, 0, 0],
                             [0, 0, 0, 0, 0, 0, 0]])
        self.tstcore_command(DrawRectCommand, matchtext, state, expected)

    def test_RotateColumnCommand(self):
        # test follows the first rotate columns command in the example
        matchtext = 'rotate column x=1 by 1'
        state = np.array([[1, 1, 1, 0, 0, 0, 0],
                          [1, 1, 1, 0, 0, 0, 0],
                          [0, 0, 0, 0, 0, 0, 0]])
        expected = np.array([[1, 0, 1, 0, 0, 0, 0],
                             [1, 1, 1, 0, 0, 0, 0],
                             [0, 1, 0, 0, 0, 0, 0]])
        self.tstcore_command(RotateColumnCommand, matchtext, state, expected)


    def test_RotateRowCommand(self):
        # test follows the first rotate row command in the example
        matchtext = 'rotate row y=0 by 4'
        state = np.array([[1, 0, 1, 0, 0, 0, 0],
                          [1, 1, 1, 0, 0, 0, 0],
                          [0, 1, 0, 0, 0, 0, 0]])
        expected = np.array([[0, 0, 0, 0, 1, 0, 1],
                             [1, 1, 1, 0, 0, 0, 0],
                             [0, 1, 0, 0, 0, 0, 0]])
        self.tstcore_command(RotateRowCommand, matchtext, state, expected)

    def test_apply_draw_commands(self):
        # test applies all the steps of the example
        commands = ['rect 3x2',
                    'rotate column x=1 by 1',
                    'rotate row y=0 by 4',
                    'rotate column x=1 by 1']
        state = np.zeros((3,7), dtype=np.int32)
        apply_draw_commands(state, commands)

        expected = np.array([[0, 1, 0, 0, 1, 0, 1],
                             [1, 0, 1, 0, 0, 0, 0],
                             [0, 1, 0, 0, 0, 0, 0]])
        self.assertTrue(np.array_equal(state, expected))

if __name__ == '__main__':
    unittest.main()
