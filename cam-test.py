#A file for checking if the desired cam is opening or not
import cv2

cam_num = 0
cap = cv2.VideoCapture(cam_num)

while True:
  ret, frame = cap.read()
  if not ret or frame is None:
    print("Error in fetching the frames from the camera")

  #Display the window
  cv2.imshow("Frame", frame)

  if cv2.waitKey(1) & 0xFF == ord('q'):
      break

cap.release()
cv2.destroyAllWindows()

