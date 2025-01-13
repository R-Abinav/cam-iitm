import cv2
import numpy as np

# Load the image
img = cv2.imread('/Users/R.Abinav/Desktop/CV/AUV/images/custom_gate.jpeg')
cv2.imshow('Original Image', img)

# Convert to grayscale
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# Apply median blur to reduce noise
blurred = cv2.medianBlur(gray, 5)

# Mask the region of interest (optional, adjust as needed)
# Here, the assumption is the sticky notes are mostly centered
h, w = gray.shape
roi = np.zeros_like(gray)
cv2.rectangle(roi, (50, 50), (w-50, h-50), 255, -1)  # Adjust ROI bounds
masked = cv2.bitwise_and(blurred, blurred, mask=roi)

# Apply adaptive histogram equalization to enhance contrast
clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
enhanced = clahe.apply(masked)

# Detect edges using adaptive Canny
v = np.median(enhanced)
lower = int(max(0, 0.7 * v))  # Dynamic lower threshold
upper = int(min(255, 1.3 * v))  # Dynamic upper threshold
canny = cv2.Canny(enhanced, lower, upper)
cv2.imshow('Canny Edges', canny)

# Use probabilistic Hough Line Transform
lines = cv2.HoughLinesP(canny, 1, np.pi / 180, threshold=100, minLineLength=100, maxLineGap=20)

# Draw the detected lines on the image
output = img.copy()
if lines is not None:
    for line in lines:
        x1, y1, x2, y2 = line[0]
        cv2.line(output, (x1, y1), (x2, y2), (0, 255, 0), 2)

# Display the results
cv2.imshow("Detected Lines", output)

cv2.waitKey(0)
cv2.destroyAllWindows()
