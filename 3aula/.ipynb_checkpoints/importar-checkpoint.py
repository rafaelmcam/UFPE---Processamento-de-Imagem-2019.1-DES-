import numpy as np
import cv2
from skimage.util import random_noise


def gs_f(frame):
        return (cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY))
        return frame

def salt_pepper(frame):
        return (random_noise(frame, mode = "s&p"))
