import unittest
from day17 import Day17PathFinder


class Day17Tests(unittest.TestCase):

    def test_moves_from_pos1(self):
        # For example, suppose the passcode is hijkl. Initially, you have taken no steps, and so
        # your path is empty: you simply find the MD5 hash of hijkl alone. The first four characters
        # of this hash are ced9, which indicate that up is open (c), down is open (e), left is open (d),
        # and right is closed and locked (9). Because you start in the top-left corner, there are no
        # "up" or "left" doors to be open, so your only choice is down.
        pf = Day17PathFinder('hijkl')
        moves = pf.moves_from_pos((0,0), '')
        expected = [((0,1), 'D')]
        self.assertEqual(frozenset(moves), frozenset(expected))

    def test_moves_from_pos2(self):
        # Next, having gone only one step (down, or D), you find the hash of hijklD. This produces f2bc,
        # which indicates that you can go back up, left (but that's a wall), or right.
        pf = Day17PathFinder('hijkl')
        moves = pf.moves_from_pos((0,1), 'D')
        expected = [((0,0), 'DU'), ((1,1), 'DR')]
        self.assertEqual(frozenset(moves), frozenset(expected))

    def test_moves_from_pos3(self):
        # Going right means hashing hijklDR to get 5745 - all doors closed and locked.
        pf = Day17PathFinder('hijkl')
        moves = pf.moves_from_pos((1,1), 'DR')
        expected = []
        self.assertEqual(frozenset(moves), frozenset(expected))

    def test_moves_from_pos4(self):
        # After going DU (and then hashing hijklDU to get 528e), only the right door is open;
        pf = Day17PathFinder('hijkl')
        moves = pf.moves_from_pos((0,0), 'DU')
        expected = [((1,0), 'DUR')]
        self.assertEqual(frozenset(moves), frozenset(expected))

        # after going DUR, all doors lock. (Fortunately, your actual passcode is not hijkl).
        moves = pf.moves_from_pos((1, 0), 'DUR')
        expected = []
        self.assertEqual(frozenset(moves), frozenset(expected))


    def test_example1(self):
        # If your passcode were ihgpwlah, the shortest path would be DDRRRD.
        pf = Day17PathFinder('ihgpwlah')
        sp = pf.find_shortest_path()
        self.assertEqual(sp, 'DDRRRD')

    def test_example2(self):
        # With kglvqrro, the shortest path would be DDUDRLRRUDRD.
        pf = Day17PathFinder('kglvqrro')
        sp = pf.find_shortest_path()
        self.assertEqual(sp, 'DDUDRLRRUDRD')

    def test_example3(self):
        # With ulqzkmiv, the shortest would be DRURDRUDDLLDLUURRDULRLDUUDDDRR.
        pf = Day17PathFinder('ulqzkmiv')
        sp = pf.find_shortest_path()
        self.assertEqual(sp, 'DRURDRUDDLLDLUURRDULRLDUUDDDRR')

    def test_longest_example1(self):
        # If your passcode were ihgpwlah, the longest path would take 370 steps.
        pf = Day17PathFinder('ihgpwlah')
        sp = pf.find_longest_path()
        self.assertEqual(len(sp), 370)

    def test_longest_example2(self):
        # With kglvqrro, the longest path would be 492 steps long.
        pf = Day17PathFinder('kglvqrro')
        sp = pf.find_longest_path()
        self.assertEqual(len(sp), 492)

    def test_longest_example3(self):
        # With ulqzkmiv, the longest path would be 830 steps long.
        pf = Day17PathFinder('ulqzkmiv')
        sp = pf.find_longest_path()
        self.assertEqual(len(sp), 830)


if __name__ == '__main__':
    unittest.main()
