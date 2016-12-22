import sys
import re
import collections
import numpy as np
from copy import copy
import hashlib
import heapq


GridNode = collections.namedtuple('GridNode', ['x', 'y', 'size', 'used', 'avail'])

match_df_input_line_re = re.compile(r'\/dev\/grid\/node-x([0-9]+)-y([0-9]+)\s+([0-9]+)T\s+([0-9]+)T\s+([0-9]+)T\s+([0-9]+)\%')
def parse_df_input_line(line):
    match = match_df_input_line_re.match(line)
    assert match, "Failed to parse input line"

    return GridNode(x=int(match.group(1)), y=int(match.group(2)), size=int(match.group(3)),
                    used=int(match.group(4)), avail=int(match.group(5)))

def count_viable_pairs(nodes):
    """
    Given a list of nodes, count the number of nodes that can exchange data.

    :param nodes: a list of GridNodes
    :return: The number of node-pairs that can exchange data
    """
    # sort the nodes by 'used', exclude nodes that are empty
    nodes_by_used = filter(lambda x: x.used>0, sorted(nodes, key=lambda x: x.used))

    # sort the nodes by 'avail' (keeping empty nodes)
    nodes_by_available = sorted(nodes, key=lambda x: x.avail)

    # iterate through the nodes_by_used, there can only be 'fewer' nodes with that amount of space
    # available in nodes_by_available
    available_index = 0
    count = 0
    for used_node in nodes_by_used:
        # skip forward in available until we're past the end, or the available node has enough storage
        while available_index<len(nodes_by_available) and \
                nodes_by_available[available_index].avail<used_node.used:
            available_index += 1

        # if there are nodes that are available to contain this size, then count them
        if available_index<len(nodes_by_available):
            count += len(nodes_by_available) - available_index

            # check that the used_node can contain itself, and remove it from the count if so
            if used_node.avail >= used_node.used:
                count -= 1

    return count


def day22a_solver(nodes):
    return count_viable_pairs(nodes)


