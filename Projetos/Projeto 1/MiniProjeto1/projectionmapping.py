import math
import numpy as np
import cv2

width = 640
height = 480

referencePoints = np.float32([[10, 10],[20, 10],[20, 20],[10, 20], [40, 10], [60, 10], [60, 60], [40, 60], [100, 100], [150, 100], [150, 150], [100, 150]])


currentPoint = -1
calibrating = True
fullScreen = False

inputimage1 = cv2.imread("pp.jpg")
rows1, cols1 = inputimage1.shape[:2]
pts1 = np.float32([[0,0],[cols1,0],[cols1,rows1],[0,rows1]])

image = np.zeros((height, width, 3), np.uint8)

cap = cv2.VideoCapture("f1.mp4")
ret, frame = cap.read()
pts_frame = np.float32([[0,0],[frame.shape[1], 0],[frame.shape[1],frame.shape[0]],[0,frame.shape[0]]])
n_frames = 1

def pointColor(n):
	if n%4 == 0:
		return (0,0,255)
	elif n%4 == 1:
		return (0,255,255)
	elif n%4 == 2:
		return (255,255,0)
	else:
		return (0,255,0)

def mouse(event, x, y, flags, param):
	global currentPoint

	if event == cv2.EVENT_LBUTTONDOWN:
		cp = 0
		for point in referencePoints:
			dist = math.sqrt((x-point[0])*(x-point[0])+(y-point[1])*(y-point[1]))
			if dist < 7:
				currentPoint = cp
				break
			else:
				cp = cp + 1


	if event == cv2.EVENT_LBUTTONUP:
		currentPoint = -1
		
	if currentPoint != -1:
		referencePoints[currentPoint] = [x,y]

cv2.namedWindow("test", cv2.WINDOW_NORMAL)
cv2.setMouseCallback("test", mouse)

while True:
	
	image[:] = (0,0,0)
	if calibrating:
		color = 0
		for point in referencePoints:
			cv2.circle(image, (int(point[0]), int(point[1])),5,pointColor(color), -1)
			color = color + 1


	M = cv2.getPerspectiveTransform(pts1,referencePoints[:4])
	cv2.warpPerspective(inputimage1, M, (width,height), image, borderMode=cv2.BORDER_TRANSPARENT)

	M2 = cv2.getPerspectiveTransform(pts1,referencePoints[4:8])
	cv2.warpPerspective(inputimage1, M2, (width,height), image, borderMode=cv2.BORDER_TRANSPARENT)

	M3 = cv2.getPerspectiveTransform(pts1,referencePoints[8:12])
	cv2.warpPerspective(inputimage1, M3, (width,height), image, borderMode=cv2.BORDER_TRANSPARENT)

	cv2.imshow("test", image)
	key = cv2.waitKey(1) & 0xFF

	if key == ord("c"):
		calibrating = not calibrating

	if key == ord("f"):
		if fullScreen == False:
			cv2.setWindowProperty("test", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
		else:
			cv2.setWindowProperty("test", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_NORMAL)
		fullScreen = not fullScreen

	if key == ord("q"):
		break

cv2.destroyAllWindows()