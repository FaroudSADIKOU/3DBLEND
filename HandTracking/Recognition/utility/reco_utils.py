"""
"""
import numpy as np
from sklearn import preprocessing

def euclidian_distance(point_a, point_b):
    """ Compute Euclidean distance between two points.
    """
    return np.linalg.norm(point_a - point_b) 

def build_X_based_on_fingertips_distance(X):
    n = X.shape[0]
    fingertips_based_X = []
    
    new_observation = []
    for finger_tips_index in range(6, n, 3):
        new_observation = np.append(
            new_observation,
            [
                euclidian_distance(
                    X[finger_tips_index: finger_tips_index+3], 
                    X[next_finger_tips_index: next_finger_tips_index+3]
                ) for next_finger_tips_index in range(finger_tips_index+3, n, 3)
            ]
        )
    fingertips_based_X.append(new_observation)
    return np.asarray(fingertips_based_X)
