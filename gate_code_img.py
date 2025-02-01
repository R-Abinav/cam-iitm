import cv2
import numpy as np

#below is the intersection of two lines in Ax + By + C = 0 form
def find_intersection(line1, line2):
    A1, B1, C1 = line1
    A2, B2, C2 = line2
    det = A1 * B2 - A2 * B1
    if det == 0:  
        return None
    x = (B1 * C2 - B2 * C1) / det
    y = (A2 * C1 - A1 * C2) / det
    return int(x), int(y)

# Load the image
image_path = "/Users/R.Abinav/Desktop/CV/AUV/images/croppped.png"  # Change this to your image path
frame = cv2.imread(image_path)

if frame is None:
    print("Error, while fetching the image!")
    exit()

#Initial frame
cv2.imshow("Initial Frame", frame)

#The Limits for the colors
#                 H    S    V
lower1 = np.array([0, 20, 30])
upper1 = np.array([10, 250, 255])

lower2 = np.array([170, 20, 30])
upper2 = np.array([180, 250, 255])

#Apply the color mask , so that the image only sees the color 
hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
mask1 = cv2.inRange(hsv, lower1, upper1)
mask2 = cv2.inRange(hsv, lower2, upper2)
_mask = cv2.bitwise_or(mask1, mask2)

#Now Apply edge detection on the mask?? -> Find the edges in the mask -> Should only see the edges of the gate?
thresh1 = 50 #50
thresh2 = 150 #150
edge = cv2.Canny(_mask, thresh1, thresh2)

#Line Detection 
threshold = 100 #100    #Higher the threshold, it detects only stronger lines.
lines = cv2.HoughLines(edge, 1, np.pi/180, threshold)

if lines is not None:
    verti = []
    hori = []

    for rho,theta in lines[:,0]:
        #print(f"rho: {rho}, theta (degrees): {np.degrees(theta)}")
        a = np.cos(theta)
        b = np.sin(theta)
        x0 = a * rho
        y0 = b * rho
        x1 = int(x0 + 1000 * (-b))
        y1 = int(y0 + 1000 * (a))
        x2 = int(x0 - 1000 * (-b))
        y2 = int(y0 - 1000 * (a))

        # cv2.line(frame, (x1, y1), (x2, y2), (255, 0, 0), 2)  # Blue lines for all detected
        # cv2.imshow("Line Detection in Progress", frame)
        # cv2.waitKey(500)  # Show each line for 500 milliseconds

        #The acceptable tolerance -> Imma keep it high , CHANGE WHILE TESTING
        lower_verti, higher_verti = 80, 100
        lower_hori, higher_hori = -10, 10

        # THE OLD CONDITIONS ?:
        # if lower_verti <= np.degrees(theta) <= higher_verti:
        #     verti.append((rho, theta, x1, y1, x2, y2))
        # elif lower_hori <= np.degrees(theta) <= higher_hori:
        #     hori.append((rho, theta, x1, y1, x2, y2))

        if lower_hori <= np.degrees(theta) <= higher_hori:
            verti.append((rho, theta, x1, y1, x2, y2))  # These are horizontal lines
        elif lower_verti <= np.degrees(theta) <= higher_verti:
            hori.append((rho, theta, x1, y1, x2, y2))  # These are vertical lines
    
    # #I wanna see what i appeneded in the hori, verti array:
    # for rho, theta, x1, y1, x2, y2 in verti:
    #     cv2.line(frame, (x1, y1), (x2, y2), (255, 0, 0), 2)
    #     cv2.imshow("Vertical Lines", frame)
    #     cv2.waitKey(300)  # Show for 3s

    # # Draw all horizontal lines in green
    # for rho, theta, x1, y1, x2, y2 in hori:
    #     cv2.line(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
    #     cv2.imshow("Horizontal Lines", frame)
    #     cv2.waitKey(300)  # Show for 3s

    if len(verti) >=2 and len(hori) >=1:
        #Is the down code really required??
        #I am assuming it is required, as i am not clustering lines, there will a hell lot of lines forming on the poles

        #Down code is to find the line closest to the left
        left_line = verti[0]
        for li in verti:
            if li[0] < left_line[0]:
                left_line = li
        
        #Down code is to find the line closest to the right
        right_line = verti[0]
        for li in verti:
            if li[0] > right_line[0]:
                right_line = li

        #Down code is to find the line closest to the top
        top_line = hori[0]
        for li in hori:
            if li[1] < top_line[1]:
                top_line = li

        #I am just drawing the selected lines in greeen
        for line in [left_line, right_line, top_line]:
            rho, theta, x1, y1, x2, y2 = line
            cv2.line(frame, (x1, y1), (x2, y2), (0, 255, 0), 5)
        
        #Define the line equations -> This from gpt
        left_eq = (np.cos(left_line[1]), np.sin(left_line[1]), -left_line[0])
        right_eq = (np.cos(right_line[1]), np.sin(right_line[1]), -right_line[0])
        top_eq = (np.cos(top_line[1]), np.sin(top_line[1]), -top_line[0])

        #Find the intersections
        corners = [find_intersection(left_eq,top_eq), find_intersection(top_eq, right_eq)]
        #print("Corners:", corners)

        #Draw the lines
        for line in [left_line, right_line, top_line]:
            rho, theta, x1, y1, x2, y2 = line
            cv2.line(frame, (x1, y1), (x2, y2), (0, 255, 0), 5)

        #Mark the corners
        for corner in corners:
            if corner:
                cv2.circle(frame, corner, 8, (0, 0, 255), -1) 
            
        #We can add text on the frame
        cv2.putText(frame, "Gate Detected!",(250,250), cv2.FONT_HERSHEY_PLAIN, 5, (0,0,255), 2)
        print("Gate Detected!")

#Show the windows
cv2.imshow("Masked Image", _mask)
cv2.imshow('Final Frame', frame)

#Wait for user to press any key and close
cv2.waitKey(0)
cv2.destroyAllWindows()
