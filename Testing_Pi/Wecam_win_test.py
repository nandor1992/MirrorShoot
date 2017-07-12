import cv2
cap = cv2.VideoCapture(0)
count = 0

   # Capture frame-by-frame
ret, frame = cap.read()

cv2.imwrite("../Resource/Photo/frame.jpg", frame)     # save frame as JPEG file