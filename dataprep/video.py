import cv2
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
from mediapipe_utils import get_distance, calc_blur, apply_blur, draw_landmarks_on_image, get_landmark_name
from support_vec_class import get_model

# CONFIG
MAX_BLUR = 1
FILTER_CLASS = ['Z', 'Y', '2', 'W']


# Create detector and video capture
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print('Cannot open camera')
    exit()
base_options = python.BaseOptions(model_asset_path='dataprep/hand_landmarker.task')
options = vision.HandLandmarkerOptions(base_options=base_options,
                                        num_hands=2)
detector = vision.HandLandmarker.create_from_options(options)
model = get_model()


# Loop over video feed
blurCounter = 0
blurData = None
while True:
    ret, frame = cap.read()
    if not ret:
        print("Can't receive frame")
        break
    image = mp.Image(image_format=mp.ImageFormat.SRGB, data=frame)
    detection_result = detector.detect(image)
    image = image.numpy_view()

    text = None
    blur = False
    # Calculate the distance, inc blur accordingly
    #distance = get_distance(detection_result.hand_world_landmarks, 'INDEX_FINGER_TIP', 'THUMB_TIP')
    if len(detection_result.hand_world_landmarks)>0:
        features = []
        for i in range(0, 21):
            name_landmark = get_landmark_name(i)
            for k in range(0, 21):
                distance = get_distance(detection_result.hand_world_landmarks, name_landmark, get_landmark_name(k))
                features.append(float(distance))
        classification = model.predict([features])[0]
        #if distance is not None and (1/distance)**2 > 200:
        if classification in FILTER_CLASS:
            #print((1/distance)**2)
            text = classification    # Text displayed above hand
            blur = True

            if blurCounter == 0:    # Only calculate blur every MAX_BLUR iterations
                blurData = calc_blur(annotated_image, detection_result.hand_landmarks)
            elif blurCounter > MAX_BLUR:
                blurCounter = 0
            else:
                blurCounter +=1
    else:
        blur = 0
    
    # Draw lines and landmarks on hand
    annotated_image = draw_landmarks_on_image(image, detection_result, text_override=text)

    # If blur, apply blur to image
    if blur:
        annotated_image = apply_blur(annotated_image, blurData)
    
    cv2.imshow('frame', annotated_image)
    cv2.waitKey(1)

cap.release()
cv2.destroyAllWindows()