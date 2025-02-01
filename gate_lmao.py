import cv2
import numpy as np

# Color thresholds (update as needed)
lower1 = np.array([0, 20, 0])
upper1 = np.array([10, 250, 255])

lower2 = np.array([170, 20, 0])
upper2 = np.array([180, 250, 255])

# Function to find intersection of two lines in Ax + By + C = 0 form
def find_intersection(line1, line2):
    A1, B1, C1 = line1
    A2, B2, C2 = line2
    determinant = A1 * B2 - A2 * B1
    if determinant == 0:  # Lines are parallel
        return None
    x = (B1 * C2 - B2 * C1) / determinant
    y = (A2 * C1 - A1 * C2) / determinant
    return int(x), int(y)

# Load an image (replace "image.jpg" with your actual image path)
image = cv2.imread("/Users/R.Abinav/Desktop/CV/AUV/images/croppped.png")

if image is None:
    print("Error: Could not load image!")
    exit()

# Convert image to HSV and apply color detection
hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
mask1 = cv2.inRange(hsv, lower1, upper1)
mask2 = cv2.inRange(hsv, lower2, upper2)
_mask = cv2.bitwise_or(mask1, mask2)

# Apply edge detection on the mask
edges = cv2.Canny(_mask, 50, 150)

# Detect lines using Hough Line Transform
lines = cv2.HoughLines(edges, 1, np.pi / 180, 100)

if lines is not None:
    vertical_lines = []
    horizontal_lines = []
    for rho, theta in lines[:, 0]:
        a = np.cos(theta)
        b = np.sin(theta)
        x0 = a * rho
        y0 = b * rho
        x1 = int(x0 + 1000 * (-b))
        y1 = int(y0 + 1000 * (a))
        x2 = int(x0 - 1000 * (-b))
        y2 = int(y0 - 1000 * (a))

        if 85 <= np.degrees(theta) <= 95:  # Vertical
            vertical_lines.append((rho, theta, x1, y1, x2, y2))
        elif -5 <= np.degrees(theta) <= 5:  # Horizontal
            horizontal_lines.append((rho, theta, x1, y1, x2, y2))

    # Select prominent lines
    if len(vertical_lines) >= 2 and len(horizontal_lines) >= 1:
        left_line = min(vertical_lines, key=lambda l: l[0])  # Closest to left
        right_line = max(vertical_lines, key=lambda l: l[0])  # Closest to right
        top_line = min(horizontal_lines, key=lambda l: l[1])  # Closest to top

        # Find intersections to mark corners
        left_eq = (np.cos(left_line[1]), np.sin(left_line[1]), -left_line[0])
        right_eq = (np.cos(right_line[1]), np.sin(right_line[1]), -right_line[0])
        top_eq = (np.cos(top_line[1]), np.sin(top_line[1]), -top_line[0])

        corners = [
            find_intersection(left_eq, top_eq),
            find_intersection(right_eq, top_eq),
        ]

        # Draw lines
        for line in [left_line, right_line, top_line]:
            rho, theta, x1, y1, x2, y2 = line
            cv2.line(image, (x1, y1), (x2, y2), (0, 255, 0), 2)

        # Mark corners
        for corner in corners:
            if corner:
                cv2.circle(image, corner, 5, (0, 0, 255), -1)

        # Add gate detection message
        cv2.putText(image, "Gate Detected!!!", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)

# Display the results
cv2.imshow("Mask", _mask)
cv2.imshow("Gate Detection", image)

# Wait for key press and close the window
cv2.waitKey(0)
cv2.destroyAllWindows()
