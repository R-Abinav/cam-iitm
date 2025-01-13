import cv2
import numpy as np

#Function to get the right interval in hue
def get_limits(color):
    if len(color) != 3:
        raise ValueError("Input color must be a BGR triplet with 3 elements.")
    
    c = np.uint8([[color]]) #here insert the bgr values which you want to convert to hsv
    hsvC = cv2.cvtColor(c, cv2.COLOR_BGR2HSV)

    lowerLimit = (hsvC[0][0][0] - 10, 100, 100)
    upperLimit = (hsvC[0][0][0] + 10, 255, 255)

    lowerLimit = np.array(lowerLimit, dtype='uint8')
    upperLimit = np.array(upperLimit, dtype='uint8')

    return lowerLimit, upperLimit