class PuzzleState(object):
    """
    A hashable object of the puzzle's state. This is specifically for sliding puzzle like problems. That is,
    puzzles where the is exactly one 'zero used' node, and that nodes are partionable into two sets: nodes that
    are large and 'full' such that their data can't be moved to any other node, nodes that are roughly the same
    size and can contain any of the data from other nodes of the same class if they were empty.
    """
    def __init__(self, source):
        """
        Create a new state.
        :param source: Either a PuzzleState object to produce a new clone, or a list of GridNode objects describing a grid.
        """
        self.move_pos = None
        self.move_delta = None

        # clone from a source state
        if isinstance(source, self.__class__):
            self.data_pos = copy(source.data_pos)
            self.zero_pos = source.zero_pos
            self.available_grid = source.available_grid.copy()
            self.used_grid = source.used_grid.copy()

            self.height = source.height
            self.width = source.width
        else:
            # otherwise assume it's a list of nodes that we can convert
            self._initialise_from_grid_node_list(source)

    def _initialise_from_grid_node_list(self, source):
        """
        Initialise this state from a list of GridNode objects
        :param source: a list of GridNode objects
        :return: Nothing. Updates self.
        """
        # find the max of the grid bounds
        max_x = 0
        max_y = 0
        for x,y,size,used,avail in source:
            max_x = max(max_x, x)
            max_y = max(max_y, y)

        self.width = max_x + 1
        self.height = max_y + 1

        # make a grid for available and used storage on each node, fill with a dummy value (-1)
        self.available_grid = np.ones((self.width, self.height), dtype=int) * -1
        self.used_grid = np.ones((self.width, self.height), dtype=int) * -1

        # fill the grid from our iterator
        for x,y,size,used,avail in source:
            assert self.available_grid[x, y] ==- 1, "Already encountered data for this grid node. Can't overwrite."
            assert self.used_grid[x, y] == -1, "Already encountered data for this grid node. Can't overwrite."

            self.available_grid[x,y]=avail
            self.used_grid[x,y]=used

        # check that the grid is actually full!
        assert -1 not in self.available_grid, "Didn't entirely fill the grid..."
        assert -1 not in self.used_grid, "Didn't entirely fill the grid..."

        # the position of our 'interesting data' is the top right corner
        self.data_pos = (max_x, 0)

        # find the position of the empty cell
        self.zero_pos = self.find_zero_pos()

    def try_apply_move(self, delta):
        """
        Create a new state by trying a particular move.

        :param delta: A tuple (dx, dy) with the direction to move the zero block
        :return: A new PuzzleState object after performing this move, or None if the move isn't possible
        """
        # get the 'zero' and 'source' positions (we're moving 'source' to 'zero')
        zero_x, zero_y = self.zero_pos
        source_x, source_y = (zero_x - delta[0], zero_y - delta[1])

        # if the source is outside the bounds, it's not a possible move
        if source_x < 0 or source_x >= self.width or \
           source_y < 0 or source_y >= self.height:
            return None

        # if the zero_block has less storage available than to move data from the source, this move
        # isn't possible
        data_len = self.used_grid[source_x, source_y]
        if self.available_grid[zero_x, zero_y] < data_len:
            return None

        # clone ourselves, and move the data
        post_move_state = self.__class__(self)

        # move data into the zero position
        post_move_state.available_grid[zero_x, zero_y] -= data_len
        post_move_state.used_grid[zero_x, zero_y] += data_len

        # clear the data from the source position
        post_move_state.available_grid[source_x, source_y] += data_len
        post_move_state.used_grid[source_x, source_y] = 0

        # the source position is now empty, it's the new zero position
        post_move_state.zero_pos = (source_x, source_y)

        # if we're moving the data (from source to zero pos), then update the known data position
        if post_move_state.data_pos == (source_x, source_y):
            post_move_state.data_pos = (zero_x, zero_y)

        # record the move to reach this state
        post_move_state.move_pos = (source_x, source_y)
        post_move_state.move_delta = delta

        return post_move_state

    def find_zero_pos(self):
        """
        Locate the first zero-usage grid node.

        :return: a tuple (x,y)
        """
        for y in range(self.height):
            for x in range(self.width):
                if self.used_grid[x, y] == 0:
                    return x, y

        assert False, "Failed to find a zero-used grid node?"

    def __hash__(self):
        # since nodes are equivalent, the only things we need to include in the hash are the
        # place where the data is and the zero-usage grid node.
        return hash((self.data_pos, self.zero_pos))

    def __eq__(self, other):
        return self.data_pos == other.data_pos and \
                self.zero_pos == self.zero_pos

    def __ne__(self, other):
        return not self.__eq__(other)

    def visualise(self):
        """
        Create a visualisation of the state. For each node:
          if the data we want is at this node, mark it with 'G'
          if a node is empty, mark it with '_'
          if a node is too full to be moved to the empty node, mark it as '#' (i.e. it's immovable)
          otherwise, mark the node as '.' (i.e. it's movable, but contains data)
        :return: a list of strings that should be displayed in order
        """

        lines = []
        zero_x, zero_y = self.zero_pos
        for y in range(self.height):
            s = ''
            for x in range(self.width):
                if (x,y) == self.data_pos:
                    s += 'G'
                elif self.used_grid[x, y]==0:
                    s += '_'
                elif self.used_grid[x, y] > self.available_grid[zero_x, zero_y]:
                    s += '#'
                else:
                    s += '.'

            lines.append(s)
        return lines



def are_all_nodes_full_or_interchangable(nodes):
    """
    If all the nodes are mostly 'full', and so it's not possible to merge any 2-nodes data, then this
    puzzle collapses to a (modified) sliding block puzzle. That is, there is ONE empty node, and we can
    shuffle most nodes data into it. There may be SOME nodes that are too big/full to be moved.

    :param nodes: a list of GridNode tuples
    :return: True if this arrangement of nodes is 'sliding-block' like.
    """
    # sort the nodes by 'used'
    nodes_by_used = sorted(nodes, key=lambda x: x.used)

    # sort the nodes by 'avail', exclude all the zero-used
    nodes_by_available = list(filter(lambda x:x.used > 0, sorted(nodes, key=lambda x: x.avail)))

    # if there is ONE zero-node (least used is zero, and most available.used = 0) and the 'most' available node has less storage than
    # the least 'used' node (excluding the zero), then this is a sliding block puzzle
    return nodes_by_used[0].used == 0 and nodes_by_used[1].used > 0 and \
           nodes_by_available[-1].avail < nodes_by_used[1].used





