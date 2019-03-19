import vrep
import cv2
import array
import numpy as np
import time
from PIL import Image as I


def mapRange(value, leftMin, leftMax, rightMin, rightMax):
    # Figure out how 'wide' each range is
    leftSpan = leftMax - leftMin
    rightSpan = rightMax - rightMin

    # Convert the left range into a 0-1 range (float)
    valueScaled = float(value - leftMin) / float(leftSpan)

    # Convert the 0-1 range into a value in the right range.
    return rightMin + (valueScaled * rightSpan)


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


while True:
	r, resolution, image = vrep.simxGetVisionSensorImage(clientID, colorCam, 1, vrep.simx_opmode_buffer);
	mat = np.asarray(image, dtype=np.uint8) 
	mat2 = mat.reshape(resolution[1], resolution[0], 1)

	img = cv2.flip( mat2, 0 )
	#480, 640
	#mask = cv2.inRange(img, cor1, cor2)
	mask = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY_INV)[1]
	mask = cv2.medianBlur(mask, 5) #tirar pontos brancos
	

	try:
		meio = np.mean(np.argwhere(np.array([i * mask[(mask.shape[0]//2)*1, i]/255 for i in range(mask.shape[1])])))
	except:
		meio = np.zeros(1)
		
	try:
		fim = np.mean(np.argwhere(np.array([i * mask[(mask.shape[0]-1), i]/255 for i in range(mask.shape[1])])))
	except:
		fim = np.zeros(1)


	#print(meio, fim)
	
	#quanto maior o T o K precisa ser menor pra não dar um ganho proporcional muito grande
	k = 6
	T = 4
	#pares testados (2, 14), (3, 10), (6, 4)


	print(meio, fim)

	PAR = 100

	if np.isnan(meio):
		if vR > vL:
			vl, vR = 0, 0.4*T
		else:
			vl, vR = 0.4*T, 0
		pass
	else:
		if abs(meio - mask.shape[1]//2) > PAR:
			if meio > mask.shape[1]//2:
				print("Virada forçada à Direita")
				vL, vR = 0.1*k*T, 0.1*T
			elif meio < mask.shape[1]//2:
				print("Virada forçada à Esquerda")
				vL, vR = 0.1*T, 0.1*k*T
		else:
			vL, vR = mapRange(fim, 0, mask.shape[0], -0.4, 0.4)*T, 0.2*T
			print("Ajuste Fino Proporcional")
			#mapRange(fim, 0, mask.shape[0], -0.1, 0.1)
		

	vrep.simxSetJointTargetVelocity(clientID, leftmotor, vL, vrep.simx_opmode_streaming);
	vrep.simxSetJointTargetVelocity(clientID, rightmotor, vR, vrep.simx_opmode_streaming);	
	cv2.imshow('robot camera', mask)	

	if cv2.waitKey(1) & 0xFF == ord('q'):
            break

	cv2.waitKey(1)