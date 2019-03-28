#Aluno: Rafael Mendes Campello

import math
import numpy as np
import cv2

width = 640
height = 480

referencePoints = np.float32([


[10, height // 2], [110, height // 2], [110, 9* height // 10], [10, 9* height // 10],

[200, height // 2], [300, height // 2], [300, 9* height // 10], [200, 9* height // 10],

[400, height // 2], [500, height // 2], [500, 9* height // 10], [400, 9* height // 10],

])


currentPoint = -1
calibrating = True
fullScreen = False


image = np.zeros((height, width, 3), np.uint8)

cap = cv2.VideoCapture("f1.mp4")
ret1, frame1 = cap.read()

pts_frame = np.float32([[0,0],[frame1.shape[1], 0],[frame1.shape[1],frame1.shape[0]],[0,frame1.shape[0]]])
n_frames1 = 1

cap2 = cv2.VideoCapture("sampleV.mp4")
ret2, frame2 = cap2.read()

pts_frame2 = np.float32([[0,0],[frame2.shape[1], 0],[frame2.shape[1],frame2.shape[0]],[0,frame2.shape[0]]])
n_frames2= 1

cap3 = cv2.VideoCapture("sampleV2.mp4")
ret3, frame3 = cap3.read()

pts_frame3 = np.float32([[0,0],[frame3.shape[1], 0],[frame3.shape[1],frame3.shape[0]],[0,frame3.shape[0]]])
n_frames3= 1

print(pts_frame)
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
	ret1, frame1 = cap.read()
	n_frames1 += 1

	ret2, frame2 = cap2.read()
	n_frames2 += 1

	ret3, frame3 = cap3.read()
	n_frames3 += 1

	if n_frames1 >= int(cap.get(cv2.CAP_PROP_FRAME_COUNT)):
		n_frames1 = 0
		cap.set(cv2.CAP_PROP_POS_FRAMES, n_frames1)

	if n_frames2 >= int(cap2.get(cv2.CAP_PROP_FRAME_COUNT)):
		n_frames2= 0
		cap2.set(cv2.CAP_PROP_POS_FRAMES, n_frames2)

	if n_frames3 >= int(cap3.get(cv2.CAP_PROP_FRAME_COUNT)):
		n_frames3 = 0
		cap3.set(cv2.CAP_PROP_POS_FRAMES, n_frames3)


	image[:] = (0,0,0)
	if calibrating:
		color = 0
		for point in referencePoints:
			cv2.circle(image, (int(point[0]), int(point[1])),5,pointColor(color), -1)
			color = color + 1


	M = cv2.getPerspectiveTransform(pts_frame,referencePoints[:4])
	cv2.warpPerspective(frame1, M, (width,height), image, borderMode=cv2.BORDER_TRANSPARENT)

	M2 = cv2.getPerspectiveTransform(pts_frame2,referencePoints[4:8])
	cv2.warpPerspective(frame2, M2, (width,height), image, borderMode=cv2.BORDER_TRANSPARENT)

	M3 = cv2.getPerspectiveTransform(pts_frame3,referencePoints[8:12])
	cv2.warpPerspective(frame3, M3, (width,height), image, borderMode=cv2.BORDER_TRANSPARENT)

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