import cv2
import numpy as np

img_path = '/Users/R.Abinav/Desktop/CV/AUV/images/circle.jpeg'
img = cv2.imread(img_path)

#Convert to gray
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

#Canny edge
canny = cv2.Canny(img, 30, 250)

#Contour Detection
contours, heirarchies = cv2.findContours(canny, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
print(len(contours))


output_img = img.copy()
for cnt in contours:
    #Draw the edges
    #cv2.polylines(output_img, [cnt], isClosed=True, color=(0, 255, 0), thickness=5)

    #Get rect
    rect = cv2.minAreaRect(cnt)
    (x,y), (w,h), angle = rect

    box = cv2.boxPoints(rect)
    box = np.int32(box)

    cv2.circle(output_img, (int(x), int(y)), 5, (0,0,255) ,-1)
    cv2.polylines(output_img, [box], isClosed=True, color=(0, 0, 255), thickness=5)

    cv2.putText(output_img, "Width {}".format(round(w,1)), (int(x), int(y - 15)), cv2.FONT_HERSHEY_PLAIN, 3, (100, 200, 0), 2)

    print(box)


# Show the result
cv2.imshow('Original Image', img)
cv2.imshow('Canny Edges', canny)
cv2.imshow('Contours', output_img)

cv2.waitKey(0)
cv2.destroyAllWindows()