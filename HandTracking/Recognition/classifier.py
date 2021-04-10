"""
"""

# %% imports

import os, sys, inspect
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler
from pickle import dump, load # for model persistence

from utility.utils import Utils
from utility.real_parser import TARGET_COL_NAME


# %%

src_dir = os.path.dirname(os.path.realpath(__file__))
MODEL_PATH_NAME = os.path.abspath(os.path.join(src_dir, "svm_model.pkl"))
MODEL2_PATH_NAME = os.path.abspath(os.path.join(src_dir, "random_forest.pkl"))
SCALER_PATH_NAME = os.path.abspath(os.path.join(src_dir, "scaler.pkl"))

MLP_MODEL_PATH_NAME = os.path.abspath(os.path.join(src_dir, "mlp_model.h5"))

# class name (Will be initiate later)
class_dict = {} 

# %% Utils functions

def euclidian_distance(point_a, point_b):
    """ Compute Euclidean distance between two points.
    """
    return np.linalg.norm(point_a - point_b) 

def build_class_dict(list_of_target):
    values = range(len(list_of_target))
    for index in values:
        class_dict[list_of_target[index]] = index

def build_numerical_labels(labels_as_str: list):
    classes_as_num = np.array(
        list(map(lambda x: class_dict[x], labels_as_str)),
        dtype=np.int32
    )
    return classes_as_num

def build_X_based_on_fingertips_distance(X):
    m, n = X.shape
    fingertips_based_X = []
    
    for frame_index in range(m):
        new_observation = []
        for finger_tips_index in range(6, n, 3):
            new_observation = np.append(
                new_observation,
                [
                    euclidian_distance(
                        X[frame_index, finger_tips_index: finger_tips_index+3], 
                        X[frame_index, next_finger_tips_index: next_finger_tips_index+3]
                    ) for next_finger_tips_index in range(finger_tips_index+3, n, 3)
                ]
            )
        fingertips_based_X.append(new_observation)
    return np.asarray(fingertips_based_X)


def classif_report(classifier, x_test, y_test, y_true):
    print(
        f'Classification report for classifier {classifier}:\n\
        {metrics.classification_report(y_test, y_true, target_names=class_dict.keys(), digits=4)}\n'
    )

    disp = metrics.plot_confusion_matrix(
        classifier, 
        x_test, y_test,
        display_labels = class_dict.keys(),
        xticks_rotation = 'vertical'
    )
    disp.figure_.figsize = (25, 25)
    disp.figure_.suptitle("Confusion Matrix")
    # print(f'Confusion matrix:\n{disp.confusion_matrix}')
    plt.show()
    return disp.confusion_matrix

def train_model(classifier, X_train, X_test, y_train, y_test):
    # fit the training dataset on the classifier
    classifier.fit(X_train, y_train)
    # predict the labels on test dataset
    predictions = classifier.predict(X_test)
    # ask for confusion matrix
    confusion_matrix = classif_report(classifier, X_test, y_test, predictions)
    return metrics.accuracy_score(predictions, y_test), confusion_matrix
# end train_model


# %% load data

reco_utils = Utils()
raw_data = reco_utils.load_data()

# %% clean data
raw_data = raw_data.dropna().reset_index(drop=True)

print(f'Raw data shape: {raw_data.shape} ')
raw_data.head()

# %% Features generation 

build_class_dict(pd.unique(raw_data.iloc[:, -1]))
print(class_dict)

y = build_numerical_labels(raw_data.iloc[:, -1])
X = raw_data.drop(columns=TARGET_COL_NAME).values
X = build_X_based_on_fingertips_distance(X)

print(f'X shape: {X.shape}\ny shape: {y.shape}')

print(X[0])

# %% Data preprocessing

from sklearn import preprocessing, metrics
from sklearn.model_selection import train_test_split
from sklearn import svm
#from sklearn.metrics import precision_score, recall_score, f1_score, confusion_matrix
from sklearn.metrics import classification_report, confusion_matrix

