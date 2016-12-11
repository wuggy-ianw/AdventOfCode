import unittest

from day11 import State, Generator, Microchip, find_shortest_move_sequence, does_floor_contain_only_compatible_items, move_items_by_elevator_between_floors


def unordered_lists_equal(a,b):
    if len(a) != len(b):
        return False    # unequal lengths

    for x in a:
        found = False
        for y in b:
            if x==y:
                found = True
                break

        # an item in a was not found in b
        if not found:
            return False

    # all items must have been found
    return True

class Day11Tests(unittest.TestCase):

    def test_does_floor_contain_only_compatible_items(self):
        # an empty floor should contain only compatible items
        result = does_floor_contain_only_compatible_items(set())
        self.assertTrue(result)

        # a floor with only microchip items contains only compatible items
        result = does_floor_contain_only_compatible_items({Microchip('hydrogen'), Microchip('helium'), Microchip('lithium')})
        self.assertTrue(result)

        # a floor with only generator items contains only compatible items
        result = does_floor_contain_only_compatible_items({Generator('hydrogen'), Generator('helium'), Generator('lithium')})
        self.assertTrue(result)

        # a floor with a mismatched microchip and generator contains incompatible items
        result = does_floor_contain_only_compatible_items({Microchip('hydrogen'), Generator('helium')})
        self.assertFalse(result)

        # a floor with mismatched microchips and generators contains incompatible items
        result = does_floor_contain_only_compatible_items({Microchip('hydrogen'), Microchip('helium'), Generator('helium')})
        self.assertFalse(result)

        # a floor with a matched microchips and generators contains compatible items
        result = does_floor_contain_only_compatible_items({Microchip('hydrogen'), Microchip('helium'), Generator('hydrogen'), Generator('helium')})
        self.assertTrue(result)


    def test_move_items_by_elevator_between_floors1(self):
        # trying to move items from an empty floor to another floor produces no valid moves
        state = State([frozenset(), frozenset()])
        new_states = move_items_by_elevator_between_floors(0, 1, state, {})
        self.assertEqual(new_states, [])

    def test_move_items_by_elevator_between_floors2(self):
        # trying to move items from a floor with a single item to an empty floor produces one valid move
        state = State([{Microchip('hydrogen')}, frozenset()])
        new_states = move_items_by_elevator_between_floors(0, 1, state, {})

        expected = [State([frozenset(), {Microchip('hydrogen')}], elevator_floor = 1, parent = state)]
        self.assertEqual(new_states, expected)


    def test_move_items_by_elevator_between_floors3(self):
        # trying to move items from a floor with two items to a floor where one of those items is incompatible a produces one valid move
        state = State([{Microchip('hydrogen'), Microchip('helium')},
                       {Generator('helium')}
                      ])
        new_states = move_items_by_elevator_between_floors(0, 1, state, {})


        expected = [State([{Microchip('hydrogen')},
                           {Microchip('helium'), Generator('helium')}], elevator_floor = 1, parent = state)]
        self.assertEqual(new_states, expected)


    def test_move_items_by_elevator_between_floors4(self):
        # trying to move a generator and it's chip to another floor containing an incompatible generator is a valid move
        state = State([{Generator('helium'), Microchip('helium')},
                       {Generator('lithium')}])
        new_states = move_items_by_elevator_between_floors(0, 1, state, {})

        # two valid moves: moving just the helium-generator and moving both the helium microchip and generator together
        expected = [State([{Microchip('helium')},
                           {Generator('helium'), Generator('lithium')}], elevator_floor=1, parent=state),
                    State([frozenset(),
                           {Generator('helium'), Microchip('helium'), Generator('lithium')}], elevator_floor=1, parent=state)]
        self.assertEqual(set(new_states), set(expected))

    def test_move_items_by_elevator_between_floors5(self):
        # when there are multiple possible moves, make sure they're all available
        state = State([set(),
                       {Generator('hydrogen'), Generator('helium'), Generator('lithium')}], elevator_floor = 1)
        new_states = move_items_by_elevator_between_floors(1, 0, state, {})

        # many valid moves: we can move all the 1- and 2-item combinations
        expected = [State([{Generator('hydrogen')},
                               {Generator('helium'), Generator('lithium')}], parent=state),
                    State([{Generator('helium')},
                               {Generator('hydrogen'), Generator('lithium')}], parent=state),
                    State([{Generator('lithium')},
                                {Generator('hydrogen'), Generator('helium')}], parent=state),
                    State([{Generator('hydrogen'), Generator('helium')},
                                {Generator('lithium')}], parent=state),
                    State([{Generator('hydrogen'), Generator('lithium')},
                                {Generator('helium')}], parent=state),
                    State([{Generator('helium'), Generator('lithium')},
                                {Generator('hydrogen')}], parent=state)]
        self.assertEqual(set(new_states), set(expected))



    def test_move_items_by_elevator_between_floors6(self):
        # when there are multiple possible moves, make sure they're all available
        # we should also be able to EXCLUDE states that we've already encountered
        state = State([set(),
                       {Generator('hydrogen'), Generator('helium'), Generator('lithium')}], elevator_floor = 1)

        excluded = [State([{Generator('lithium')},
                                {Generator('hydrogen'), Generator('helium')}], parent=state),
                    State([{Generator('hydrogen'), Generator('helium')},
                                {Generator('lithium')}], parent=state),
                    State([{Generator('hydrogen'), Generator('lithium')},
                                {Generator('helium')}], parent=state)]

        new_states = move_items_by_elevator_between_floors(1, 0, state, excluded)

        # many valid moves: we can move all the 1- and 2-item combinations
        # excluding some that we will move out of expected
        expected = [State([{Generator('hydrogen')},
                               {Generator('helium'), Generator('lithium')}], parent=state),
                    State([{Generator('helium')},
                               {Generator('hydrogen'), Generator('lithium')}], parent=state),
                    State([{Generator('helium'), Generator('lithium')},
                                {Generator('hydrogen')}], parent=state)]

        self.assertTrue(unordered_lists_equal(new_states, expected))



    def test_example(self):
            # The first floor contains a hydrogen-compatible microchip and a lithium-compatible microchip.
            # The second floor contains a hydrogen generator.
            # The third floor contains a lithium generator.
            # The fourth floor contains nothing relevant.
            # In this arrangement, it takes 11 steps to collect all of the objects at the fourth floor for assembly.
            startstate = State([{Microchip('hydrogen'), Microchip('lithium')},
                           {Generator('hydrogen')},
                           {Generator('lithium')},
                           set()
                          ])

            # find the end-state
            moves = find_shortest_move_sequence(startstate)
            self.assertEqual(len(moves), 12)        # 11 + 1 for the initial state


if __name__ == '__main__':
    unittest.main()
