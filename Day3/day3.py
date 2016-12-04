#
# solution for the 3rd puzzle of Advent of Code: http://adventofcode.com/2016/day/3
#

import numpy as np

def checkvalid(triangle):
    return triangle[0] + triangle[1] > triangle[2] and \
           triangle[0] + triangle[2] > triangle[1] and \
           triangle[1] + triangle[2] > triangle[0]

def partA(translate_triangles=None):
    # answer for part a
    with(open('input_3a.txt', 'r')) as infile:
        triangle_lines = infile.read().splitlines()
    triangles = [[int(y) for y in x.split()] for x in triangle_lines]

    if translate_triangles:
        triangles = translate_triangles(triangles)

    valid_triangles = list(filter(checkvalid,triangles))
    print(len(valid_triangles))

def partB():
    def translate(triangles):
        # translate blocks of triangles so that:
        #'    4   21  894'
        #'  419  794  987'
        #'  424  797  125'
        # becomes
        #'    4  419  424'
        #'   21  794  797'
        #'  894  987  125'
        # we've already parsed them into arrays of integers, so just take a 3x3 block and transpose it

        translated_triangles = []

        for source in [ triangles[x:x+3] for x in range(0,len(triangles), 3)]:
            # get the source 3x3 into a numpy array
            source_matrix = np.array(source)

            # transpose...
            transposeded = source_matrix.transpose()

            for i in range(3):
                translated_triangles.append(list(transposeded[i,:]))

        return translated_triangles

    partA(translate)


if __name__ == '__main__':
    partA()
    partB()