# split data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=42)
print(X_train[0])
# define scaler
scaler = MinMaxScaler()
# fit scaler on the training dataset
scaler.fit(X_train)
# transform both datasets
X_train_scaled = scaler.transform(X_train)
X_test_scaled = scaler.transform(X_test)
print(X_train[0])
# save the scaler
dump(scaler, open(SCALER_PATH_NAME, 'wb'))

# %% models creation and training

# SVM
svm_model = svm.SVC(kernel='linear')
svm_accuracy, svm_conf_mat = train_model(
    svm_model,
    X_train_scaled, X_test_scaled, 
    y_train, y_test
)
print(f'SVM Accuracy: {svm_accuracy}')

#Random Forest
# %%
from sklearn.ensemble import RandomForestClassifier
random_forest_model = RandomForestClassifier(max_depth=None, random_state=0, criterion='entropy')
rf_accuracy, _ = train_model(
    random_forest_model,
    X_train_scaled, X_test_scaled, 
    y_train, y_test
)
print(f'RF Accuracy: {rf_accuracy}')

# %% model persistance

# SVM model saving
dump(svm_model, open(MODEL_PATH_NAME, 'wb'))
# Random forest model saving
dump(random_forest_model, open(MODEL2_PATH_NAME, 'wb'))
        

# %% Neural network

# import tensorflow as tf
# from tensorflow import keras
# from tensorflow.keras import initializers
# from tensorflow.keras.layers import Dense
# from tensorflow.keras.optimizers import Adam, Adamax

# from tensorflow.keras.utils import to_categorical
# one_hot_label = to_categorical(y_train)

# input_dim = X_train.shape[1]  # Number of features
# nb_label = 8

# initializer_1 = initializers.RandomNormal(stddev=0.01)

# model = keras.Sequential(
#     [
#         Dense(512, input_shape=(input_dim,), activation='relu', kernel_initializer=initializer_1),
#         Dense(256, activation="relu"),
#         Dense(128, activation="relu"),
#         Dense(nb_label, activation="softmax", name="outputlayer")
#     ]
# )

# # model compilation
# model.compile(
#     optimizer=Adam(),
#     loss=keras.losses.CategoricalCrossentropy(),
#     metrics=['accuracy']
# )
# #model.summary()

# #%%

# # custom callback to monitor the  accuracy on validation data
# class StopOnCallback(keras.callbacks.Callback):
    
#     def __init__(self, accs_, max_loss_):
#         super(StopOnCallback, self).__init__()
#         self.accs = accs_
#         self.max_loss = max_loss_

#     def on_epoch_end(self, epoch, logs=None): 
#         accuracy = logs["accuracy"]
#         val_accuracy = logs["val_accuracy"]
#         loss = logs["loss"]
#         if val_accuracy >= self.accs and accuracy >= self.accs and loss <= self.max_loss:
#             self.model.stop_training = True

# # %%

# # check_perf_callback=StopOnCallback(1.00, 2.0e-05)
# # lr_callback = keras.callbacks.ReduceLROnPlateau(monitor='val_loss', patience=5, factor=0.1)

# EPOCH = 100; BATCH_SIZE = 32


# history = model.fit(
#     X_train_scaled, 
#     one_hot_label, 
#     batch_size=BATCH_SIZE, epochs=EPOCH,
#     validation_split=0.15,
# )


# test_loss, test_accuracy = model.evaluate(X_test_scaled, to_categorical(y_test), verbose=False)
# print('Accuracy on test dataset:', test_accuracy)

# # save model 
# model.save(MLP_MODEL_PATH_NAME)

# %% Evaluating the ability to generalize of our models
from sklearn.model_selection import cross_val_score

svm_scores = cross_val_score(svm_model, X_train_scaled, y_train, cv=5)
print(f'SVM: Accuracy of {svm_scores.mean()} with a standard deviation of {svm_scores.std()}')

rf_scores = cross_val_score(random_forest_model, X_train_scaled, y_train, cv=5)
print(f'RF: Accuracy of {rf_scores.mean()} with a standard deviation of {rf_scores.std()}')