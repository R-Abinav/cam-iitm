import cv2
import numpy as np

cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()

    if not ret:
        print("Failed to grab frame!")
        break

    #cv2.imshow('Initial Frame', frame)

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    #cv2.imshow('Gray', gray)

    canny = cv2.Canny(gray, 50, 200)
    #cv2.imshow('Canny', canny)

    lines = cv2.HoughLines(canny, 1, np.pi/180, 160, np.array([]))

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

            cv2.line(frame, (x1,y1), (x2,y2), (0,255,0), 5)
    
    cv2.imshow("Lines", frame)
    cv2.imshow('Canny', canny)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
