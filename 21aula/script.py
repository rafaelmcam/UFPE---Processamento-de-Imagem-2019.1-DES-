import cv2
import numpy as np
import matplotlib.pyplot as plt

reshape = (600, 400)

cap = cv2.VideoCapture("video.mp4")

ret, frame = cap.read()
frame = cv2.resize(frame, reshape)

mask = np.zeros(frame.shape, dtype = np.uint8)


