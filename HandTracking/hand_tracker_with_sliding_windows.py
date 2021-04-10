# %% imports

import os, sys, inspect
import time
import numpy as np
from joblib import load
import pickle
import time

src_dir = os.path.dirname(os.path.realpath(__file__))
lib_dir = os.path.abspath(os.path.join(src_dir, "../LeapMotionLibForPython/LeapMotionPython3.7.7/lib/"))
reco_dir = os.path.abspath(os.path.join(src_dir, "Recognition/"))
sys.path.insert(0, lib_dir)
sys.path.append(reco_dir)

from utility import reco_utils
import Leap
from Leap import Finger, Bone

FINGERS_TYPES = [Finger.TYPE_THUMB, Finger.TYPE_INDEX, Finger.TYPE_MIDDLE, Finger.TYPE_RING, Finger.TYPE_PINKY ]

MODEL_PATH_NAME = os.path.abspath(os.path.join(reco_dir, "svm_model.pkl"))
MODEL2_PATH_NAME = os.path.abspath(os.path.join(reco_dir, "random_forest.pkl"))
SCALER_PATH_NAME = os.path.abspath(os.path.join(reco_dir, "scaler.pkl"))


# different class (hand postures)
TARGETS_DICT = {
    0: '1', 1: '2', 2: '4', 3: 'A', 4: 'B', 5: 'O', 6: 'ROCK', 7: 'V'
}

# %%
# first load the necessary objects

def load_model():
    """ load classifier
    """
    with open(MODEL_PATH_NAME, 'rb') as file:
        pickled_model = pickle.load(file)
    return pickled_model

def load_scaler():
    with open(SCALER_PATH_NAME, 'rb') as file:
        scaler = pickle.load(file)
    return scaler

# load the model
model = load_model()
# load the scaler (for data preprocessing) 
scaler = load_scaler()
# have an instance of the controller
controller = Leap.Controller()
# %%

def build_feautures_vector_from_hand(hand):
    X = []
    # get all fingers tips position
    palm_position = hand.palm_position
    palm_normal = hand.palm_normal
    X.extend([
        palm_position.x, palm_position.y, palm_position.z,
        palm_normal.x, palm_normal.y, palm_normal.z
    ])
    for finger_type in FINGERS_TYPES:
        finger = hand.fingers.finger_type(finger_type)[0]
        finger_tip = finger.bone(Bone.TYPE_DISTAL).next_joint
        X.extend([finger_tip.x, finger_tip.y, finger_tip.z])
    X = reco_utils.build_X_based_on_fingertips_distance(np.array(X))
    X = scaler.transform(X)
    return X

def predict(X):
    return TARGETS_DICT[
        model.predict(X)[0]
    ] 

def listen_for_thirteen_seconds():
    temp_dict = {}
    cycle_end_time = time.time() + 1/2
    while time.time() < cycle_end_time: # this will run for 2 second
        frame = controller.frame()
        if frame.is_valid:
            # get right hand
            hands = frame.hands
            for hand in hands:
                # for simplicity do right hand stuff
                if hand.is_right:
                    X = build_feautures_vector_from_hand(hand)
                    #print(f'Predicted class: {predict(X)}\n')
                    posture = predict(X)
                    temp_dict[posture] = temp_dict.get(posture, 0) + 1 
                else:
                    print("LEFT HAND")
    return temp_dict

def validate(gesture_dict: dict):
    if(gesture_dict):
        max_key = max(gesture_dict, key=gesture_dict.get)
        prob = gesture_dict[max_key] / sum(gesture_dict.values())
        return max_key, prob
    else:
        return None, 0
    
# %% main script 

# TODO this is an infinite loop
for i in range(20):
    #print("F I R S T  C Y C L E ")
    gestures_dict = listen_for_thirteen_seconds()
    # after the first cycle, we check for the stats
    max_key, prob = validate(gestures_dict)
    while(prob <= 0.60 and len(gestures_dict)<= 3):
        #print("A N O T H E R  C Y C L E  T O  B E  S U R E ")
        gestures_dict =  listen_for_thirteen_seconds()
        # now merge both the 2 dict
        # TODO test the behavior when merge the previous and actual dict together
        max_key, prob = validate(gestures_dict)
    #print(f'Gesture {max_key} with prob: {prob}')
    print(max_key)

# %%
