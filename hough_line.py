import cv2
import numpy as np

def houghLineTransform():
    image_path = '/Users/R.Abinav/Desktop/CV/AUV/images/good.jpeg'
    img = cv2.imread(image_path)

    if img is None:
        print("Image wasnt loaded!!")
        return

    #Convert to gray scale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    #Some method to enhance contrast in the image 
    clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8, 8))
    gray_equalized = clahe.apply(gray)

    #Apply blur to reduce noise? -> I dont think its required -> Need to clarify while testing
    #blur = cv2.GaussianBlur(gray_equalized, (5,5), 0)

    #Use Canny Edge to detect edges
    canny = cv2.Canny(gray_equalized, 50, 150)

    #Set up some required variables for hough transform
    distReso = 1
    angleReso = np.pi/180
    threshold = 80      #Experiment with value

    lines = cv2.HoughLines(canny, distReso, angleReso, threshold)

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
    
    #cv2.imshow('Blurred', blur)
    cv2.imshow('Canny Edges', canny)
    cv2.imshow('Lines?', img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

if __name__ == "__main__":
    houghLineTransform()
