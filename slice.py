#!/usr/bin/python
#Generate a single slice

import math

#zero line - radius of circle from which amplitudes will be added
radius = 20

#multiplier so ring doesn't look crazy out of shape
multiplier = min(width, height) / 400

#bezier width
bezier_width = radius * .07

#angle diff between each amplitude
angle_diff = math.pi*2/len(data)

half_pi = math.pi / 2
for order, amp in enumerate(j):
    #calculate angle for each freq
    angle = angle_diff * order + half_pi

    #amplitude
    newAmp = j[order] * multiplier

    #limit max_move
#    try:
#        if abs(prevPoints[order-1]["amp"] - newAmp) > max_move:
#            newAmp = prevPoints[order]["amp"] - max_move
#    except (IndexError):
#        pass
#
    #set x and y coords
    x = half_w + math.cos(angle) * (radius + newAmp)
    y = half_h + math.sin(angle) * (radius + newAmp)

    prevPoints.append({"x": x, "y": y, "amp": newAmp})

    if (order == len(j) - 1):
        prevAngle = angle
        angle = half_pi
        cp1x = x + math.cos(prevAngle + half_pi) * bezier_width
        cp1y = y + math.sin(prevAngle + half_pi) * bezier_width
        cp2x = prevPoints[0]["x"] + math.cos(angle - half_pi) * bezier_width
        cp2y = prevPoints[0]["y"] + math.sin(angle - half_pi) * bezier_width

    else:
        prevAngle = angle_diff * (order - 1) + half_pi
        cp1x = prevPoints[order - 1]["x"] + math.cos(prevAngle + half_pi) * bezier_width
        cp1y = prevPoints[order - 1]["y"] + math.sin(prevAngle + half_pi) * bezier_width
        cp2x = x + math.cos(angle - half_pi) * bezier_width
        cp2y = y + math.sin(angle - half_pi) * bezier_width

#
