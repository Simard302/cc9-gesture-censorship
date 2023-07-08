#import numpy as np
import cv2
import mediapipe as mp
from mediapipe_utils import calc_blur, apply_blur
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
#import matplotlib.pyplot as plt

base_options = python.BaseOptions(model_asset_path='dataprep/hand_landmarker.task')
options = vision.HandLandmarkerOptions(base_options=base_options,
                                        num_hands=2)
detector = vision.HandLandmarker.create_from_options(options)

img = cv2.imread('dataprep/data/test_data/hand.jpg')

image = mp.Image(image_format=mp.ImageFormat.SRGB, data=img)
detection_result = detector.detect(image)

blurData = calc_blur(img, detection_result.hand_landmarks)
img = apply_blur(img, blurData)

# fig = plt.figure()
# a1 = fig.add_axes([0, 0, 1, 1])
# a1.pcolormesh(xi, yi, np.greater(zi.reshape(xi.shape), 1), shading='gourand')
# a1.set_xlim(0, 1)
# a1.set_ylim(0, 1)
# a1.scatter(y, x)
cv2.imshow('img', img)
#plt.show()
cv2.waitKey(0)