#!/usr/bin/python

"""
Extract selected features from an image and save them under a fixed file name structure.
As first argument, supply the source folder with the image channels, as second the mask image and as third the target folder.
Note: Does not overwrite existing feature files.
"""

import os
import sys
import numpy
import itertools

from medpy.io import load, header
from medpy.features.intensity import intensities, centerdistance, centerdistance_xdminus1, local_mean_gauss, local_histogram, hemispheric_difference, median, guassian_gradient_magnitude
from medpy.features.intensity import indices as indices_feature

trg_dtype = numpy.float32
features_to_extract = [
	('flair_tra', intensities, [], False),
	('flair_tra', local_mean_gauss, [3], True),
	('flair_tra', local_mean_gauss, [5], True),
	('flair_tra', local_mean_gauss, [7], True),
	('flair_tra', guassian_gradient_magnitude, [5], True),
	('flair_tra', median, [7], True),
	('flair_tra', local_histogram, [11, 'image', (0, 100), 5, None, None, 'ignore', 0], False), #11 bins, 5*2=10mm region
	('flair_tra', local_histogram, [11, 'image', (0, 100), 10, None, None, 'ignore', 0], False), #11 bins, 10*2=20mm region
	('flair_tra', local_histogram, [11, 'image', (0, 100), 15, None, None, 'ignore', 0], False), #11 bins, 15*2=30mm region
	('flair_tra', centerdistance_xdminus1, [0], True),
	('flair_tra', centerdistance_xdminus1, [1], True),
	('flair_tra', centerdistance_xdminus1, [2], True)
]

def main():
	# loading the image mask
	m = load(sys.argv[2])[0].astype(numpy.bool)

	# extracting the required features and saving them
	for sequence, function_call, function_arguments, voxelspacing in features_to_extract:
		if not isfv(sys.argv[3], sequence, function_call, function_arguments):
			#print sequence, function_call.__name__, function_arguments
			i, h = load('{}/{}.nii.gz'.format(sys.argv[1], sequence))
			call_arguments = list(function_arguments)
			if voxelspacing: call_arguments.append(header.get_pixel_spacing(h))
			call_arguments.append(m)
			fv = function_call(i, *call_arguments)
			savefv(fv, sys.argv[3], sequence, function_call, function_arguments)

def savefv(fv, trgdir, seq, fcall, fargs):
	"""Saves the supplied feature vector under a fixed naming rule."""
	name = 'feature.{}.{}.{}'.format(seq, fcall.func_name, '_'.join(['arg{}'.format(i) for i in fargs]))
	with open('{}/{}.npy'.format(trgdir, name), 'wb') as f:
		numpy.save(f, fv.astype(trg_dtype))

def isfv(trgdir, seq, fcall, fargs):
	name = 'feature.{}.{}.{}'.format(seq, fcall.func_name, '_'.join(['arg{}'.format(i) for i in fargs]))
	return os.path.exists('{}/{}.npy'.format(trgdir, name))

if __name__ == "__main__":
	main()



