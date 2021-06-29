import pickle
import matplotlib.pyplot as plt
from skimage import io
from skimage.color import rgb2gray
import os
from PIL import Image
from PIL import ImageFile

import config.config as cnf
from local_binary_patterns.local_binary_pattern import LocalBinaryPatterns

config = cnf.Config()
MODEL_RELATIVE_PATH = config.relative_model_path

def predict_image(img_path):
    module_name = "predict_image"

    try:
        #load the Local Binary Pattern class
        lbp = LocalBinaryPatterns(14, 5)

        #get the project root path
        project_root = os.path.dirname(os.path.dirname(__file__))
        model_pickle_path = os.path.join(project_root, MODEL_RELATIVE_PATH)
        print(model_pickle_path)
        
        #load existing model
        with open(model_pickle_path, 'rb') as handle:
            calibrated_svc_2 = pickle.load(handle)

        image = plt.imread(img_path)
        #image = rgb2gray(io.imread(img_path))
        gray = rgb2gray(image)

        hist = lbp.get_lbp(gray)
        prediction = calibrated_svc_2.predict(hist.reshape(1, -1))
        predicted_probs = calibrated_svc_2.predict_proba(hist.reshape(1, -1))  #important to use predict_proba
        confidence = max(predicted_probs[0,0], predicted_probs[0,1])
        print("This image most likely belongs to {0} with a {1} percent confidence.".format(prediction[0], confidence))
        
        return prediction[0], confidence
    except Exception as ex:
        error_text = "Error in: {0}. Exception {1}".format(module_name, ex)
        raise Exception(error_text)
