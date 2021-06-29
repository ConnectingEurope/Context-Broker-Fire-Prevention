# -*- coding: utf-8 -*-
"""
Created on Tue May 11 15:34:56 2021

@author: edelirio
"""

import cv2
import numpy as np

def detect_color(frame, count):
    res = {}
    
    img = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    boundaries = [
    	([36, 25, 25], [70, 255,255]),  #GREEN BOUNDARIES
    	([0, 74, 0], [28, 255, 255]) #ORANGE BOUNDARIES
    ]
    
    isfirst = True
    # loop over the boundaries
    for (lower, upper) in boundaries:
        # create NumPy arrays from the boundaries
        lower = np.array(lower, dtype = "uint8")
        upper = np.array(upper, dtype = "uint8")
        # find the colors within the specified boundaries and apply
        # the mask
        mask = cv2.inRange(img, lower, upper)
        #output = cv2.bitwise_and(img, img, mask = mask)
        ratio= cv2.countNonZero(mask)/(img.size/3)

        #cv2.imwrite(r'C:\Users\edelirio\Desktop\CBPilot\drytreesdetector\processed_frames\frame%d.jpg' % count, output)

        if isfirst:
            isfirst = False
            #print('green pixel percentage:', np.round(ratio*100, 2))
            res['greenPixels'] = np.round(ratio*100, 2)
        else:
            #print('dry pixel percentage:', np.round(ratio*100, 2))
            res['dryPixels'] = np.round(ratio*100, 2)
            
    return res

if __name__ == '__main__': 
    img_source = cv2.imread(r'C:\Users\edelirio\Desktop\CBPilot\drytreesdetector\dry_trees_detector\images\testing\frame63.jpg')
    
    #https://stackoverflow.com/questions/47483951/how-to-define-a-threshold-value-to-detect-only-green-colour-objects-in-an-image
    
    ## convert to hsv
    img = cv2.cvtColor(img_source, cv2.COLOR_BGR2HSV)
    
    #here we decide the boundaries of the colors to detect
    boundaries = [
    	([36, 25, 25], [70, 255,255]),  #GREEN BOUNDARIES
    	([0, 74, 0], [28, 255, 255]) #ORANGE BOUNDARIES
    ]
    
    isfirst = True
    # loop over the boundaries
    for (lower, upper) in boundaries:
        # create NumPy arrays from the boundaries
        lower = np.array(lower, dtype = "uint8")
        upper = np.array(upper, dtype = "uint8")
        # find the colors within the specified boundaries and apply
        # the mask
        mask = cv2.inRange(img, lower, upper)
        output = cv2.bitwise_and(img, img, mask = mask)
        ratio= cv2.countNonZero(mask)/(img.size/3)
        
        if isfirst:
            isfirst = False
            print('green pixel percentage:', np.round(ratio*100, 2))
        else:
            print('dry pixel percentage:', np.round(ratio*100, 2))

        # show the images
        cv2.imshow("images", np.hstack([img, output]))
        cv2.waitKey(0)
    
