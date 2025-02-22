import cv2
import numpy as np

#                 H    S    V
lower1 = np.array([0, 0, 150])
upper1 = np.array([180, 50, 255])

lower2 = np.array([0, 0, 150])
upper2 = np.array([180, 50, 255])

cap = cv2.VideoCapture(0)

#Lets apply some preprocessing -> For better underwater detection
#I am initializing clahe
clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8,8))

while True:
    ret, frame = cap.read()
    if not ret:
        print("Failed to capture frame!")
        break

    #Convert to LAB Color Space
    lab = cv2.cvtColor(frame, cv2.COLOR_BGR2LAB)
    
    #Apply the clahe to L channel
    l,a,b = cv2.split(lab)
    l_clahe = clahe.apply(l)

    #Merge back to BGR
    lab_clahe = cv2.merge((l_clahe, a, b))
    frame_clahe = cv2.cvtColor(lab_clahe, cv2.COLOR_LAB2BGR)

    hsv = cv2.cvtColor(frame_clahe, cv2.COLOR_BGR2HSV)

    mask1 = cv2.inRange(hsv, lower1, upper1)
    mask2 = cv2.inRange(hsv, lower2, upper2)

    _mask = cv2.bitwise_or(mask1, mask2)
    
    contours, hierarchy = cv2.findContours(_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    if len(contours) != 0:
        for contour in contours:
            if cv2.contourArea(contour) >= 500:
                x, y, w, h = cv2.boundingRect(contour)
                cv2.rectangle(frame, (x,y), (x+w, y+h), (0,0,255), 5)

    cv2.imshow("Mask", _mask)
    cv2.imshow('Webcam', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

