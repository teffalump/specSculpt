#!/usr/bin/python
#Generate a single slice

import math
from bezier_functions import *

class slice:

    def __init__(self, data, steps = 100, radius=20, outfile="out.scad"):
        #outfile
        self.outfile = outfile

        #amp data
        self.data = data
        self.l_data = len(data)

        #zero line - radius of circle from which amplitudes will be added
        self.radius = radius

        #multiplier so ring doesn't look crazy out of shape
        #self.multiplier = min(width, height) / 400
        self.multiplier = .5

        #bezier width
        self.bezier_width = radius * .07

        #angle diff between each amplitude
        self.angle_diff = math.pi*2/len(data)

        self.half_pi = math.pi / 2

        #number of points for each bez curve
        self.steps = steps

        self.h = 10


    def points(self):
        self.prevPoints = []
        for order, amp in enumerate(self.data):

            #calculate angle for each freq
            self.angle = self.angle_diff * order + self.half_pi

            #amplitude
            self.newAmp = self.data[order] * self.multiplier

            #limit max_move
        #    try:
        #        if abs(prevPoints[order-1]["amp"] - newAmp) > max_move:
        #            newAmp = prevPoints[order]["amp"] - max_move
        #    except (IndexError):
        #        pass
        #
            #set x and y coords
            self.x = math.cos(self.angle) * (self.radius + self.newAmp)
            self.y = math.sin(self.angle) * (self.radius + self.newAmp)

            self.prevPoints.append({"x": self.x, "y": self.y, "amp": self.newAmp})

            if (order == self.l_data - 1):
                self.prevAngle = self.angle
                self.angle = self.half_pi
                self.cp1x = self.x + math.cos(self.prevAngle + self.half_pi) * self.bezier_width
                self.cp1y = self.y + math.sin(self.prevAngle + self.half_pi) * self.bezier_width
                self.cp2x = self.prevPoints[0]["x"] + math.cos(self.angle - self.half_pi) * self.bezier_width
                self.cp2y = self.prevPoints[0]["y"] + math.sin(self.angle - self.half_pi) * self.bezier_width

            elif (order == 0):
                continue

            else:
                self.prevAngle = self.angle_diff * (order - 1) + self.half_pi
                self.cp1x = self.prevPoints[order - 1]["x"] + math.cos(self.prevAngle + self.half_pi) * self.bezier_width
                self.cp1y = self.prevPoints[order - 1]["y"] + math.sin(self.prevAngle + self.half_pi) * self.bezier_width
                self.cp2x = self.x + math.cos(self.angle - self.half_pi) * self.bezier_width
                self.cp2y = self.y + math.sin(self.angle - self.half_pi) * self.bezier_width

            for i in range(self.steps+1):
                print(pointAlongBez4([self.prevPoints[order-1]["x"],
                                        self.prevPoints[order-1]["y"]],
                                        [self.cp1x, self.cp1y],
                                        [self.cp2x, self.cp2y],
                                        [self.x, self.y],
                                        i/self.steps))

a = slice([0,0,0,0])
a.points()
