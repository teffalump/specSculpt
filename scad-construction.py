#!/usr/bin/python3
#Generate vertices of solid

def BEZ03(u):
    return pow((1-u), 3);
def BEZ13(u):
    return 3*u*(pow((1-u),2));
def BEZ23(u):
    return 3*(pow(u,2))*(1-u);
def BEZ33(u):
    return pow(u,3);

def pointAlongBez4(p0, p1, p2, p3, u):
    return [
            BEZ03(u)*p0[0]+BEZ13(u)*p1[0]+BEZ23(u)*p2[0]+BEZ33(u)*p3[0],
            BEZ03(u)*p0[1]+BEZ13(u)*p1[1]+BEZ23(u)*p2[1]+BEZ33(u)*p3[1]
            ]

def random_data(length = 1000, width = 50):
    from random import randrange as pick
    return [[pick(0,255) for j in range(width)] for i in range(length)]

def offsets_to_points(points, offsets):
    d1 = abs(points[0][0] - points[1][0]) 
    d2 = abs(points[0][1] - points[1][1])
    #x-coord 
    if points[0][0] <= points[1][0]:
        cp1x = offsets[0][0] * d1 + points[0][0] 
        cp2x = offsets[1][0] * d1 + points[0][0] 
    else:
        cp1x = points[0][0] - offsets[0][0] * d1
        cp2x = points[0][0] - offsets[1][0] * d1

    #y-coord
    if points[0][1] < points[1][1]:
        cp1y = offsets[0][1] * d2 + points[0][1] 
        cp2y = offsets[1][1] * d2 + points[0][1] 
    else:
        cp1y = points[0][1] - offsets[0][1] * d2
        cp2y = points[0][1] - offsets[1][1] * d2
    return [[cp1x, cp1y],[cp2x, cp2y]]
        
def bezierSplinePoints(points, steps=100, offsets=[[.8, 0], [.2, 1]]):
    #points = cubic bezier spline must go through these
    #steps = number of steps per bez line
    #offsets = control point offsets relative to the diff between p0 and p3
    #that is, [.5, .5] would mean p1 would be halfway between p0[0] and p3[0], and halfway between p0[1] and p3[1]

    #return points to fill in the full line (excluding original points)
    for p in range(len(points) - 1):
        c_points=offsets_to_points([points[p], points[p+1]], offsets)
        for step in range(1,steps):
            yield pointAlongBez4(points[p], c_points[0], c_points[1], points[p+1], step/steps)

from random import randrange as pick
print(len(list(bezierSplinePoints([[j, pick(1,255)] for j in range(10000)]))))
