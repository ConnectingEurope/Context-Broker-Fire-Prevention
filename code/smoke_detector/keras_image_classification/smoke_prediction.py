# -*- coding: utf-8 -*-
"""
Created on Tue Mar 16 10:01:40 2021

@author: edelirio
"""
import tensorflow as tf

from tensorflow import keras
import numpy as np
import os

img_height = 180
img_width = 400

class_names = ['neutral', 'smoke']
project_root = os.path.dirname(os.path.dirname(__file__))

#load trained model
reconstructed_model = keras.models.load_model(project_root + '/keras_image_classification/model')
reconstructed_model.summary()

def predict_image(image_path):

    img = keras.preprocessing.image.load_img(
        image_path, target_size=(img_height, img_width)
    )
    img_array = keras.preprocessing.image.img_to_array(img)
    img_array = tf.expand_dims(img_array, 0) # Create a batch
    
    predictions = reconstructed_model.predict(img_array)
    score = tf.nn.softmax(predictions[0])
    
    print("This image most likely belongs to {} with a {:.2f} percent confidence.".format(class_names[np.argmax(score)], 100 * np.max(score)))
    
    return (class_names[np.argmax(score)],100 * np.max(score))

folder_path = project_root + '/predict_images/'
results= []

for filename in os.listdir(folder_path):   
    print(filename)
    pred_result = predict_image(folder_path + filename)
    results.append(pred_result)
    
print(results)