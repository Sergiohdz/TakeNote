import sys
import os
import cv2
import random
from math import pi, sqrt
from numpy import product, array
imagefiles = []

for arg in sys.argv:
    if arg != "detection.py":
        imagefiles.append(str(arg))

for imagefile in imagefiles:
    print type(imagefile)
    print imagefile
    # Read in image
    print os.path.isfile(imagefile)
    img = cv2.imread(imagefile)
    # Convert to gray
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # Find height and width
    h,w = img.shape[:2]
    # Apply Gaussian Blur
    blur = cv2.GaussianBlur(gray, (9,9), 1)
    # Apply Canny edge detection
    edges = cv2.Canny(blur, 0.4*255, 0.4*0.4*255, img, 3)
    # Apply Hough line detection
    lines = cv2.HoughLinesP(edges, 1, pi/720, 150, None, min(h,w)/8, min(h,w)/50);

    # For later use in shape detection
    newlines = []
    xyvalues = []
    thirdleft = w/3
    thirdright = w*2/3
    thirdup = h/3
    thirddown = h*2/3
    fifthleft = w/5
    fifthright = w*4/5
    fifthup = h/5
    fifthdown = h*4/5
    n = 40
    xvalues = random.sample(range(thirdleft,thirdright),n)
    yvalues = random.sample(range(thirdup,thirddown),n)
    xvaluesf = map(float,xvalues)
    yvaluesf = map(float,yvalues)

    for line in lines[0]:
        # Find points
        pt1 = (line[0],line[1])
        pt2 = (line[2],line[3])
        if line[2] == line[0]:
            pt1x = (line[0],0)
            pt2x = (line[0],h)
            m = float("Inf")
        else:
            # Find slope m
            m = float(line[3] - line[1]) / float(line[2] - line[0])
            # Solve for b, far left
            b = int(line[1] - m*line[0])
            # Solve for y, far right
            y = int(m*w + b)
            # Find points
            pt1x = (0,b)
            pt2x = (w,y)

        # Draw lines
        # cv2.line(img, pt1x, pt2x, (0,0,127), 3)  #extended
        cv2.line(img, pt1, pt2, (0,0,255), 3)   #actual

    #    contour = cv2.findContours(edges,cv2.RETR_CCOMP,cv2.CHAIN_APPROX_SIMPLE)
    #    while contour:
    #        bound_rect = cv2.boundingRect(array(contour))
    #        print cv2.contourArea(contour)
    #        contour = contour.h_next()

        # SHAPE DETECTION
        # Get rid of all lines fully in outside fifths
        if ( line[0]<fifthleft and line[2]<fifthleft ):
            pass
        elif ( line[0]>fifthright and line[2]>fifthright ):
            pass
        elif ( line[1]<fifthup and line[3]<fifthup ):
            pass
        elif ( line[1]>fifthdown and line[1]>fifthdown ):
            pass
        else:
            # Draw lines
            # cv2.line(img, pt1x, pt2x, (0,0,127), 3)  #extended
            cv2.line(img, pt1, pt2, (255,0,0), 3)   #actual

    for i in range(n):
        # Draw dots
        cv2.circle(img,(xvalues[i],yvalues[i]),5,(0,255,0),-1)

    # Write image (with line) and edges to jpg
    outfile = imagefile[:-4] + "_out.jpg"
    #outfileedge = imagefile[:-4] + "edges.jpg"
    cv2.imshow('Image',img)
    cv2.imwrite(outfile, img)
    #cv2.imwrite(outfileedge, edges)