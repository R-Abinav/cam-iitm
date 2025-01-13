import cv2
from util import get_limits
from PIL import Image

blue = [156,86,0] #Blue in BGR color space
yellow = [0,255,255]
green = [0,204,0]

video_path = "/Users/R.Abinav/Desktop/CV/AUV/images/IMG_9940.MOV"

cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()

    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    lower, upper = get_limits(yellow)

    mask = cv2.inRange(hsv, lower, upper)

    mask_ = Image.fromarray(mask) #Converting our image from a numpy array (Which is OpenCV representation for our image) to a Pillow representation

    boundingBox = mask_.getbbox()

    #print(boundingBox)
    if boundingBox is not None:
        x1, y1, x2, y2 = boundingBox
        frame = cv2.rectangle(frame, (x1,y1), (x2,y2), (0,255,0), 5)

        #For centroid
        cen_x = int((x1+x2)/2)
        cen_y = int((y1+y2)/2)

        #Draw the centroid
        frame = cv2.circle(frame, (cen_x, cen_y), 5, (0,255,0), -1)

    #cv2.imshow('frame',mask)
    cv2.imshow('frame', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()