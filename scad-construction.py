#!/usr/bin/python3
#Generate vertices of solid
import numpy as np
from bezier_functions import *

def random_data(length = 1000, width = 50):
    from random import randrange as pick
    return [[pick(0,255) for j in range(width)] for i in range(length)]

from sys import exit
test_data=random_data(2,3)
steps=10

with open('/home/cz/Programming/specSculpt/test.scad', 'w') as out:
    out.write("polyhedron ( points = [")
    from pprint import pprint
    for sl in range(len(test_data) - 1):
        v_vert = []
        h = []
        for i,c in enumerate(test_data[sl]):
            print("calculating c_points")
            c_points = offsets_to_points([[0,c], [1,test_data[sl+1][i]]])
            print("getting vertical vertices")
            v_points = [pointAlongBez4([0,c], c_points[0], c_points[1], [1,test_data[sl+1][i]], j/steps) for j in range(steps+1)]
            print("done getting v vertices")

            # index is x-value
            v_vert.append([np.insert(x, 0, i) for x in v_points])

        #the vertical slice are now in (x,y,z) coordinates...i think
        v = np.around(v_vert,2)
        pprint(v)
        print("getting slice vertices")
        for t in range(steps+1):

            #these are all the transverse slices
            #same y-value, so need:
            #    slice horizontally through the vertical vertices
            #    slice 0 and 2 index for each vertice point (i.e., only x and z, since all same y-value)
            #    push that to bezierSplinePoints function
            #    reinsert y-value along vert axis

            h.append(np.insert(list(bezierSplinePoints(np.squeeze(v[...][:,t,0:3:2]))), 1, v[0][t][1], axis=1).tolist())
            print("done with a slice")

        #generator to generate triangle->indices mapping, still work in progress
        gen = ([[(hort_l * i + j, (hort_l * (i+1) + j), (hort_l * i + j + 1)], [(hort_l * (i+1) + j), (hort_l * (i+1) + j +1), (hort_l * i + j + 1)]] for i in range(vert_l - 1) for j in range(hort_l))

        pprint(np.array(h))
        for s in np.array(h):
            for point in s:
                out.write("[")
                point.tofile(out,",")
                out.write("],\n")
    out.write("[]]);")

        
#v_vert now has all vertical vertices (x,y,z)...hopefully
#this is only for flat one, though
#for i,c in enumerate(v_vert):
    #if i % 50 == 0: pprint(c)
#print(len(v_vert))
