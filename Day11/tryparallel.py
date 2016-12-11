from day11 import *
import multiprocessing
import itertools

# messy experiment - parallelising the move generation

# I've submitted this into github just for reference. In practice, this is slower than the simple batch BFS.
# In other languages than python (or in an environment without the GIL), the overheads of moving the sets
# around may be low enough/eliminated.

def pool_set_global(history):
    global g_history
    g_history = history

def pool_call_move_items_by_elevator(state):
    global g_history
    return move_items_by_elevator(state, g_history)


def find_shortest_move_sequence_endstate_parallel(startstate, checkpointlog = True, parallel = True):
    active_states = frozenset([startstate])
    history = set([startstate])

    depth = 0
    while True:
        assert len(active_states)>0

        if checkpointlog:
            print('nactive=' + str(len(active_states)) + ' depth=' + str(depth))

        # get all the new states we can reach from this state
        if parallel:
            pool = multiprocessing.Pool(processes=8, initializer=pool_set_global, initargs=(history,))
            new_states_for_moves = pool.imap_unordered(pool_call_move_items_by_elevator, active_states, chunksize=10000)
            pool.close()
            pool.join()
            del pool
        else:
            pool_set_global(history)
            new_states_for_moves = map(pool_call_move_items_by_elevator, active_states)

        # next batch of active_states is the new set of states
        active_states = frozenset(itertools.chain.from_iterable(new_states_for_moves))
        history.update(active_states)

        # if any of the new states are the end state, then we're done
        for ns in active_states:
            if is_end_state(ns):
                return ns

        depth += 1

if __name__ == '__main__':
    print(day11a_solver(corefunc = find_shortest_move_sequence_endstate_parallel))
    print(day11b_solver(corefunc = find_shortest_move_sequence_endstate_parallel))
