#@markdown We implemented some functions to visualize the hand landmark detection results. <br/> Run the following cell to activate the functions.

from mediapipe import solutions
from mediapipe.framework.formats import landmark_pb2
from math import sqrt
import numpy as np
import cv2

MARGIN = 10  # pixels
FONT_SIZE = 1
FONT_THICKNESS = 1
HANDEDNESS_TEXT_COLOR = (88, 205, 54) # vibrant green

LANDMARK_LOOKUP = [
  'WRIST',

  'THUMB_CMC',
  'THUMB_MCP',
  'THUMB_IP',
  'THUMB_TIP',

  'INDEX_FINGER_MCP',
  'INDEX_FINGER_PIP',
  'INDEX_FINGER_DIP',
  'INDEX_FINGER_TIP',

  'MIDDLE_FINGER_MCP',
  'MIDDLE_FINGER_PIP',
  'MIDDLE_FINGER_DIP',
  'MIDDLE_FINGER_TIP',

  'RING_FINGER_MCP',
  'RING_FINGER_PIP',
  'RING_FINGER_DIP',
  'RING_FINGER_TIP',

  'PINKY_FINGER_MCP',
  'PINKY_FINGER_PIP',
  'PINKY_FINGER_DIP',
  'PINKY_FINGER_TIP',
]

def calc_blur(image, data):
    if len(data)<1: return None
    landmarks = data[0]
    xlen = len(image)
    ylen = len(image[0])
    c = [(v.x, v.y) for v in landmarks]
    maxs = np.amax(np.array(c), axis=0)
    mins = np.amin(np.array(c), axis=0)

    min_pix = [int(max(xlen*mins[1]-xlen//10, 0)), int(max(ylen*mins[0]-ylen//10, 0))]
    max_pix = [int(min(xlen*maxs[1]+xlen//10, ylen)), int(min(ylen*maxs[0]+ylen//10, ylen))]

    blur = cv2.blur(image, (100, 100), 5)

    from scipy.stats import kde

    landmarks = data[0]
    x = [v.x for v in landmarks]
    y = [v.y for v in landmarks]
    k = kde.gaussian_kde([x, y])
    xi, yi = np.mgrid[0:1:xlen//5*1j, 0:1:ylen//5*1j]
    zi = k(np.vstack([yi.flatten(), xi.flatten()]))

    scores = np.greater(zi.reshape(xi.shape), 1.5)

    return blur, scores, min_pix, max_pix

def apply_blur(image, blurData):
    blur, scores, min_pix, max_pix = blurData
    for x in range(min_pix[0], max_pix[0]):
        for y in range(min_pix[1], max_pix[1]):
            if scores[x//5][y//5]>0:
                image[x,y] = blur[x,y]

    return image

def get_distance(data, name1, name2):
  if len(data)<1: return None
  landmarks = data[0]
  idx1 = get_landmark_index(name1)
  idx2 = get_landmark_index(name2)
  coords1 = [landmarks[idx1].x, landmarks[idx1].y, landmarks[idx1].z]
  coords2 = [landmarks[idx2].x, landmarks[idx2].y, landmarks[idx2].z]

  return sqrt((coords1[0] - coords2[0])**2 + \
        (coords1[1] - coords2[1])**2 + \
        (coords1[2] - coords2[2])**2)

def get_landmark_name(index):
  return LANDMARK_LOOKUP[index]

def get_landmark_index(name):
  for i in range(0, len(LANDMARK_LOOKUP)):
    if LANDMARK_LOOKUP[i] == name: return i
  return -1

def draw_landmarks_on_image(rgb_image, detection_result, text_override=None):
  hand_landmarks_list = detection_result.hand_landmarks
  handedness_list = detection_result.handedness
  annotated_image = np.copy(rgb_image)

  # Loop through the detected hands to visualize.
  for idx in range(len(hand_landmarks_list)):
    hand_landmarks = hand_landmarks_list[idx]
    handedness = handedness_list[idx]

    # Draw the hand landmarks.
    hand_landmarks_proto = landmark_pb2.NormalizedLandmarkList()
    hand_landmarks_proto.landmark.extend([
      landmark_pb2.NormalizedLandmark(x=landmark.x, y=landmark.y, z=landmark.z) for landmark in hand_landmarks
    ])
    solutions.drawing_utils.draw_landmarks(
      annotated_image,
      hand_landmarks_proto,
      solutions.hands.HAND_CONNECTIONS,
      solutions.drawing_styles.get_default_hand_landmarks_style(),
      solutions.drawing_styles.get_default_hand_connections_style())

    # Get the top left corner of the detected hand's bounding box.
    height, width, _ = annotated_image.shape
    x_coordinates = [landmark.x for landmark in hand_landmarks]
    y_coordinates = [landmark.y for landmark in hand_landmarks]
    text_x = int(min(x_coordinates) * width)
    text_y = int(min(y_coordinates) * height) - MARGIN

    # Draw handedness (left or right hand) on the image.
    if text_override is not None:
        text = text_override
    else:
        text = f"{handedness[0].category_name}"
    cv2.putText(annotated_image, text,
                (text_x, text_y), cv2.FONT_HERSHEY_DUPLEX,
                FONT_SIZE, HANDEDNESS_TEXT_COLOR, FONT_THICKNESS, cv2.LINE_AA)

  return annotated_image