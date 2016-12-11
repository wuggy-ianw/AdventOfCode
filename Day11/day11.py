import itertools
from functools import partial

class Generator(object):
    def __init__(self, element):
        self.element = element

    def isCompatibleWith(self, items):
        # generators can be on a floor with any other item without exploding
        return True

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.element == other.element

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return hash((self.__class__.__name__, self.element))

    def __repr__(self):
        return '<%s %s>' % (self.__class__.__name__, self.element)


class Microchip(object):
    def __init__(self, element):
        self.element = element

    def isCompatibleWith(self, items):
        # microchips can only be on a floor with a generator
        compatible = True   # if there's no generators, we're compatible
        for i in items:
            if isinstance(i, Generator):
                if i.element == self.element:
                    # if we're on a floor with a compatible generator, we're shielded
                    compatible = True
                    break
                else:
                    # if we're on a floor with a generator (and not shielded) then we're not compatible
                    compatible = False

        return compatible

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.element == other.element

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return hash((self.__class__.__name__, self.element))

    def __repr__(self):
        return '<%s %s>' % (self.__class__.__name__, self.element)


class State(object):
    def __init__(self, floors, elevator_floor = 0, parent = None, depth = 0, num_items = None):
        self.elevator_floor = elevator_floor
        self.depth = depth
        self.parent = parent
        self.floors = [ frozenset(f) for f in floors ]

        if num_items:
            self.num_items = num_items
        else:
            self.num_items = sum([len(f) for f in self.floors])

    def clone(self):
        return State(self.floors, self.elevator_floor, self, self.depth + 1, self.num_items)

    def __eq__(self, other):
        # equivalence is based on elevator position and floor items, not depth or parent etc
        return isinstance(other, self.__class__) and self.elevator_floor == other.elevator_floor and self.floors == other.floors

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        # our hash is based on floor config and elevator position
        return hash((self.__class__.__name__, self.elevator_floor, *self.floors))

    def __repr__(self):
        return '<%s %d %d %s>' % (self.__class__.__name__, self.depth, self.elevator_floor, self.floors)



def does_floor_contain_only_compatible_items(floor_items):
    compatible = [f.isCompatibleWith(floor_items) for f in floor_items]
    return all(compatible)



def is_state_in_state_list(a, states):
    return a in states


def move_items_by_elevator_between_floors(from_floor, to_floor, state, excluded_states):
    """
    Given a state, generate states for all the possible moves from that state. A valid move
    will move one or two items from one floor to another iff both floors still have a compatible
    set of items (i.e. no chips will be fried). States that already exist in excluded_states will
    be ignored and not included in the output.

    :param from_floor: integer index of the source floor
    :param to_floor: integer index of the destination floor
    :param state: a State object holding a valid state
    :param excluded_states: a set of State objects which should not be included in the output
    :return: a list of states
    """
    # trying to move items to a non-existant floor just returns no new states
    if to_floor < 0 or to_floor >= len(state.floors):
        return []

    states = []

    # the elevator can move 1 or 2 items from the current floor to the adjacent floor
    for n_items in range(1,3):
        for items_to_move in itertools.combinations(state.floors[from_floor], n_items):
            # given these items to move, get the set of items on each floor we're changing
            items_on_source_floor_after_move = state.floors[from_floor] - frozenset(items_to_move)
            items_on_dest_floor_after_move = state.floors[to_floor] | frozenset(items_to_move)

            # check both the source and dest floor item sets don't fry anything
            if does_floor_contain_only_compatible_items(items_on_source_floor_after_move) and \
               does_floor_contain_only_compatible_items(items_on_dest_floor_after_move):

                # make a candidate state
                state_after_move = state.clone()
                state_after_move.elevator_floor = to_floor
                state_after_move.floors[to_floor] = items_on_dest_floor_after_move
                state_after_move.floors[from_floor] = items_on_source_floor_after_move

                # if we've not already encountered this state, include it in the valid states we can make with this move
                if state_after_move not in excluded_states:
                    states.append(state_after_move)

    return states


def move_items_by_elevator(state, excluded_states):
    """
    Given a state, generate states for all the possible moves from that state, moving items up or down
    one floor.

    :param state: a State object
    :param excluded_states: a set of State objects which should not be included in the output
    :return: a list of states
    """
    current_floor = state.elevator_floor

    up_states = move_items_by_elevator_between_floors(current_floor, current_floor + 1, state, excluded_states)
    down_states = move_items_by_elevator_between_floors(current_floor, current_floor - 1, state, excluded_states)

    return up_states + down_states



