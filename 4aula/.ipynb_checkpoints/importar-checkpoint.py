import numpy as np
import cv2
from skimage.util import random_noise


def gs_f(frame):
        gs = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
        cv2.imshow("Frame GS", gs)
        return
    
###############

def salt_pepper(frame):
        gs = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        sp = random_noise(gs, mode = "s&p")
        cv2.putText(sp,'PROCESSED IMAGE', (0,50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), 2)
        #cv2.imshow("Frame Salt and Pepper", sp)
        return sp

def salt_pepper_half(frame):
    #comentar abaixo ou não para colorido/gs
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
 
    left, middle, right = frame[:,:frame.shape[1]//3]/255 , frame[:,frame.shape[1]//3:frame.shape[1]*2//3] , frame[:,frame.shape[1]*2//3:]
    
    middle, right = random_noise(middle, mode = "s&p"), random_noise(right, mode = "s&p")
    
    right = cv2.medianBlur(np.float32(right), 5)
    
    processed = np.concatenate((left, middle, right), axis=1)

    cv2.putText(processed,'Original', (0,50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), 2)
    cv2.putText(processed,'S&P', (frame.shape[1]//3,50), cv2.FONT_HERSHEY_SIMPLEX, 1, (10,10,10), 2)
    cv2.putText(processed,'S&P + Median Blur', (frame.shape[1]*2//3,50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,0), 2)
    return processed


# def filter_img(img,kernel = np.ones((3, 3), dtype="float32")/9):
#     return cv2.filter2D(img, -1, kernel)


###############
def default(frame, e):

    cv2.putText(frame,'DEFAULT IMAGE', (0,50), cv2.FONT_HERSHEY_SIMPLEX, 1, (160,255,255), 2)
    cv2.putText(frame, str(e), (0,100), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,255), 2)
    cv2.imshow('frame',frame)
    return
