import cv2
import numpy as np
from proper_clustering import cluster
from extract_line_data import extractLineData

lines_data = extractLineData()
grouped_lines = cluster(lines_data)

def draw_clustered_lines(image, grouped_lines):
    k = 3000  #length multiplier
    
    #Draw the left pole (green line)
    for line in grouped_lines["left_pole"]:
        rho, theta = line["rho"], line["theta"]
        d_hat = np.array([[np.cos(theta)], [np.sin(theta)]])
        d = rho * d_hat
        l_hat = np.array([[-np.sin(theta)], [np.cos(theta)]])
        p1 = (d + k * l_hat).astype(int)
        p2 = (d - k * l_hat).astype(int)
        cv2.line(image, (p1[0][0], p1[1][0]), (p2[0][0], p2[1][0]), (0, 255, 0), 3)  # Green line
    
    #Draw the right pole (green line)
    for line in grouped_lines["right_pole"]:
        rho, theta = line["rho"], line["theta"]
        d_hat = np.array([[np.cos(theta)], [np.sin(theta)]])
        d = rho * d_hat
        l_hat = np.array([[-np.sin(theta)], [np.cos(theta)]])
        p1 = (d + k * l_hat).astype(int)
        p2 = (d - k * l_hat).astype(int)
        cv2.line(image, (p1[0][0], p1[1][0]), (p2[0][0], p2[1][0]), (0, 255, 0), 3)  # Green line
    
    #Draw the top pole (red line)
    top_line = grouped_lines["top_pole"]
    rho, theta = top_line["rho"], top_line["theta"]
    d_hat = np.array([[np.cos(theta)], [np.sin(theta)]])
    d = rho * d_hat
    l_hat = np.array([[-np.sin(theta)], [np.cos(theta)]])
    p1 = (d + k * l_hat).astype(int)
    p2 = (d - k * l_hat).astype(int)
    cv2.line(image, (p1[0][0], p1[1][0]), (p2[0][0], p2[1][0]), (0, 0, 255), 3)  # Red line
    
    return image


image_path = '/Users/R.Abinav/Desktop/CV/AUV/images/good.jpeg'  
img = cv2.imread(image_path)

#Draw clustered lines on the image
result_img = draw_clustered_lines(img, grouped_lines)


cv2.imshow("Clustered Lines", result_img)
cv2.waitKey(0)
cv2.destroyAllWindows()

