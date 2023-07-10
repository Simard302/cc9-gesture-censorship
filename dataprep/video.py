import cv2, os
import mediapipe as mp
import numpy as np
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
from mediapipe_utils import get_distance, calc_blur, apply_blur, draw_landmarks_on_image, get_landmark_name
from support_vec_class import get_model
import multiprocessing
from queue import Queue

# CONFIG
IMG_FILTER_CLASS = ['MF']
IMG_TRAIN_SET = os.path.join('dataprep', 'data', 'training','features_middlefinger.csv')
IMG_THREADS = 1
IMG_WIDTH = 320
DISABLE_OVERLAY = False

# Initialize detector and model
base_options = python.BaseOptions(model_asset_path=os.path.join('dataprep', 'data', 'hand_landmarker.task'))
options = vision.HandLandmarkerOptions(
    base_options=base_options,
    num_hands=2,
    running_mode=vision.RunningMode.VIDEO
)
detector = vision.HandLandmarker.create_from_options(options)
model = get_model(IMG_TRAIN_SET)

def display_image(ret, frame, ts, w, h):
    if not ret:
        return None
    scale = IMG_WIDTH/w
    frame = cv2.resize(frame, (int(w*scale), int(h*scale)))
    image = mp.Image(image_format=mp.ImageFormat.SRGB, data=frame)
    detection_result = detector.detect_for_video(image, ts)
    image = image.numpy_view()
    out_image = np.copy(image)

    if len(detection_result.hand_world_landmarks)>0:
        classes = []
        for hand in range(0, len(detection_result.hand_world_landmarks)):
            features = []
            for i in range(0, 21):
                name_landmark = get_landmark_name(i)
                for k in range(0, 21):
                    distance = get_distance(detection_result.hand_world_landmarks[hand], name_landmark, get_landmark_name(k))
                    features.append(float(distance))
            classes.append(model.predict([features])[0])
            if classes[hand] in IMG_FILTER_CLASS:
                out_image = apply_blur(out_image, 
                    calc_blur(out_image, detection_result.hand_landmarks[hand])
                )
        # Draw lines on hands + label
        if not DISABLE_OVERLAY: out_image = draw_landmarks_on_image(out_image, detection_result, text_override=classes)
    
    return out_image

def calc_image(cap):
    fps = cap.get(cv2.CAP_PROP_FPS)
    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    fourcc = cv2.VideoWriter_fourcc(*'MJPG')
    #scale = IMG_WIDTH/frame_width
    scale = 1
    output = cv2.VideoWriter('temp_short.avi', fourcc, fps, (int(frame_width*scale), int(frame_height*scale)))
    with multiprocessing.Pool(IMG_THREADS) as pool:
        results = Queue()
        i = 0
        lastTs = -1
        while True:
            ret, frame = cap.read()
            ts = int(cap.get(cv2.CAP_PROP_POS_MSEC))
            if i > 30: break
            if ts > lastTs:
                lastTs = ts
                #results.put(pool.apply_async(display_image, [ret, frame, ts, frame_width, frame_height]))
                results.put(frame)

            if results.qsize() >= IMG_THREADS or ts == 0:
                #image = results.get().get()
                image = results.get()
                if image is None: break
                cv2.imshow('frame', image)
                output.write(image)
                cv2.waitKey(1)
            
            print(f"Completed frame: {i}")
            i+=1
    output.release()

# Loop over video feed
if __name__ == '__main__':
    os.environ['OPENCV_LOG_LEVEL'] = 'DEBUG'
    os.environ['OPENCV_VIDEOIO_DEBIG'] = '1'
    print(cv2.__version__)
    print(cv2.getBuildInformation())
    cap = cv2.VideoCapture("dataprep/data/video/test.avi", cv2.CAP_FFMPEG)
    print(cap.isOpened())
    #cap = cv2.VideoCapture(0)
    ret, frame = cap.read()
    file = calc_image(cap)
    print(file)
    cap.release()
    cv2.destroyAllWindows()