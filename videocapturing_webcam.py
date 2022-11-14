import cv2
video = cv2.VideoCapture(2)


while(True):
	ret, frame = video.read()
	frame = cv2.resize(frame, (0,0),fx=0.4,fy=0.4)
	cv2.imshow('webcam', frame)
	if cv2.waitKey(1) & 0xFF == ord('s'):
            break


video.release()

cv2.destroyAllWindows()
