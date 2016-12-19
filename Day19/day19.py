def day19a_shuffle_presents(num_elves):
    """
    For a given number of elves, shuffle presents until there's only one elf with presents.

    :param num_elves: starting number of elves
    :return: index (from 1) of the initial elves who now has all the presents
    """
    # For part a, there's a clear pattern:
    #   arrays of length n*2 produce an array of length n with the same odd elements
    #   arrays of length (n*2)+1 produce an array of length n where the first element increases
    #      the amount of increase depends on our current level (i.e. each time we eliminate half the items, the 'step'
    #      to the next item doubles).
    first_elf = 1
    level = 2
    while num_elves!=1:
        if (num_elves%2) == 0:
            num_elves = int(num_elves/2)
        else:
            num_elves = int(num_elves/2)
            first_elf += level

        level *= 2

    return first_elf

def day19b_shuffle_presents_slow_one_level(elves):
    """
    Given a circle of elves, shuffle presents until all the elves have shuffled presents. This version
    runs using simulation with noddy data structures, so it's rather slow.

    :param elves: a list of integers, holding elf 'indices'
    :return: a new list of integers holding elf 'indices' for elves still with presents
    """
    # used in tests to check the pattern extraction
    i = 0
    while True:
        delindex = (i + int(len(elves)/2))%len(elves)

        if delindex>i:
            # if we're deleting something after this index, move forward in the list
            i += 1
        else:
            # otherwise, by deleting an earlier 'elf' from the circle, we move all the other elves down one index
            pass

        del elves[delindex]
        if i>=len(elves):
            break

    return elves

def day19b_shuffle_presents_one_level(elves):
    """
    Given a circle of elves, shuffle presents until all the elves have shuffled presents. This version
    runs using some optimisations!

    :param elves: a list of integers, holding elf 'indices'
    :return: a new list of integers holding elf 'indices' for elves still with presents
    """
    mod = len(elves)%3
    if mod==0:
        # there is a pattern for n*3 sized arrays, they seem to take only each 3rd element
        # i.e. 1..9 -> 3,6,9
        elves = elves[2::3]
    elif mod==1:
        # there is a pattern for (n*3)+1 sized arrays
        # it seems to be: split the list into two k and k+1 element lists
        #   split the first list into k-1 and it's last element
        #   take every 3rd element from the truncated first list
        #   then take the last item in the first list
        #   then take every 3rd item from the k+1 element list, but ending with the 3rd element from the end
        # example:
        #   1,2,3,4,5,6,7,8,9,10 gets split into two lists...
        #   1,2,3,4,5 ,6,7,8,9,10 and we take the 3rd elements and the last element from the first list...
        #  [1,4,5] 6,7,8,9,10 and then we take every 3rd element ENDING at the 3rd element from the end
        #  [1,4,5,8]
        k = int(len(elves)/2)
        elves = elves[0:k-1:3] + [elves[k-1]] + list(reversed(list(reversed(elves[k:]))[2::3]))
    else:
        # there is a pattern for (n*3)+2 sized arrays
        # it seems to be: split the list into three parts: a list of k elements, the middle elements (1 or 2), and a second list of k elements
        #   take every 3rd element from the first list, starting from the 2nd element
        #   if the middle list is of length 2, take the first element of it
        #   then take every 3rd item from the second list, but ending with the 2nd element from the end
        # example:
        #   1,2,3,4,5,6,7,8,9,10,11 gets split into parts
        #   1,2,3,4,5  6  7,8,9,10,11 and we take the 3rd elements from the first list...
        #  [2,5]  6   7,8,9,10,11 and then we take every 3rd element ENDING at the 2nd element from the end
        #  [2,5,7,10]
        # example 2:
        #   1,2,3,4,5,6,7,8,9,10,11,12,13,14 gets split into parts
        #   1,2,3,4,5,6, 7,8  9,10,11,12,13,14 and we take the 3rd elements from the first list...
        #  [2,5]  7,8  9,10,11,12,13,14 and then we append the first element from the middle part (since it's len 2)
        #  [2,5,7]  9,10,11,12,13,14 and then we take every 3rd element ENDING at the 2nd element from the end
        #  [2,5,7,10,13]
        k = int(len(elves)/2)
        mlen = len(elves)-2*k
        if mlen==0:
            k -= 1
            mlen = 2
        a = elves[0:k]
        b = elves[-1:k:-1]
        middle = [] if mlen==1 else [elves[k]]

        elves = a[1::3] + middle + list(reversed(b[1::3]))

    return elves

def day19b_shuffle_presents(num_elves):
    """
    SFor a given number of elves, shuffle presents until there's only one elf with presents. This uses
    the b-solution part shuffling rules.

    :param num_elves: starting number of elves
    :return: index (from 1) of the initial elves who now has all the presents
    """
    elves = list(range(1,num_elves+1))
    while len(elves)!=1:
        elves = day19b_shuffle_presents_one_level(elves)

    return elves[0]

if __name__=='__main__':
    print(day19a_shuffle_presents(5))
    print(day19a_shuffle_presents(3018458))
    print()
    print(day19b_shuffle_presents(5))
    print(day19b_shuffle_presents(3018458))

