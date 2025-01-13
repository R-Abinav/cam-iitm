import cv2
from util import get_limits
from PIL import Image

blue = [156,86,0] #Blue in BGR color space
yellow = [0,255,255]
green = [0,204,0]
red = [102,102,255] #BGR

img_path = "/Users/R.Abinav/Desktop/CV/AUV/images/yaw_2.jpeg"

img = cv2.imread(img_path)
#cv2.imshow('initial image', img)

hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

lower, upper = get_limits(yellow)

mask = cv2.inRange(hsv, lower, upper)

mask_ = Image.fromarray(mask) #Converting our image from a numpy array (Which is OpenCV representation for our image) to a Pillow representation

boundingBox = mask_.getbbox()

#print(boundingBox)
if boundingBox is not None:
    x1, y1, x2, y2 = boundingBox
    img = cv2.rectangle(img, (x1,y1), (x2,y2), (0,255,0), 5)

    #For centroid
    cen_x = int((x1+x2)/2)
    cen_y = int((y1+y2)/2)

    #Draw the centroid
    img = cv2.circle(img, (cen_x, cen_y), 5, (0,255,0), -1)

    #cv2.imshow('frame',mask)
    cv2.imshow('frame', img)

cv2.waitKey(0)