import cv2
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
from mediapipe_utils import draw_landmarks_on_image
from mediapipe_utils import get_distance
from io import BytesIO
from time import sleep

cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print('Cannot open camera')
    exit()
base_options = python.BaseOptions(model_asset_path='dataprep/hand_landmarker.task')
options = vision.HandLandmarkerOptions(base_options=base_options,
                                        num_hands=2)
detector = vision.HandLandmarker.create_from_options(options)
while True:
    ret, frame = cap.read()
    if not ret:
        print("Can't receive frame")
        break
    image = mp.Image(image_format=mp.ImageFormat.SRGB, data=frame)
    detection_result = detector.detect(image)
    
    text = None
    distance = get_distance(detection_result.hand_world_landmarks, 'INDEX_FINGER_TIP', 'THUMB_TIP')
    if distance is not None and (1/distance)**2 > 200:
        print((1/distance)**2)
        text = 'OK!'
    
    annotated_image = draw_landmarks_on_image(image.numpy_view(), detection_result, text_override=text)
    cv2.imshow('frame', annotated_image)
    cv2.waitKey(1)

cap.release()
cv2.destroyAllWindows()