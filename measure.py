import cv2
import numpy as np

# Function to compare both gates!
def check_gate_widths_equal(gate_widths, threshold=5):
    if len(gate_widths) != 2:
        print("Error: Two gates not detected.")
        return False
    
    # Compare the widths of both detected poles
    width_diff = abs(gate_widths[0] - gate_widths[1])
    
    # If the difference is within the threshold, the gates equal MAGA
    if width_diff <= threshold:
        return True
    else:
        return False

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

gate_width = []

for cnt in contours:
    #Draw the edges
    #cv2.polylines(output_img, [cnt], isClosed=True, color=(0, 255, 0), thickness=5)

    #Get rect
    rect = cv2.minAreaRect(cnt)
    (x,y), (w,h), angle = rect

    #Store the width??
    gate_width.append(w)

    box = cv2.boxPoints(rect)
    box = np.int32(box)

    cv2.circle(output_img, (int(x), int(y)), 5, (0,0,255) ,-1)
    cv2.polylines(output_img, [box], isClosed=True, color=(0, 0, 255), thickness=5)

    cv2.putText(output_img, "Width {}".format(round(w,1)), (int(x), int(y - 15)), cv2.FONT_HERSHEY_PLAIN, 3, (100, 200, 0), 2)

    print(box)

# Check if the gate widths are equal
if check_gate_widths_equal(gate_width):
    print("The widths of both poles are equal!")
else:
    print("The widths of the poles are not equal.")

# Show the result
cv2.imshow('Original Image', img)
cv2.imshow('Canny Edges', canny)
cv2.imshow('Contours', output_img)

cv2.waitKey(0)
cv2.destroyAllWindows()