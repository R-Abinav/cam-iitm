import cv2
import numpy as np

img = cv2.imread('/Users/R.Abinav/Desktop/CV/AUV/images/custom_gate.jpeg')
cv2.imshow('Image',img)

gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
#cv2.imshow('Gray', gray)

canny = cv2.Canny(gray, 50, 200)
#cv2.imshow('Canny', canny)

lines = cv2.HoughLines(canny, 1, np.pi/180, 180, np.array([]))

if lines is not None:
    for line in lines:
        rho, theta = line[0]
        a = np.cos(theta)
        b = np.sin(theta)

        x0 = a*rho
        y0 = b*rho

        x1 = int(x0+1000*(-b))
        y1 = int(y0+1000*(a))
        x2 = int(x0-1000*(-b))
        y2 = int(y0-1000*(1))
        cv2.line(img, (x1,y1), (x2,y2), (0,255,0), 5)
    
cv2.imshow("Lines", img)
cv2.imshow('Canny', canny)

cv2.waitKey(0)

