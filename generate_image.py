#!/usr/bin/python

''' 
    Generate the images, hopefully stitch them together into video
    Mostly, this is bezier curve code (hopefully)
'''
import time,cairo, math, cStringIO, sys
output = cStringIO.StringIO()
width = 500
half_w = width / 2
height = 500
half_h = height / 2
svg = False
if svg:
    surface = cairo.SVGSurface(None, width, height)
else:
    #8-bit shit
    surface = cairo.ImageSurface(cairo.FORMAT_RGB24, width, height)
cxt = cairo.Context(surface)

#radius is radius (in points) of circle from which amplitudes will be added
radius = 100

#multiplier so ring doesn't look crazy out of shape
multiplier = min(width, height) / 400

#bezier width
bezier_width = radius * .07

#max movement
max_move = .6

#say the amp data is in data --- right now just test data
from random import randint
data = [[randint(1,60) for x in range(50)] for i in range(50)] 


#angle diff between each amplitude
angle_diff = math.pi*2/len(data)

half_pi = math.pi / 2
prevPoints=[]
for f,j in enumerate(data):
    cxt.set_source_rgb(0.,0.,0.)
    cxt.paint()
    cxt.set_source_rgb(1.,1.,1.)
    for order, amp in enumerate(j):
        #print cxt.get_current_point()

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
        #print (x,y)
        if (order == 0):
            cxt.move_to(x,y)

        else:
           prevAngle = angle_diff * (order - 1) + half_pi
           cp1x = prevPoints[order - 1]["x"] + math.cos(prevAngle + half_pi) * bezier_width
           cp1y = prevPoints[order - 1]["y"] + math.sin(prevAngle + half_pi) * bezier_width
           cp2x = x + math.cos(angle - half_pi) * bezier_width
           cp2y = y + math.sin(angle - half_pi) * bezier_width
           #cxt.curve_to(cp1x, cp1y, cp2x, cp2y, x, y);

        if (order == len(j) - 1):
            prevAngle = angle
            angle = half_pi
            cp1x = x + math.cos(prevAngle + half_pi) * bezier_width
            cp1y = y + math.sin(prevAngle + half_pi) * bezier_width
            cp2x = prevPoints[0]["x"] + math.cos(angle - half_pi) * bezier_width
            cp2y = prevPoints[0]["y"] + math.sin(angle - half_pi) * bezier_width
            cxt.curve_to(cp1x, cp1y, cp2x, cp2y, prevPoints[0]["x"], prevPoints[0]["y"])

        #print prevPoints
    #surface.create_for_data(output, cairo.FORMAT_RGB24, width, height)
    cxt.fill()
    surface.write_to_png(sys.stdout)
    #try:
    #    surface.write_to_png(sys.stdout)
    #    #sys.stdout.write(output)
    #    #im = Image.open(StringIO.StringIO(buf))
    #    #print im.format, im.size, im.mode
    #    #im.save(sys.stdout, "JPEG")
    #except IOError, e:
    #    print "eww", e
    ##print "buffer", output
    #time.sleep(2)
    #sys.exit(0)
    #name = str(f) + ".png"
    #surface.write_to_png("/home/cz/Programming/specSculpt/" + name)
    #cxt.save()
#for i in range(49,-1,-1):
#    cxt.restore()
#    surface.write_to_png(output)
#surface.finish()
#with open("/home/cz/Programming/specSculpt/buffer_dump.svg", "w") as f:
#    f.write(output.getvalue())
