# %% imports
import os, sys, inspect
import time
import numpy as np
import pickle
import csv

src_dir = os.path.dirname(os.path.realpath(__file__))
lib_dir = os.path.abspath(os.path.join(src_dir, "../LeapMotionLibForPython/LeapMotionPython3.7.7/lib/"))
reco_dir = os.path.abspath(os.path.join(src_dir, "Recognition/"))
sys.path.insert(0, lib_dir)
sys.path.append(reco_dir)

import time
from utility import reco_utils
import Leap
from Leap import Finger, Bone

COLUMNS_DICT = {
    "palm_x": 0, "palm_y": 1, "palm_z": 2, "normal_x": 3, "normal_y": 4, "normal_z": 5,
    "thumb_x": 6, "thumb_y": 7, "thumb_z": 8, "index_x": 9, "index_y": 10, "index_z": 11,
    "middle_x": 12, "middle_y": 13, "middle_z": 14, "ring_x": 15 , "ring_y": 16, "ring_z": 17,
    "pinky_x": 18, "pinky_y": 19, "pinky_z": 20
}
FINGERS_TYPES = [Finger.TYPE_THUMB, Finger.TYPE_INDEX, Finger.TYPE_MIDDLE, Finger.TYPE_RING, Finger.TYPE_PINKY ]
NB_FRAME = 100
# %%

controller = Leap.Controller()

user_name = "USER"
data_dir = None # to be set up later
# list of hand postures
list_postures_name = ["A", "B", "1", "2", "4", "v", "O", "ROCK"]

def prepare_directory(user_name):
    """ Creates a directory with he user name.
    The collected data as csv file will be stored in the created directory
    """
    global data_dir
    data_dir = os.path.abspath(os.path.join(reco_dir, f'dataset/{user_name}'))
    try:
        os.mkdir(data_dir)
    except OSError:
        print (f'Creation of the directory {data_dir} failed')
    else:
        print (f'Successfully created the directory {data_dir}')


def prepare_file(posture_name: str):
    """ Creates a csv file for data of a particular posture.
    For example 'd.csv' with d the [posture_name].
    """
    file_name = os.path.abspath(os.path.join(data_dir, f'{posture_name}.csv'))
    with open(file_name, 'w+', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(COLUMNS_DICT.keys())


def collect(posture_name):
    """ Principal function for data collection.
    """
    #print("Inside collect")
    file_name = os.path.abspath(os.path.join(data_dir, f'{posture_name}.csv'))
    for i in range(NB_FRAME):
        frame = controller.frame()
        if frame.is_valid:
            # get right hand
            hands = frame.hands
            for hand in hands:
                # for simplicity do right hand stuff
                if hand.is_right:
                    print("R  I  G  H  T")
                    # get fingers data
                    X = get_features_vector(hand)
                    # write X to file
                    with open(file_name, 'a', newline='') as file:
                        writer = csv.writer(file)
                        writer.writerow(X)
                else:
                    print("LEFT HAND")
        # after one itteration, wait 30S
        time.sleep(1/15)
# end collect

def get_features_vector(hand):
    """ Retrieves needed skeletal data from a Hand object.
    """
    #print("Inside get features")
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
    
    #print("TEST\n", len(X))
    return X
# end get_features_vector


def countdown_step():
    """ A countdown funcion: counting from 5 to 0.
    Used to give time to user to change hand posture.
    """
    for i in range(5):
        time.sleep(1)
        print(5 - i)
    time.sleep(1)
    print("GO")
# end countdown_step

def main():
    """ Main script to manage all the collect proccess.
    """
    user_name = input("Entrez votre Prénom:\n>");
    # create folder for all the users data
    prepare_directory(user_name)
    for posture_name in list_postures_name[:1]:
        # create a file for that posture
        prepare_file(posture_name)

        print(f'Faites le geste {posture_name} dans :')
        countdown_step()
        # collect now
        collect(posture_name)
        # wait 2 secondes after one posture time to change posture
        time.sleep(2)
    

if __name__ == '__main__':
    main()

