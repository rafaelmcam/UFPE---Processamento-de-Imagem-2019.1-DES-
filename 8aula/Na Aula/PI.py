import vrep
import cv2
import array
import numpy as np
import time
from PIL import Image as I

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


cor1 = (0, 0, 0)
cor2 = (180, 255, 30)

while True:
	r, resolution, image = vrep.simxGetVisionSensorImage(clientID, colorCam, 1, vrep.simx_opmode_buffer);
	mat = np.asarray(image, dtype=np.uint8) 
	mat2 = mat.reshape(resolution[1], resolution[0], 1)

	img = cv2.flip( mat2, 0 )
	#480, 640
	#mask = cv2.inRange(img, cor1, cor2)
	mask = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY_INV)[1]
	

	try:
		meio = np.mean(np.argwhere(np.array([i * mask[(480//2)*1, i]/255 for i in range(640)])))
	except:
		meio = np.zeros(1)
		
	try:
		fim = np.mean(np.argwhere(np.array([i * mask[(480-1), i]/255 for i in range(640)])))
	except:
		fim = np.zeros(1)

	#print(meio, fim)
	PAR = 120
	#controle prioritário
	


	if meio > 640//2 + PAR:
		print("Virada forçada à Direita")
		ratio = -10000
	elif meio < 640//2 - PAR:
		print("Virada forçada à Esquerda")
		ratio = 10000
	else:#controle secundário
		mask = mask[476:, :]
		lista2 = np.array([sum(mask[:, x]) for x in range(480)])

		
		left = sum(lista2[:480//2])
		right = sum(lista2[480//2:])

		ratio = (left - right)/(255)
		#ratio = left/(left+right+1)
	

	k = 7
	T = 3

	try:
		#vem do prioritário
		if ratio == 10000:
			vR = 0.1*k
			vL = 0
		elif ratio == -10000:
			vL = 0.1*k
			vR = 0
		else:#secundário
			# |x| < 0.06  LINHA RETA caso contrário lembra da última curva que estava fazendo
			if ratio < -250:
				vR = 0.1
				vL = 0.1*k
				lastDir = 1
			elif ratio > 250:
				vR = 0.1*k
				vL = 0.1
				lastDir = -1
			elif ratio == 0:
				if lastDir == 1:
					vR = 0
					vL = 0.1*k
				elif lastDir == -1:
					vR = 0.1*k
					vL = 0
				else:
					vR = 0.1
					vL = 0.1
			else:
				vR = 0.5
				vL = 0.5
	except:
		ratio = -1
		vL = 0
		vR = 0
    

	vR = vR * T
	vL = vL * T

	print(ratio)


	vrep.simxSetJointTargetVelocity(clientID, leftmotor, vL, vrep.simx_opmode_streaming);
	vrep.simxSetJointTargetVelocity(clientID, rightmotor, vR, vrep.simx_opmode_streaming);	
	cv2.imshow('robot camera', mask)	

	if cv2.waitKey(1) & 0xFF == ord('q'):
            break

	cv2.waitKey(1)