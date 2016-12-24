import itertools
from copy import copy
import heapq

class Maze(object):
    """
    Class holding the maze data. Mazes are described as a list of strings (from top to bottom)
    containing the characters '#' for walls, '0' to '9' for points to visit (and zero the start
    position), and any other character meaning that block is accessible.
    """

    def __init__(self, maze_lines):
        """
        :param maze_lines: A list of strings, all the same length representing a maze
        """
        self.height = len(maze_lines)
        self.width = len(maze_lines[0])

        self.maze_lines = maze_lines.copy()
        for m in self.maze_lines:
            assert len(m) == self.width, "Maze line wasn't the same width as the first line?"

        self.path_points = self._find_path_points()

    def _find_path_points(self):
        """
        Find the marked path points, including the start position
        :return: a dictionary keyed by the INTEGER tag of the path point, with values
                 a tuple(x,y) of that tags position
        """
        # find all the 0-9 characters in the maze
        path_points = {}
        for y, m in enumerate(self.maze_lines):
            for x, c in enumerate(m):
                if str.isdigit(c):
                    path_points[int(c)] = (x, y)

        return path_points

    def is_wall_or_out_of_bounds(self, x, y):
        """
        Determine if we cannot enter a given x,y point
        :param x: ordinate
        :param y: ordinate
        :return: boolean
        """
        return x < 0 or x >= self.width or y < 0 or y >= self.height or \
                self.maze_lines[y][x] == '#'

class PuzzleState(object):
    """
    Hashable object for the puzzle state: the maze we're searching in, our current position
    and the remaining points to visit.
    """
    move_directions = ((0, 1), (0, -1), (1, 0), (-1, 0))

    def __init__(self, maze, pos=None, remaining_path_points=None):
        self.maze = maze

        # if we're not initialised with an explicit position, find the '0' position from the maze
        if pos:
            self.pos = pos
        else:
            self.pos = maze.path_points[0]

        # if we're not initialised with an explicit set of remaining points to visit,
        if remaining_path_points is not None:       # can't use a plain if... empty sets are 'false'!
            self.remaining_path_points = remaining_path_points
        else:
            self.remaining_path_points=frozenset(maze.path_points.values())

        # if our current position happens to be a path point, remove it!
        self.remaining_path_points = self.remaining_path_points.difference([self.pos])

    def moves_from_this_state(self, exclude):
        """
        Determine the states we can reach from this state.

        :param exclude: set of states that we should exclude from the moves list (i.e. because
                        we've already visited them)
        :return: a list of new states
        """
        x, y = self.pos
        moves = []

        # check all directions we can move in
        for delta_x, delta_y in self.move_directions:
            cx, cy = x + delta_x, y + delta_y
            if not self.maze.is_wall_or_out_of_bounds(cx, cy):
                # the candidate state is a move to a new position
                new_state = PuzzleState(self.maze, (cx, cy), self.remaining_path_points)

                # only keep this candidate state if we've not already visited it
                if new_state not in exclude:
                    moves.append(new_state)

        return moves

    ''' Hashability and equality for the puzzle state works by comparing that they
        share the same maze OBJECT, not a maze with the same 'content'. This is faster,
        since the maze is relatively big compared to the rest of the puzzle state, but
        means that PuzzleStates with copies of the same maze are NOT considered equal.
    '''
    def __eq__(self, other):
        return self.maze is other.maze and self.pos == other.pos and \
               self.remaining_path_points == other.remaining_path_points

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return hash((id(self.maze), self.pos, self.remaining_path_points))



def until_all_numbers_visited(state):
    # if we've visited all the positions, we're done
    return len(state.remaining_path_points) == 0

def until_all_numbers_visited_and_return_to_zero(state):
    # if we've visited all the positions and returned to our start point, we're done
    return until_all_numbers_visited(state) and \
           state.pos == state.maze.path_points[0]


class MultiTargetPathFinder(object):
    """
    Path finder for visiting multiple points in a maze.
    """

    def path_search_metric_dijkstra(self, state, path_len):
        # simple metric makes use behave like Dijkstra's shortest path algorithm
        return path_len

    def __init__(self, state, metric = 'dijkstra', until=until_all_numbers_visited):
        """

        :param state: PuzzleState object with the initial position and places to visit
        :param metric: Name of the metric to use. Default is a simple Dijkstra shortest-path metric.
        :param until: a callable f(state) which returns True if we've reached the end condition.
                      Default is to stop when all the path points have been reached.
        """
        metrics = {'dijkstra': self.path_search_metric_dijkstra}
        self.metric = metrics[metric]
        self.until = until

        self.visited = set()
        self.search_heap = []       # empty heaps are already heaps
        self.tie_breaker_index = 0

        self.add_state_to_heap_and_mark_visited(state)
        self.best_path = None

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
            print(metric, tie_breaker, state.pos, state.remaining_path_points, len(path), len(self.search_heap))

        # if we're done
        if self.until(state):
            self.best_path = path
            return True

        # get all the visitable positions and push them on the heap
        for v in state.moves_from_this_state(self.visited):
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
            done = self.step((index % 10000) == 0)
            index += 1

        return self.best_path


def day24a_solver(maze_lines):
    maze = Maze(maze_lines)
    initial_state = PuzzleState(maze)

    pf = MultiTargetPathFinder(initial_state)
    best_path = pf.find_shortest_path()
    return len(best_path) - 1  # exclude the initial state since we want number of moves


def day24b_solver(maze_lines):
    maze = Maze(maze_lines)
    initial_state = PuzzleState(maze)

    pf = MultiTargetPathFinder(initial_state, until=until_all_numbers_visited_and_return_to_zero)
    best_path = pf.find_shortest_path()
    return len(best_path) - 1  # exclude the initial state since we want number of moves



if __name__ == '__main__':
    with(open('input_24a.txt', 'r')) as infile:
        maze_lines = infile.read().splitlines()

    print(day24a_solver(maze_lines))
    print(day24b_solver(maze_lines))
