#python3 -W ignore PI.py

import vrep
import cv2
import array
import numpy as np
import time
from PIL import Image as I


#internet limita o range que uma variável pode assumir
clamp = lambda n, minn, maxn: max(min(maxn, n), minn)

#calcula o centroide de uma faixa da imagem
def centroide_tira(mask, tira, last_value):
	r = np.mean(np.where(mask[tira, :] > 250))
	if np.isnan(r):
		if last_value > mask.shape[1]//2:
			r = mask.shape[1]
		else:
			r = 0
	return r

print('program started')
vrep.simxFinish(-1)
clientID=vrep.simxStart('127.0.0.1',19997,True,True,5000,5)
print ('Connected to remote API server')
r, colorCam = vrep.simxGetObjectHandle(clientID, "kinect_rgb", vrep.simx_opmode_oneshot_wait);
r, leftmotor = vrep.simxGetObjectHandle(clientID, "Pioneer_p3dx_leftMotor", vrep.simx_opmode_oneshot_wait);
r, rightmotor = vrep.simxGetObjectHandle(clientID, "Pioneer_p3dx_rightMotor", vrep.simx_opmode_oneshot_wait);

vrep.simxSetJointTargetVelocity(clientID, leftmotor, 0, vrep.simx_opmode_streaming);
vrep.simxSetJointTargetVelocity(clientID, rightmotor, 0, vrep.simx_opmode_streaming);

r, resolution, image = vrep.simxGetVisionSensorImage(clientID, colorCam, 1, vrep.simx_opmode_streaming);
time.sleep(0.5)

top, mid, bot = 320, 320, 320

#(0.5, 0.02, 2) para (k, kf = 2, 4)
kp, ki, kd = 0.4, 0, 8

I = 0
C = 0
vL, vR = 0.2, 0.2

while True:
	r, resolution, image = vrep.simxGetVisionSensorImage(clientID, colorCam, 1, vrep.simx_opmode_buffer);
	mat = np.asarray(image, dtype=np.uint8) 
	mat2 = mat.reshape(resolution[1], resolution[0], 1)

	img = cv2.flip( mat2, 0 )
	#480, 640
	#mask = cv2.inRange(img, cor1, cor2)
	mask = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY_INV)[1]
	mask = cv2.medianBlur(mask, 5) #tirar pontos brancos
	
	top = centroide_tira(mask, mask.shape[0]//8, top)
	mid = centroide_tira(mask, mask.shape[0]//2, mid)
	bot = centroide_tira(mask, mask.shape[0]-1, bot)


	#(2, 1.5), (1.5 , 1.5)
	k = 5
	kF = 1.3

	C_prev = C

	Cb = bot - mask.shape[1]//2
	Cm = mid - mask.shape[1]//2
	Ct = top - mask.shape[1]//2

	C = Cb * (6/6)

	#C = ((mid + bot)/2) - mask.shape[1]//2
	#C = bot - mask.shape[1]//2

	P = kp * (C/(mask.shape[1]//2))
	I += ki * (C/(mask.shape[1]//2))
	D = kd * ((C/(mask.shape[1]//2)) - (C_prev/(mask.shape[1]//2)))
	r = P + I + D
	vL, vR = 4 + r * k, 4 - r * k

	vLf = clamp(vL * kF, 0.5, 8)
	vRf = clamp(vR * kF, 0.5, 8)



	#print(C, C_prev)
	print("{:.2f} {:.2f}".format(vLf, vRf))
	#print("Erro Total: {:6.2f}     {:6.2f} {:6.2f} {:6.2f}".format(C, Cb, Cm, Ct))

	vrep.simxSetJointTargetVelocity(clientID, leftmotor, vLf, vrep.simx_opmode_streaming);
	vrep.simxSetJointTargetVelocity(clientID, rightmotor, vRf, vrep.simx_opmode_streaming);

	#cv2.ellipse(mask, center = (int(top), mask.shape[0]//8), axes = (20, 20), angle = 0, startAngle = 0, endAngle = 360, color = 127, thickness = -1)
	#cv2.ellipse(mask, center = (int(mid), mask.shape[0]//2), axes = (20, 20), angle = 0, startAngle = 0, endAngle = 360, color = 127, thickness = -1)
	cv2.ellipse(mask, center = (int(bot), mask.shape[0]-1), axes = (20, 20), angle = 0, startAngle = 0, endAngle = 360, color = 127, thickness = -1)
	cv2.imshow('robot camera', mask)	

	if cv2.waitKey(1) & 0xFF == ord('q'):
            break

	cv2.waitKey(1)