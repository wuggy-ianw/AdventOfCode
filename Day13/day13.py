import heapq
import copy

class Day13PathFinder:
    direction_deltas = [(-1, 0),
                        (1, 0),
                        (0, -1),
                        (0, 1)]

    def path_search_metric_astar_manhatten(self, pos, path_len):
        return path_len + sum([abs(a - b) for a, b in zip(pos, self.dest_pos)])

    def path_search_metric_dijkstra(self, pos, path_len):
        return path_len     # dijkstra


    def __init__(self, favourite_number, dest_pos, metric = 'A*-manhatten'):
        metrics = {'A*-manhatten': self.path_search_metric_astar_manhatten,
                   'dijkstra': self.path_search_metric_dijkstra}
        self.metric = metrics[metric]

        self.favourite_number = favourite_number
        self.dest_pos = dest_pos

        self.visited = set()
        self.search_heap = []       # empty heaps are already heaps
        self.tie_breaker_index = 0

        pos = (1,1)
        self.add_position_to_heap_and_mark_visited(pos)

        self.bestpath = None


    def is_position_reachable(self, pos):

        # if it's -ive then it's not reachable
        x, y = pos
        if x < 0 or y < 0:
            return False

        #You can determine whether a given x,y coordinate will be a wall or an open space using a simple system:
        #Find x*x + 3*x + 2*x*y + y + y*y.
        v = x*x + 3*x + 2*x*y + y + y*y

        #Add the office designer's favorite number (your puzzle input).
        v += self.favourite_number

        #Find the binary representation of that sum; count the number of bits that are 1.
        #    If the number of bits that are 1 is even, it's an open space.
        #    If the number of bits that are 1 is odd, it's a wall.
        nbits = bin(v).count('1')

        return (nbits % 2) == 0


    def is_position_reachable_and_unvisited(self, pos):
        # if we've already visited, then don't visit it again
        if pos in self.visited:
            return False

        return self.is_position_reachable(pos)


    def moves_from_pos(self, pos):
        reachable_positions = []

        x, y = pos
        for dx, dy in self.direction_deltas:
            candidate_pos = (x + dx, y + dy)
            if self.is_position_reachable_and_unvisited(candidate_pos):
                reachable_positions.append(candidate_pos)

        return reachable_positions


    def add_position_to_heap_and_mark_visited(self, pos, path=None):
        # visit this position
        self.visited.add(pos)

        # extend the path we've walked to include this pos
        if path:
            path = copy.copy(path)
        else:
            path = []
        path.append(pos)

        # compute the metric
        metric = self.metric(pos, len(path))

        # push a tuple to the heap of all this, ordered by metric then tie_breaker
        heapq.heappush(self.search_heap, (metric, self.tie_breaker_index, pos, path))

        self.tie_breaker_index += 1


    def step(self, until = None):
        # take the 'best' item from the heap
        metric, tie_breaker, pos, path = heapq.heappop(self.search_heap)

        # if this step has reached the optional end-condition, end
        if until and until(metric, tie_breaker, pos, path):
            return True

        # if we've reached the destination position
        if pos == self.dest_pos:
            self.bestpath = path
            return True

        # get all the visitable positions and push them on the heap
        for v in self.moves_from_pos(pos):
            self.add_position_to_heap_and_mark_visited(v, path)

        return False


    def find_shortest_path(self):
        done = False
        while not done:
            done = self.step()

        return self.bestpath

    def maze_character(self, x, y, path):
        pos = (x,y)
        if path and pos in path:
            return 'O'

        if self.is_position_reachable(pos):
            return '.'
        else:
            return '#'

    def visualise_maze(self, width, height, path = None):
        visualisation = []
        visualisation.append('  ' + "".join([str(i%10) for i in range(width)]))

        for y in range(height):
            visualisation.append(str(y%10) + ' ' + "".join([self.maze_character(x,y, path) for x in range(width)]))

        return visualisation


def day13a_solver():
    df = Day13PathFinder(1358, (31,39))
    path = df.find_shortest_path()

    width = 2 + max(x for x,y in path)
    height = 2 + max(y for x,y in path)

    for l in df.visualise_maze(width, height, path):
        print(l)

    print()
    print(len(path) - 1)  # -1 to exclude the starting position in the path


def day13b_solver():
    def until(metric, tie_breaker, pos, path):
        return len(path)==51        # 50 steps is 51 positions

    df = Day13PathFinder(1358, (31,39), metric='dijkstra')

    done = False
    while not done:
        done = df.step(until)

    width = 2 + max(x for x,y in df.visited)
    height = 2 + max(y for x,y in df.visited)

    for l in df.visualise_maze(width, height, df.visited):
        print(l)

    print()
    print(len(df.visited))  # include the initial position

if __name__ == '__main__':
    day13a_solver()
    day13b_solver()
