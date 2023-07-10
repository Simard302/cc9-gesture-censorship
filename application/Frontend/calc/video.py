import os
from cv2 import resize, CAP_PROP_FPS, CAP_PROP_FRAME_WIDTH, CAP_PROP_FRAME_HEIGHT, CAP_PROP_POS_MSEC, VideoWriter_fourcc, VideoWriter, destroyAllWindows, waitKey, imencode
import mediapipe as mp
import numpy as np
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
from Frontend.calc.utils import get_distance, calc_blur, apply_blur, draw_landmarks_on_image, get_landmark_name
from Frontend.calc.svm import get_model
import multiprocessing
from queue import Queue
import tempfile

# CONFIG
IMG_FILTER_CLASS = ['MF']
IMG_TRAIN_SET = os.path.join('data', 'training','features_middlefinger.csv')
IMG_THREADS = 12
IMG_WIDTH = 320
DISABLE_OVERLAY = False
PARALLEL = False

class VideoCensor():

    def __init__(self):
        self.base_options = python.BaseOptions(model_asset_path=os.path.join('data', 'hand_landmarker.task'))
        self.options = vision.HandLandmarkerOptions(
            base_options=self.base_options,
            num_hands=2,
            running_mode=vision.RunningMode.VIDEO
        )
        self.detector = vision.HandLandmarker.create_from_options(self.options)
        self.model = get_model(IMG_TRAIN_SET)

    def display_image(self, ret, frame, ts, w, h):
        if not ret:
            return None
        scale = IMG_WIDTH/w
        frame = resize(frame, (int(w*scale), int(h*scale)))
        image = mp.Image(image_format=mp.ImageFormat.SRGB, data=frame)
        detection_result = self.detector.detect_for_video(image, ts)
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
                classes.append(self.model.predict([features])[0])
                if classes[hand] in IMG_FILTER_CLASS:
                    out_image = apply_blur(out_image, 
                        calc_blur(out_image, detection_result.hand_landmarks[hand])
                    )
            # Draw lines on hands + label
            if not DISABLE_OVERLAY: out_image = draw_landmarks_on_image(out_image, detection_result, text_override=classes)
        
        return out_image

    def calc_image(self, cap):
        frame_width = int(cap.get(CAP_PROP_FRAME_WIDTH))
        frame_height = int(cap.get(CAP_PROP_FRAME_HEIGHT))

        if PARALLEL:

            with multiprocessing.Pool(IMG_THREADS) as pool:
                results = Queue()
                i = 0
                lastTs = -1
                while True:
                    ret, frame = cap.read()
                    ts = int(cap.get(CAP_PROP_POS_MSEC))
                    if ts > lastTs:
                        lastTs = ts
                        results.put(pool.apply_async(self.display_image, [ret, frame, int(ts), frame_width, frame_height]))

                    if results.qsize() > IMG_THREADS or ts == 0:
                        image = results.get().get()
                        if image is None: break
                        #output.write(image)
                        ret, jpeg = imencode('.jpg', image)
                        yield (b'--frame\r\n'
                            b'Content-Type: image/jpeg\r\n\r\n' + jpeg.tobytes() + b'\r\n\r\n')
                        print(f"Completed frame: {i}")
                        #waitKey(1)
                    
                    print(f"Completed frame: {i}")
                    i+=1
        else:
            i = 0
            lastTs = -1
            while True:
                ret, frame = cap.read()
                ts = int(cap.get(CAP_PROP_POS_MSEC))
                if ts > lastTs:
                    lastTs = ts
                    image = self.display_image(ret, frame, int(ts), frame_width, frame_height)
                    if image is None: break
                else: break
                #output.write(image)
                ret, jpeg = imencode('.jpg', image)
                yield (b'--frame\r\n'
                    b'Content-Type: image/jpeg\r\n\r\n' + jpeg.tobytes() + b'\r\n\r\n')
                print(f"Completed frame: {i}")
                #waitKey(1)
                i += 1

        cap.release()
        destroyAllWindows()