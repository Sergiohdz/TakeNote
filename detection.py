import cv2

imagefiles = ["//home/bernease/Downloads/IMG_4364.jpg","//home/bernease/Downloads/IMG_4363.jpg",
"//home/bernease/Downloads/IMG_4338.JPG","//home/bernease/Downloads/IMG_4334.JPG",
"//home/bernease/Downloads/IMG_4315.JPG"]

for imagefile in imagefiles:
    img = cv2.imread(imagefile)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    h,w = img.shape[:2]
    edges = cv2.Canny(gray, 80, 150)
    lines = cv2.HoughLinesP(edges, 1, math.pi/720, 1, None, min(h,w)/5, min(h,w)/80);

    for line in lines[0]:
        # Find points
        pt1 = (line[0],line[1])
        pt2 = (line[2],line[3])
        print "pt1:",line[0],",",line[1]
        print "pt2:",line[2],",",line[2]
        # Find slope
        m = float(line[3] - line[1]) / float(line[2] - line[0])
        print "m",m
        # Solve for b, far left
        b = int(line[1] - m*line[0])
        # Solve for y, far right
        y = int(m*w + b)
        # Find points
        pt1x = (0,b)
        pt2x = (w,y)
        print "pt1x:",0,",",b
        print "pt2x:",w,",",y
        # Draw lines
        cv2.line(img, pt1x, pt2x, (0,0,127), 3)
        cv2.line(img, pt1, pt2, (0,0,255), 3)
        print "---"

    # Write image (with lines) and edges to jpg
    outfile = imagefile[:-1*len(imagefile.split('.')[-1])]
    print outfile
    #cv2.imwrite("//home/bernease/Downloads/IMG_4342_outN.JPG", img)
    #cv2.imwrite("//home/bernease/Downloads/IMG_4342_cannyoutN.JPG", edges)