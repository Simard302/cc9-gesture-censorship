from sklearn.svm import SVC
from mediapipe_utils import featurize
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
import csv, os

def get_model():
    DIR = 'dataprep/data'

    csvFile = open(os.path.join(DIR, 'training','features.csv'), 'r')
    reader = csv.reader(csvFile)
    classification = []
    data = []
    for row in reader:
        if row[0] == 'Class': continue
        classification.append(str(row[0]))
        data.append([float(x) if x != 0 else 0 for x in row[1:]])

    model = SVC()

    model.fit(data, classification)

    return model


# base_options = python.BaseOptions(model_asset_path='dataprep/hand_landmarker.task')
# options = vision.HandLandmarkerOptions(base_options=base_options,
#                                         num_hands=2)
# detector = vision.HandLandmarker.create_from_options(options)

# TEST = ['3_hand.jpg', 'Z_hand.jpg']
# for jpg in TEST:
#     feature = featurize(os.path.join(DIR, 'test_data', jpg), detector)
#     feature = [float(x) if x != 0 else 0 for x in feature]
#     print(model.predict([feature]))