class SlidingBlockSolver(object):
    """
    An A* based solver for sliding block style puzzles. Uses the PuzzleState extensively.
    """
    direction_deltas = [(-1, 0),
                        (1, 0),
                        (0, -1),
                        (0, 1)]

    def path_search_metric_astar_manhatten_sliding_block(self, state, path_len):
        # for sliding block puzzles, a good metric is normally the hamming distance to all the pieces being
        # in the right place. However, for this puzzle, we just care about the distance of the data we want
        # to the destination corner
        # So, this looks like using this metric is good:
        #   the length of the current path +
        #   the distance of the data block from the destination * (factor) +
        #      where factor is the min number of moves required to put the zero block somewhere to move the data forward
        #   the distance of the zero block from the data block
        # This *should* give the shortest number of moves, since the total metric after moving the zero block and
        # after moving the data block should always be equal or larger than the steps along the way.
        #
        # if the factor is too big, it may miss the shortest path
        # if the factor is too small, it will spend a long time searching pointless moves of the sliding block
        # 3-5 seems about right... to get from ..G_ to .G_. takes 5 moves while the other possible move (up/down)
        #                                      ....    ....
        # takes 3.
        return path_len + \
               sum([abs(a - b) for a, b in zip(state.data_pos, self.dest_pos)]) * 3 + \
               sum([abs(a - b) for a, b in zip(state.data_pos, state.zero_pos)])


    def __init__(self, state, metric = 'A*-manhatten-sliding-block'):
        metrics = {'A*-manhatten-sliding-block': self.path_search_metric_astar_manhatten_sliding_block}
        self.metric = metrics[metric]
        self.dest_pos = (0,0)

        self.visited = set()
        self.search_heap = []       # empty heaps are already heaps
        self.tie_breaker_index = 0

        self.add_state_to_heap_and_mark_visited(state)
        self.best_path = None

    def moves_from_state(self, state):
        """
        Explore the possible moves that can be performed from a given state

        :param state: a PuzzleState object
        :return: a list of new PuzzleState objects (possibly empty) for all the states we can move to, excluding
                 any states we've already visited
        """
        reachable_positions = []

        for delta in self.direction_deltas:
            candidate_state = state.try_apply_move(delta)
            if candidate_state and candidate_state not in self.visited:
                reachable_positions.append(candidate_state)

        return reachable_positions

    def add_state_to_heap_and_mark_visited(self, state, path=None):
        """
        Adds a state to the search heap and mark it visited.

        :param state: a PuzzleState object
        :param path: the list of PuzzleState objects (or None) which are the history of the 'state'
        :return: Nothing
        """
        # visit this state
        self.visited.add(state)

        # extend the path we've walked to include this state
        if path:
            path = copy(path)
        else:
            path = []
        path.append(state)

        # compute the metric
        metric = self.metric(state, len(path))

        # push a tuple to the heap of all this, ordered by metric then tie_breaker
        heapq.heappush(self.search_heap, (metric, self.tie_breaker_index, state, path))

        self.tie_breaker_index += 1

    def step(self, debugprint=False):
        """
        Perform one step of the path search algorithm. Take the 'best' candidate path and explore
        the possible moves from it.

        :param debugprint: If True, prints debug information
        :return: True, if we've reached the goal, False otherwise.
        """
        # take the 'best' item from the heap
        metric, tie_breaker, state, path = heapq.heappop(self.search_heap)

        if debugprint:
            print(metric, tie_breaker, state.data_pos, state.zero_pos, len(path), len(self.search_heap))

        # if we've reached the destination position
        if state.data_pos == self.dest_pos:
            self.best_path = path
            return True

        # get all the visitable positions and push them on the heap
        for v in self.moves_from_state(state):
            self.add_state_to_heap_and_mark_visited(v, path)

        return False

    def find_shortest_path(self):
        """
        Determine the shortest path.
        :return: a list of PuzzleState objects, including the initial state that describe the path
        """
        done = False
        index = 0
        while not done:
            done = self.step((index%1000)==0)
            index += 1

        return self.best_path


def day22b_solver(nodes):
    initial_state = PuzzleState(nodes)
    print("\n".join(initial_state.visualise()))

    sbs = SlidingBlockSolver(initial_state)
    best_path = sbs.find_shortest_path()
    return len(best_path) - 1       # exclude the initial state since we want number of moves


if __name__ == '__main__':
    with(open('input_22a.txt', 'r')) as infile:
        node_lines = infile.read().splitlines()[2:]     # skip the first two lines since they're preamble!
    nodes = [parse_df_input_line(l) for l in node_lines]

    print(day22a_solver(nodes))

    print("Is this a sliding block puzzle?", are_all_nodes_full_or_interchangable(nodes))
    print(day22b_solver(nodes))

