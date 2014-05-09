#!/usr/bin/python

"""
Apply an RDF to a case.
arg1: the decision forest file
arg2: the case folder holding the feature files
arg3: the cases mask file
arg4: the target segmentation file
arg5: the target probability file
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
probability_threshold = 0.5

def main():
	# catch parameters
	forest_file = sys.argv[1]
	case_folder = sys.argv[2]
	mask_file = sys.argv[3]
	segmentation_file = sys.argv[4]
	probability_file = sys.argv[5]

        # loading case features
	feature_vector = []
	for _file in os.listdir(case_folder):
		if _file.endswith('.npy') and _file.startswith('feature.'):
			with open(os.path.join(case_folder, _file), 'r') as f:
				feature_vector.append(numpy.load(f))
	feature_vector = join(*feature_vector)
	if 1 == feature_vector.ndim:
		feature_vector = numpy.expand_dims(feature_vector, -1)

	# load and apply the decision forest
	with open(forest_file, 'r') as f:
		forest = pickle.load(f)
	probability_results = forest.predict_proba(feature_vector)[:,1]
	classification_results = probability_results > probability_threshold # equivalent to forest.predict

	# preparing  image
	m, h = load(mask_file)
    	m = m.astype(numpy.bool)
    	oc = numpy.zeros(m.shape, numpy.uint8)
	op = numpy.zeros(m.shape, numpy.float32)
    	oc[m] = numpy.squeeze(classification_results).ravel()
	op[m] = numpy.squeeze(probability_results).ravel()

	# applying the post-processing morphology
	oc = binary_fill_holes(oc)

	# saving the results
    	save(oc, segmentation_file, h, True)
    	save(op, probability_file, h, True)

if __name__ == "__main__":
	main()
