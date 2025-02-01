import cv2
import numpy as np

# Need to take color input from the color script and then filter out the contours -> Try it with red and check

cap = cv2.VideoCapture(0)

while(True):
    ret, frame = cap.read()
    if not ret or frame is None:
        print("Failed to capture frame!!")
        break
    
    cv2.imshow("Initial Frame", frame)

    #Convert the frame to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    #Applying Canny Edge to the image
    thresh1 = 50
    thresh2 = 150
    canny = cv2.Canny(gray, thresh1, thresh2)

    #Detect the contours
    contours, hierarchies = cv2.findContours(canny, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    #Now define an area_threshold for contour filtering
    area_threshold = 500

    #Filter the contours using an array??
    filtered_contours = []

    for cnt in contours:
        if cv2.contourArea(cnt) > area_threshold:
            filtered_contours.append(cnt)
        else:
            pass

    # I will create and mask and filter out dawgg
    mask = cv2.bitwise_not(cv2.inRange(gray, 0, 255))      #This shit initialises a empty mask
    cv2.drawContours(mask, filtered_contours, -1, 255, -1)

    #Apply the mask 
    result = cv2.bitwise_and(frame, frame, mask=mask)

    # Show the results
    cv2.imshow('Filtered Contours', frame)
    cv2.imshow('Masked Result', result)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()