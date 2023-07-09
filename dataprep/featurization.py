import os
import csv
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
from mediapipe_utils import get_landmark_name, featurize

DIR = 'dataprep/data'

base_options = python.BaseOptions(model_asset_path='dataprep/hand_landmarker.task')
options = vision.HandLandmarkerOptions(base_options=base_options,
                                        num_hands=2)
detector = vision.HandLandmarker.create_from_options(options)

csvFile = open(os.path.join(DIR, 'training','features_test.csv'), 'w', newline='')
writer = csv.writer(csvFile)
writer.writerow(['Class']+['DIST_'+get_landmark_name(i)+'-'+get_landmark_name(k)for k in range(0, 21) for i in range(0, 21)])

images_middlefinger = os.listdir(os.path.join(DIR, 'middle-finger-dataset'))

for jpg in images_middlefinger:
    classification = 'MF'
    print(jpg)
    
    features = featurize(os.path.join(DIR, 'middle-finger-dataset', jpg), detector)
    if features is not None: writer.writerow([classification] + features); print('good')

images_original = os.listdir(os.path.join(DIR, 'original_images'))

for jpg in images_original:
    classification = 'N'
    print(jpg)
    
    features = featurize(os.path.join(DIR, 'original_images', jpg), detector)
    if features is not None: writer.writerow([classification] + features)

csvFile.close()

