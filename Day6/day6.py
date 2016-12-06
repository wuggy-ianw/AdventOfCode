import collections
import operator

def day6a_solver(lines, character_selector=lambda ft: ft.most_common(1)[0][0]):
    # count the frequency of each character in every position of our input
    msglen = len(lines[0])
    freq_tables = [collections.Counter() for i in range(msglen)]

    for line in lines:
        assert(len(line) == msglen)
        for i,char in enumerate(line):
            freq_tables[i][char] += 1

    # the solution is selectors chosen character in each position
    solution = "".join([character_selector(freq_table) for freq_table in freq_tables])

    return solution

def day6b_solver(lines):
    # the solution is to choose the least frequent character
    def least_common(ft):
        smallest = min(ft.items(), key=operator.itemgetter(1))
        return smallest[0]

    return day6a_solver(lines, character_selector=least_common)

if __name__ == '__main__':
    with(open('input_6a.txt', 'r')) as infile:
        msglines = infile.read().splitlines()

    print(day6a_solver(msglines))
    print(day6b_solver(msglines))