def is_end_state(state):
    """
    Check if this state is the end-state, where all the items are on the top floor

    :param state: a State object to check
    :return: True or False
    """
    return len(state.floors[-1]) == state.num_items


def find_shortest_move_sequence_endstate_batch(startstate, checkpointlog = True):
    """
    Find the end-state of the lowest-depth move sequence using a batch-wise BFS.

    :param startstate: The initial state to work from
    :param checkpointlog: If True, prints some diagnostics before processing every batch
    :return: a State object which is the end-state
    """
    active_states = frozenset([startstate])
    history = set([startstate])

    depth = 0
    while True:
        assert len(active_states)>0

        if checkpointlog:
            print('nactive=' + str(len(active_states)) + ' depth=' + str(depth))

        # get all the new states we can reach from this state
        partial_move_items_by_elevator = partial(move_items_by_elevator, excluded_states = history)
        new_states_for_moves = map(partial_move_items_by_elevator, active_states)

        # next batch of active_states is the new set of states
        active_states = frozenset(itertools.chain.from_iterable(new_states_for_moves))
        history.update(active_states)

        # if any of the new states are the end state, then we're done
        for ns in active_states:
            if is_end_state(ns):
                return ns

        depth += 1


default_solver_corefunc = find_shortest_move_sequence_endstate_batch


def find_shortest_move_sequence(startstate, corefunc = default_solver_corefunc):
    """
    Find the shortest sequence of moves to place all the generators and microprocessors on the topmost floor.

    :param startstate: State object with the initial placement of microprocessors and generators
    :param corefunc: An alternative function for finding the solution state. The default does a simple batch-BFS.
    :return: a list of State objects, starting with the start state plus one for each move made, ending in the solution state
    """
    # find the end-state
    solutionstate = corefunc(startstate)

    # work up the tree and get the list of moves
    moves_solution_to_root = [solutionstate]
    while moves_solution_to_root[-1].parent:
        moves_solution_to_root.append(moves_solution_to_root[-1].parent)

    moves = list(reversed(moves_solution_to_root))
    return moves


def day11a_solver(corefunc = default_solver_corefunc):
    # elevator starts on the first floor
    # The first floor contains a promethium generator and a promethium-compatible microchip.
    # The second floor contains a cobalt generator, a curium generator, a ruthenium generator, and a plutonium generator.
    # The third floor contains a cobalt-compatible microchip, a curium-compatible microchip, a ruthenium-compatible microchip, and a plutonium-compatible microchip.
    # The fourth floor contains nothing relevant.
    startstate = State([
                      {Generator('promethium'), Microchip('promethium')},
                      {Generator('cobalt'), Generator('curium'), Generator('ruthenium'), Generator('plutonium')},
                      {Microchip('cobalt'), Microchip('curium'), Microchip('ruthenium'), Microchip('plutonium')},
                      set()
                  ])

    moves = find_shortest_move_sequence(startstate, corefunc)
    return len(moves) - 1   # -1 to exclude the initial state


def day11b_solver(corefunc = default_solver_corefunc):
    # elevator starts on the first floor
    # The first floor contains a promethium generator and a promethium-compatible microchip.
    # The second floor contains a cobalt generator, a curium generator, a ruthenium generator, and a plutonium generator.
    # The third floor contains a cobalt-compatible microchip, a curium-compatible microchip, a ruthenium-compatible microchip, and a plutonium-compatible microchip.
    # The fourth floor contains nothing relevant.
    startstate = State([
                      {Generator('promethium'), Microchip('promethium'), Generator('elerium'), Microchip('elerium'), Generator('dilithium'), Microchip('dilithium')},
                      {Generator('cobalt'), Generator('curium'), Generator('ruthenium'), Generator('plutonium')},
                      {Microchip('cobalt'), Microchip('curium'), Microchip('ruthenium'), Microchip('plutonium')},
                      set()
                  ])

    moves = find_shortest_move_sequence(startstate, corefunc)
    return len(moves) - 1   # -1 to exclude the initial state



if __name__ == '__main__':
    print(day11a_solver())
    print(day11b_solver())

