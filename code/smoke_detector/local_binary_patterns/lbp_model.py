# -*- coding: utf-8 -*-
"""
Created on Wed Mar  3 11:56:05 2021

@author: edelirio
"""

from smoke_detection_algorithm.local_binary_patterns.local_binary_pattern import LocalBinaryPatterns

#import argparse
import matplotlib.pyplot as plt
from skimage.color import rgb2gray
from imutils import paths
from sklearn.svm import LinearSVC
import os

# PARAMETERS FOR THE LOCAL BINARY PATTERN ALGORITHM
radius = 5
n_points = 14

project_root = os.path.dirname(os.path.dirname(__file__))

##############################################################
# MODEL AND PREDICTION #

# store all the images
datas = []
# store the corresponding label
labels = []

lbp = LocalBinaryPatterns(14, 5)

# PROCESS THE LBP FOR EACH IMAGE
# loop over the training images (folder images\training\)
for image_path in paths.list_images(project_root + '/local_binary_patterns/images/training'):
	# load the image, convert it to grayscale, and describe it
    image = plt.imread(image_path)
    gray = rgb2gray(image)
    hist = lbp.get_lbp(gray)
	# extract the label from the image path, then update the
	# label and data lists
    labels.append(image_path.split(os.path.sep)[-2])
    datas.append(hist)
    
######################################################
# TRAIN MODEL Linear SVM on the data
model = LinearSVC(C=100.0, random_state=42, max_iter=5000)

#from sklearn.preprocessing import StandardScaler
from sklearn.calibration import CalibratedClassifierCV

# This is the calibrated classifier which can give probabilistic classifier
calibrated_svc = CalibratedClassifierCV(model,
                                        method='sigmoid',  #sigmoid will use Platt's scaling. Refer to documentation for other methods.
                                        cv=3) 

calibrated_svc.fit(datas, labels)

# save the trained model
import pickle
#with open(project_root + 'local_binary_patterns/model/model.pickle', 'wb') as handle:
#    pickle.dump(calibrated_svc, handle, protocol=pickle.HIGHEST_PROTOCOL)
    
#model.fit(datas, labels)

######################################################
# VALIDATE MODEL
correct = 0
total = 0

# loop over the testing images (folder images\testing\)
for image_path in paths.list_images(project_root + '/localBinaryPatterns/images/testing'):
	# load the image, convert it to grayscale, describe it,
	# and classify it
    image = plt.imread(image_path)
    gray = rgb2gray(image)
    hist = lbp.get_lbp(gray)
    prediction = calibrated_svc.predict(hist.reshape(1, -1))
    total += 1
    
    # identify the correct predictions to calculate the accuracy
    if (str(prediction[0]) == (str(image_path.split(os.path.sep)[-2]))):
        correct += 1

print("Accuracy: "+ str((correct/total)*100))