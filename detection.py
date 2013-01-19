import cv2
from math import pi
from math import sqrt

imagefiles = ["//home/bernease/Downloads/IMG_4364.jpg","//home/bernease/Downloads/IMG_4363.jpg",
"//home/bernease/Downloads/IMG_4338.JPG","//home/bernease/Downloads/IMG_4315.JPG"]

for imagefile in imagefiles:
    img = cv2.imread(imagefile)
    imgcopy=img
    #img = cv2.transpose(img)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    h,w = img.shape[:2]
    blur = cv2.GaussianBlur(gray, (9,9), 1)
    #blur = cv2.GaussianBlur(blur, (9,9), 1.4)

    edges = cv2.Canny(blur, 0.4*255, 0.4*0.4*255, imgcopy, 3)
  
    lines = cv2.HoughLinesP(edges, 1, pi/720, 150, None, min(h,w)/10, min(h,w)/50);

    for line in lines[0]:
        # Find points
        pt1 = (line[0],line[1])
        pt2 = (line[2],line[3])
        # Find slope
        if line[2] == line[0]:
            pt1x = (line[0],0)
            pt2x = (line[0],h)
        else:
            m = float(line[3] - line[1]) / float(line[2] - line[0])
            # Solve for b, far left
            b = int(line[1] - m*line[0])
            # Solve for y, far right
            y = int(m*w + b)
            # Find points
            pt1x = (0,b)
            pt2x = (w,y)

        # Draw lines
        #cv2.line(img, pt1x, pt2x, (0,0,127), 3)
        cv2.line(img, pt1, pt2, (0,0,255), 3)

    # Write image (with lines) and edges to jpg    cvtColor( dst, color_dst, CV_GRAY2BGR );

    outfile = imagefile[:-4] + "lines.jpg"
    outfileedge = imagefile[:-4] + "edges.jpg"
    cv2.imwrite(outfile, img)
    cv2.imwrite(outfileedge, edges)

    #mser = cv2.MSER()
    #regions = mser.detect(gray,None)
    #maxr = 0
    #for region in regions:
    #    lenr = float(len(region))
    #    if lenr > maxr:
    #        maxr = lenr/(h*w)

    #print maxr