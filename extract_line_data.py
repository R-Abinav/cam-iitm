import cv2
import numpy as np

def extractLineData():
    image_path = '/Users/R.Abinav/Desktop/CV/AUV/images/good.jpeg'
    img = cv2.imread(image_path)

    #Convert to gray
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    #Use CLAHE to enhance contrast
    clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8,8))
    gray_equalised = clahe.apply(gray)

    #Canny Edge 
    canny = cv2.Canny(gray_equalised, 50, 150)

    #Variable for HoughTransform
    distReso = 1
    angleReso = np.pi/180
    threshold = 80

    lines = cv2.HoughLines(canny, distReso, angleReso, threshold)
    lines_data = []

    k = 3000

    if lines is not None:
        for line in lines:
            rho, theta = line[0]
            
            if abs(theta) < 0.1 or abs(theta - np.pi) < 0.1:
                color = (0,255,0) # Green color for horizontal lines
            elif abs(theta - np.pi / 2) < 0.1:
                color = (0,0,255) # Red color for vertical lines
            else:
                continue

            #Find Points 
            d_hat = np.array([[np.cos(theta)],[np.sin(theta)]])
            d = rho*d_hat

            l_hat = np.array([[-np.sin(theta)],[np.cos(theta)]])
                
            p1 = d + k*l_hat
            p2 = d - k*l_hat

            p1 = p1.astype(int)
            p2 = p2.astype(int)

            cv2.line(img, (p1[0][0], p1[1][0]), (p2[0][0], p2[1][0]), color, 3)

            #Calculate the line length
            length = np.sqrt((p2[0][0] - p1[0][0])**2 + (p2[1][0] - p1[1][0])**2)

            #Calculate the midpoint
            midpoint = ((p2[0][0] + p1[0][0])/2, (p2[1][0] + p1[1][0])/2)

            #Calculate Slope And Intercept
            if abs(np.cos(theta)) > 1e-6:              #Non vertical line
                slope = -np.sin(theta)/np.cos(theta)
                intercept = rho / np.cos(theta)
            else:
                slope = float('inf')
                intercept = float('inf')

            lines_data.append({
                "rho": rho,
                "theta": theta,
                "slope": slope,
                "intercept": intercept,
                "length": length,
                "midpoint": midpoint
            })
    
    return lines_data






