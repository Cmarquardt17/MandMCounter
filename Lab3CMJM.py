## Christian Marquardt, Justin McGowen
## CSCI442 Robot Vision
## February 29, 2019
##
## Overview: OpenCV Candy Counter calls in a picture of the instructors choosing of M&Ms
## then must draw all possible circles around the M&Ms's then fill them in based on their
## average color then if it is in between the parameters for each value them we want to add
## it to our varible and when we are done display onto the picture

import cv2 as cv2
import numpy as np

OGimg = cv2.imread("candyBigSmallerTiny.jpg", cv2.IMREAD_COLOR)

#function that brightens picture to be able to pick up the circles easier where edges will be a lot sharper
def brighten(img, value = 70):
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    h, s, v = cv2.split(hsv)
    
    limitVal = 255 - value
    v[v > limitVal] = 255
    v[v <= limitVal] += value
    
    final_hsv = cv2.merge((h, s, v))
    img = cv2.cvtColor(final_hsv, cv2.COLOR_HSV2BGR)
    return img

#brightens, blues, and detects edges of picture
OGimg = brighten(OGimg)
blurry = cv2.blur(OGimg, (5, 5), 0)
kernel = np.ones((5, 5), np.uint8)
edgey = cv2.Canny(blurry, 5, 150)


#Locates and draws each circle in the circle based on a build in Canny and radius parameters
circles = cv2.HoughCircles(edgey, cv2.HOUGH_GRADIENT, 1, 20, param1=50, param2=15, minRadius=10, maxRadius=20)
circles = np.uint16(np.around(circles))

#initializers
arrOfCircles = []
count = 0

#finds circles in the image before we want to go over them and color them in and to go through each one eventually
for i in circles[0, :]:
    currentImg = np.zeros((OGimg.shape[0], OGimg.shape[1]), np.uint8)
    cv2.circle(currentImg,(i[0], i[1]), i[2]-5, (255, 255, 255), -1)
    arrOfCircles.append(currentImg)


#All the counters we will use for each color and und will be for any we cannot decide on what color they are
b = 0
g = 0
y = 0
o = 0
br = 0
r = 0
und = 0

#for loop that checks the colors of each circle and then draws a new colored circle on the origImg
for img in arrOfCircles:
    rgb = cv2.mean(OGimg, mask = img)
    count += 1
    currentCircle = circles[0,count-1]
    
    
    #color blue
    if(int(rgb[0]) in range(215, 256) and int(rgb[1]) in range(155, 239) and int(rgb[2]) in range(0, 47)):
        b += 1
        cv2.circle(OGimg, (currentCircle[0], currentCircle[1]), currentCircle[2], (215, 159,47), -1)
    #color orange
    elif(int(rgb[0]) in range(25, 105) and int(rgb[1]) in range(100, 175) and int(rgb[2]) in range(240, 256)):
        o += 1
        cv2.circle(OGimg, (currentCircle[0], currentCircle[1]), currentCircle[2], (34, 111, 242), -1)
        
    #color green
    elif(int(rgb[0]) in range(75, 225) and int(rgb[1]) in range(90, 255) and int(rgb[2]) in range(0, 60)):
        g += 1
        cv2.circle(OGimg, (currentCircle[0], currentCircle[1]), currentCircle[2], (85, 172, 49), -1)
        
    #color yellow
    elif(int(rgb[0]) in range(0, 75) and int(rgb[1]) in range(205, 256) and int(rgb[2]) in range(230, 256)):
        y += 1
        cv2.circle(OGimg,(currentCircle[0], currentCircle[1]),int(currentCircle[2]),(0,255,255),-1)
        
    #color red
    elif(int(rgb[0]) in range(80, 170) and int(rgb[1]) in range(75, 150) and int(rgb[2]) in range(205, 256)):
        r += 1
        cv2.circle(OGimg, (currentCircle[0],currentCircle[1]), currentCircle[2],(0, 0, 255), -1)
        
    #color brown
    elif(int(rgb[0]) in range(90, 210) and int(rgb[1]) in range(95, 174) and int(rgb[2]) in range(100, 170)):
        br += 1
        cv2.circle(OGimg, (currentCircle[0], currentCircle[1]), currentCircle[2], (52, 58, 96), -1)
        
    #if it can't find a matching color, send to undetermined or in other words und
    else:
        und += 1

#These print out the number of m&ms and their color in the center of the picture that is being created
#Made th etext color black so they are easier to see in a heavily edited picture
font = cv2.FONT_HERSHEY_SIMPLEX
cv2.putText(OGimg,("Yellow: " + str(y)), (10, 300), font, 1, (0, 0, 0), 2, cv2.LINE_AA)
cv2.putText(OGimg,("Orange: " + str(o)), (10, 340), font, 1, (0, 0, 0), 2, cv2.LINE_AA)
cv2.putText(OGimg,("Brown: " + str(br)), (10, 380), font, 1, (0, 0, 0), 2, cv2.LINE_AA)
cv2.putText(OGimg,("Blue: " + str(b)), (10, 420), font, 1, (0, 0, 0), 2, cv2.LINE_AA)
cv2.putText(OGimg,("Green: " + str(g)), (10, 460), font, 1,(0,0,0),2,cv2.LINE_AA)
cv2.putText(OGimg,("Red: " + str(r)), (10, 500), font, 1, (0, 0, 0), 2, cv2.LINE_AA)


#shows image with new circles and printed out values
cv2.imshow("Count M&M's", OGimg)

cv2.waitKey(0)
cv2.destroyAllWindows()

