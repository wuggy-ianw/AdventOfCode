import hashlib
import heapq
import copy

class Day17PathFinder(object):
    # direction -> (hash_char_to_check, delta_x, delta_y)
    direction_deltas = {'U': (0, 0, -1),
                        'D': (1, 0, 1),
                        'L': (2, -1, 0),
                        'R': (3, 1, 0)}

    def path_search_metric_astar_manhatten(self, pos, path_len):
        return path_len + sum([abs(a - b) for a, b in zip(pos, self.dest_pos)])

    def path_search_metric_dijkstra(self, pos, path_len):
        return path_len

    def __init__(self, passcode, metric = 'A*-manhatten'):
        metrics = {'A*-manhatten': self.path_search_metric_astar_manhatten,
                   'dijkstra': self.path_search_metric_dijkstra}
        self.metric = metrics[metric]

        self.passcode = passcode
        self.dest_pos = (3,3)
        self.width = 4
        self.height = 4

        self.search_heap = []       # empty heaps are already heaps
        self.tie_breaker_index = 0

        pos = (0, 0)
        self.add_position_to_heap(pos)

    def add_position_to_heap(self, pos, path=None):
        # if we've no path to this point, then use an empty path string
        if not path:
            path = ''

        # compute the metric
        metric = self.metric(pos, len(path))

        # push a tuple to the heap of all this, ordered by metric then tie_breaker
        heapq.heappush(self.search_heap, (metric, self.tie_breaker_index, pos, path))

        self.tie_breaker_index += 1

    def step(self):
        # take the 'best' item from the heap
        metric, tie_breaker, pos, path = heapq.heappop(self.search_heap)

        # if we've reached the destination position
        if pos == self.dest_pos:
            self.bestpath = path
            return True

        # get all the visitable positions and push them on the heap
        possible_moves = self.moves_from_pos(pos, path)
        for move_pos, move_path in possible_moves:
            self.add_position_to_heap(move_pos, move_path)

        return False

    def moves_from_pos(self, pos, path):
        """
        Computes the possible moves from this position reached by a given path

        :param pos: a tuple(x,y) of the current position
        :param path: a string of characters 'UDLR' describing the path taken until now
        :return: a list of tuples (pos, path) for all reachable positions, where the pos has
                    been updated and path has been extended by the movable direction
        """
        reachable_positions_and_paths = []

        x, y = pos

        tohash = self.passcode + path
        hash = hashlib.md5(tohash.encode('ascii')).hexdigest().lower()

        for step_dir, t in self.direction_deltas.items():
            # unpack the tuple
            hash_index, dx, dy = t

            # get the candidate position and path
            candidate_pos = (x + dx, y + dy)
            candidate_path = path + step_dir

            # a position is reachable iff
            #   it's candidate position is within the bounds of the puzzle map area
            #   the character at hash_index in the hash is one of 'bcdef'
            cx, cy = candidate_pos
            if cx >= 0 and cy >= 0 and cx < self.width and cy < self.height and hash[hash_index] in 'bcdef':
                reachable_positions_and_paths.append((candidate_pos, candidate_path))

        return reachable_positions_and_paths

    def find_shortest_path(self):
        done = False
        while not done:
            done = self.step()

        return self.bestpath

    def find_longest_path(self):
        # find the shortest path over and over again, until we exhaust all the possible paths
        longest_path = None
        try:
            while True:
                longest_path = self.find_shortest_path()
        except IndexError:
            # ignore this, it's our end condition!
            pass

        return longest_path

def day17a_solver():
    pf = Day17PathFinder('awrkjxxr')
    sp = pf.find_shortest_path()
    print(sp)

def day17b_solver():
    pf = Day17PathFinder('awrkjxxr')
    sp = pf.find_longest_path()
    print(len(sp))

if __name__ == '__main__':
    day17a_solver()
    day17b_solver()
