import cv2
import numpy as np

# Function to find the intersection of two lines in Ax + By + C = 0 form
def find_intersection(line1, line2):
    A1, B1, C1 = line1
    A2, B2, C2 = line2
    det = A1 * B2 - A2 * B1
    if det == 0:
        return None  # Lines are parallel
    x = (B1 * C2 - B2 * C1) / det
    y = (A2 * C1 - A1 * C2) / det
    return int(x), int(y)

# Load the image
image_path = "/Users/R.Abinav/Desktop/CV/AUV/images/croppped.png"  # Change this to your image path
frame = cv2.imread(image_path)

if frame is None:
    print("Error, while fetching the image!")
    exit()

# Initial frame
cv2.imshow("Initial Frame", frame)

# The Limits for the colors (red color range)
#                 H    S    V
lower1 = np.array([0, 20, 0])
upper1 = np.array([10, 250, 255])

lower2 = np.array([170, 20, 0])
upper2 = np.array([180, 250, 255])

# Apply the color mask to isolate the red gate
hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
mask1 = cv2.inRange(hsv, lower1, upper1)
mask2 = cv2.inRange(hsv, lower2, upper2)
_mask = cv2.bitwise_or(mask1, mask2)

# Apply edge detection on the mask to find edges of the gate
thresh1 = 50  # Lower threshold for Canny
thresh2 = 150  # Upper threshold for Canny
edge = cv2.Canny(_mask, thresh1, thresh2)

# Line Detection using Hough Transform
threshold = 100  # Higher threshold detects only stronger lines
lines = cv2.HoughLines(edge, 1, np.pi / 180, threshold)

if lines is not None:
    verti = []  # To store vertical lines (left and right poles)
    hori = []   # To store horizontal lines (top pole)

    for rho, theta in lines[:, 0]:
        print(f"rho: {rho}, theta (degrees): {np.degrees(theta)}")

        a = np.cos(theta)
        b = np.sin(theta)

        x0 = a * rho
        y0 = b * rho
        x1 = int(x0 + 1000 * (-b))
        y1 = int(y0 + 1000 * (a))
        x2 = int(x0 - 1000 * (-b))
        y2 = int(y0 - 1000 * (a))

        # Classify lines as vertical or horizontal based on their angle
        angle = np.degrees(theta)
        if 80 <= angle <= 100:  # Vertical lines (left and right poles)
            verti.append((rho, theta, x1, y1, x2, y2))
        elif -10 <= angle <= 10:  # Horizontal lines (top pole)
            hori.append((rho, theta, x1, y1, x2, y2))

    if len(verti) >= 2 and len(hori) >= 1:
        # Find the leftmost and rightmost vertical lines
        left_line = min(verti, key=lambda x: x[0])  # Line with smallest rho (left pole)
        right_line = max(verti, key=lambda x: x[0])  # Line with largest rho (right pole)

        # Find the topmost horizontal line
        top_line = min(hori, key=lambda x: x[1])  # Line with smallest theta (top pole)

        # Define the line equations in Ax + By + C = 0 form
        left_eq = (np.cos(left_line[1]), np.sin(left_line[1]), -left_line[0])
        right_eq = (np.cos(right_line[1]), np.sin(right_line[1]), -right_line[0])
        top_eq = (np.cos(top_line[1]), np.sin(top_line[1]), -top_line[0])

        # Find the intersections
        corner1 = find_intersection(left_eq, top_eq)  # Intersection of left pole and top pole
        corner2 = find_intersection(top_eq, right_eq)  # Intersection of top pole and right pole
        print("Corners:", corner1, corner2)

        # Draw the detected lines
        for line in [left_line, right_line, top_line]:
            rho, theta, x1, y1, x2, y2 = line
            cv2.line(frame, (x1, y1), (x2, y2), (0, 255, 0), 5)

        # Mark the intersections
        if corner1:
            cv2.circle(frame, corner1, 8, (0, 0, 255), -1)
        if corner2:
            cv2.circle(frame, corner2, 8, (0, 0, 255), -1)

        # Add text to indicate gate detection
        cv2.putText(frame, "Gate Detected!", (250, 250), cv2.FONT_HERSHEY_PLAIN, 5, (0, 0, 255), 2)
        print("Gate Detected!")

# Show the windows
cv2.imshow("Masked Image", _mask)
cv2.imshow('Final Frame', frame)

# Wait for user to press any key and close
cv2.waitKey(0)
cv2.destroyAllWindows()