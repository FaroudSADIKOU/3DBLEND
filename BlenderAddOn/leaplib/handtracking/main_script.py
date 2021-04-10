""" Main script to manage the framework.
Made of two different thread: one for the frontend and the other one for the backend.
The backend end made of the recognition module keep track of 
data sent by the LMC. Every time necessary, it triggers events 
corresponding to the new detected state (via a stage machine/controller).
Knowing that once the frontend is launched, it listen to keyboard events. 
It catch those events emited by the backend and process it accordingly.
"""

# %% imports packages

from __future__ import annotations

import os, sys, inspect
import time
from joblib import load
import pickle
import time
import threading

# to controll keyboard
from pynput.keyboard import Key, Controller

from typing import List

src_dir = os.path.dirname(os.path.realpath(__file__))
lib_dir = os.path.abspath(os.path.join(src_dir, "../LeapMotionLibForPython/LeapMotionPython3.7.7/lib/"))
reco_dir = os.path.abspath(os.path.join(src_dir, "Recognition/"))
sys.path.insert(0, lib_dir)
sys.path.append(reco_dir)
sys.path.insert(0, os.path.abspath("C:/leaplib"))
import Leap
from Leap import Finger, Bone

from utility import reco_utils
import numpy as np

FINGERS_TYPES = [Finger.TYPE_THUMB, Finger.TYPE_INDEX, Finger.TYPE_MIDDLE, Finger.TYPE_RING, Finger.TYPE_PINKY ]

MODEL_PATH_NAME = os.path.abspath(os.path.join(reco_dir, "svm_model.pkl"))
MODEL2_PATH_NAME = os.path.abspath(os.path.join(reco_dir, "random_forest.pkl"))
SCALER_PATH_NAME = os.path.abspath(os.path.join(reco_dir, "scaler.pkl"))

# different class (hand postures)
TARGETS_DICT = {
    0: '1', 1: '2', 2: '4', 3: 'A', 4: 'B', 5: 'O', 6: 'R', 7: 'V'
}

# %%
# first load the necessary objects

def load_model():
    """ load classifier
    """
    with open(MODEL2_PATH_NAME, 'rb') as file:
        pickled_model = pickle.load(file)
    return pickled_model

def load_scaler():
    with open(SCALER_PATH_NAME, 'rb') as file:
        scaler = pickle.load(file)
    return scaler

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

def listen_for_half_a_seconds():
    temp_dict = {}
    cycle_end_time = time.time() + 1/2
    while time.time() < cycle_end_time: # this will run for 1/2 second
        frame = controller.frame()
        if frame.is_valid:
            # get right hand
            hands = frame.hands
            for hand in hands:
                # only take care of rigth hand
                if hand.is_right:
                    X = build_feautures_vector_from_hand(hand)
                    #print(f'Predicted class: {predict(X)}\n')
                    posture = predict(X)
                    temp_dict[posture] = temp_dict.get(posture, 0) + 1 
                else:
                    pass
                    #print("LEFT HAND")
                    #return {'VALIDATE': 1}
    return temp_dict

def validate(gesture_dict: dict):
    if(gesture_dict):
        max_key = max(gesture_dict, key=gesture_dict.get)
        prob = gesture_dict[max_key] / sum(gesture_dict.values())
        return max_key, prob
    else:
        return None, 0

# class defining a statemachine
class StateMachine():
    """
    Kind of state controller ...
    """
    def __init__(self):
        self._state: str = None
        self.last_state_time = None

    def notify(self) -> None:
        """
        Trigger a keyboard event.
        """
        # keyboard.press(self._state)
        # print(f"M A C H I N E  S E N T  {self._state}")
        print(self._state)
        sys.stdout.flush()
        self.last_state_time = time.time()
        
    def change_state(self, new_posture) -> None:
        """
        """
        if self._state != new_posture:
            self._state = new_posture
            self.notify()
        elif time.time() - self.last_state_time > 2:
            self._state = new_posture
            self.notify()

# %% main script start

# keyboard monitor
keyboard = Controller()
# have an instance of the controller
controller = Leap.Controller()
# load others
# load the model
model = load_model()
# load the scaler (for data preprocessing) 
scaler = load_scaler()
# create the object we all need to observe: it is an observable
state_machine = StateMachine()

# %% T H R E A D 1  :  F R O N T - E N D

"""
Start modals things, and keep listening to keyboard events.
"""
class FrontendThread(threading.Thread):
    def __init__(self, threadID, name, counter):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.counter = counter

    def run(self):
        # here you can put all you need for example:
        # Start the main Modal, and start listen for keyboard events.
        # Just make sure to keep the thread running
        while(True):
            pass


# %% T H R E A D 2  :  B A C K - E N D
#  BA
class BackendThread(threading.Thread):
    def __init__(self, threadID, name, counter):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.counter = counter
    
    def __inner_logic(self):
        while True:
            #print("F I R S T  C Y C L E ")
            gestures_dict = listen_for_half_a_seconds()
            # after the first cycle, we check for the stats
            max_key, prob = validate(gestures_dict)
            while(prob <= 0.60 and len(gestures_dict)<= 3):
                #print("A N O T H E R  C Y C L E  T O  B E  S U R E ")
                gestures_dict =  listen_for_half_a_seconds()
                # now merge both the 2 dict
                # TODO test the behavior when merge the previous and actual dict together
                max_key, prob = validate(gestures_dict)
            #print(f'Gesture {max_key} with prob: {prob}')
            # print(max_key)
            state_machine.change_state(max_key)            
    # end __inner_logic

    def run(self):
        self.__inner_logic()

# %% main script end

# Create frontend thread
#front = FrontendThread(1, "F R O N T E N D", 1)
#front.start()

# Create backend thread
back = BackendThread(2, "B A C K E N D", 2)
# Start the backend4V4V4A
back.start()