#!/usr/bin/python

"""
Apply an RDF to a case.
arg1: the decision forest file
arg2: the case folder holding the feature files
arg3: the cases mask file
arg4: the target segmentation file
"""

import os
import sys
import pickle
import numpy

from scipy.ndimage.morphology import binary_fill_holes, binary_dilation
from scipy.ndimage.measurements import label

from medpy.io import load, save
from medpy.features.utilities import join

# constants
n_jobs = 6

def main():
	# catch parameters
	forest_file = sys.argv[1]
	case_folder = sys.argv[2]
	mask_file = sys.argv[3]
	segmentation_file = sys.argv[4]

        # loading case features
	feature_vector = []
	for _file in os.listdir(case_folder):
		if _file.endswith('.npy') and _file.startswith('feature.'):
			with open(os.path.join(case_folder, _file), 'r') as f:
				feature_vector.append(numpy.load(f))
	feature_vector = join(*feature_vector)

	# load and apply the decision forest
	with open(forest_file, 'r') as f:
		forest = pickle.load(f)
	classification_results = forest.predict(feature_vector)

	# preparing  image
	m, h = load(mask_file)
    	m = m.astype(numpy.bool)
    	o = numpy.zeros(m.shape, numpy.uint8)
    	o[m] = numpy.squeeze(classification_results).ravel()

	# applying the post-processing morphology
	o = binary_dilation(o, iterations=2)
	o = keep_largest_connected_component(o)
	o = binary_fill_holes(o)

	# savin the results
    	save(o, segmentation_file, h, True)

def keep_largest_connected_component(img):
    labeled_array, num_features = label(img)
    largest_size = 0
    largest_idx = 0
    for idx in range(1, num_features + 1):
        size = numpy.count_nonzero(labeled_array == idx)
        if size > largest_size:
            largest_idx = idx
            largest_size = size
          
    out = numpy.zeros(img.shape, numpy.bool)  
    out[labeled_array == largest_idx] = True
    return out
    # Note: generate_binary_structure(2,2) also considers diagonal connectivity

if __name__ == "__main__":
	main()
