import numpy as np
import matplotlib.pyplot as plt
import cv2

color = "RGB"

cap = cv2.VideoCapture(0)

bins = 255
alpha = 1

fig, ax = plt.subplots()

#lineR, unpack para o primeiro, equivale a ax.plot[0]
if color == "RGB":
    lineR, = ax.plot(np.arange(bins), np.zeros(bins), c='r', lw =3, alpha=alpha, label = "RED")
    lineG, = ax.plot(np.arange(bins), np.zeros(bins), c='b', lw =3, alpha=alpha, label = "BLUE")
    lineB, = ax.plot(np.arange(bins), np.zeros(bins), c='g', lw =3, alpha=alpha, label = "GREEN")
elif color == "GS":
    lineGRAY, = ax.plot(np.arange(bins), np.zeros(bins), c='k', lw =3, alpha=alpha, label = "Intensidade")

ax.set_xlim(0, bins-1)
ax.set_ylim(0, 20000)
ax.legend()
plt.ion()
plt.show()
    
while cap.isOpened():
    ret, frame = cap.read()
    if ret == True:
        numPixels = np.prod(frame.shape[:2])
        if color == "RGB":
            cv2.imshow("RGB", frame)
            b, g, r = cv2.split(frame)
            hR = cv2.calcHist([r], [0], None, [bins], [0, 255])
            hG = cv2.calcHist([g], [0], None, [bins], [0, 255])
            hB = cv2.calcHist([b], [0], None, [bins], [0, 255])
            lineR.set_ydata(hR)
            lineG.set_ydata(hG)
            lineB.set_ydata(hB)
        elif color == "GS":
            frame_gs = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            cv2.imshow("GS", frame_gs)
            hI = cv2.calcHist([frame_gs], [0], None, [bins], [0, 255])
            lineGRAY.set_ydata(hI)
        fig.canvas.draw()
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

cap.release()
cv2.destroyAllWindows()