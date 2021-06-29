# -*- coding: utf-8 -*-
"""
Created on Wed Mar  3 12:29:43 2021

@author: edelirio
"""

from skimage import feature
import numpy as np

class LocalBinaryPatterns:
	'''
	This class process the local binary pattern for an images
	and returns the corresponding histogram.

	'''
	def __init__(self, num_points, radius):
		# get the number of points and radius
		self.numPoints = num_points
		self.radius = radius
		
	def get_lbp(self, image, eps=1e-7):
		# compute the Local Binary Pattern
		# of the image, and then use the LBP representation
		# to build the corresponding histogram
		lbp = feature.local_binary_pattern(image, self.numPoints,
			self.radius, method="uniform")
		(hist, _) = np.histogram(lbp.ravel(),
			bins=np.arange(0, self.numPoints + 3),
			range=(0, self.numPoints + 2))
		# normalize the histogram
		hist = hist.astype("float")
		hist /= (hist.sum() + eps)
		# return the histogram of Local Binary Patterns
		return hist