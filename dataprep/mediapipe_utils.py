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