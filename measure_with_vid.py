import cv2
import numpy as np

vid_path = ''
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()

    #Convert to gray
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    #Canny edge
    canny = cv2.Canny(gray, 150, 175)

    #Contour Detection
    contours, heirarchies = cv2.findContours(canny, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    #print(len(contours))


    output_frame = frame.copy()
    for cnt in contours:
        #Draw the edges
        #cv2.polylines(output_frame, [cnt], isClosed=True, color=(0, 255, 0), thickness=5)

        #Get rect
        rect = cv2.minAreaRect(cnt)
        (x,y), (w,h), angle = rect

        box = cv2.boxPoints(rect)
        box = np.int32(box)

        cv2.circle(output_frame, (int(x), int(y)), 5, (0,0,255) ,-1)
        cv2.polylines(output_frame, [box], isClosed=True, color=(0, 0, 255), thickness=5)

        cv2.putText(output_frame, "Width {}".format(round(w,1)), (int(x), int(y - 15)), cv2.FONT_HERSHEY_PLAIN, 3, (100, 200, 0), 2)

        #print(box)


    # Show the result
    #cv2.imshow('Original Image', frame)
    cv2.imshow('Canny Edges', canny)
    #cv2.imshow('Contours', output_frame)

    if cv2.waitKey(1) and 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()