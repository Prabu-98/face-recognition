import cv2
cap = cv2.VideoCapture()
_,frame = cap.read()
cv2.imshow('hsd',frame)
cv2.waitKey(1)
