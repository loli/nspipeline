#!/usr/bin/python

"""
Extract selected features from an image and save them under a fixed file name structure.
As first argument, supply the source folder with the image channels, as second the mask image and as third the target folder.
"""

import os
import sys
import numpy
import itertools

from medpy.io import load, header
from medpy.features.intensity import intensities, centerdistance, centerdistance_xdminus1, local_mean_gauss, local_histogram
from medpy.features.intensity import indices as indices_feature

trg_dtype = numpy.float32
features_to_extract = [('t2_sag_tse', indices_feature, [], True),
	               ('flair_tra', local_mean_gauss, [9], True),
		       ('flair_tra', local_mean_gauss, [7], True),
		       ('flair_tra', local_mean_gauss, [5], True),
		       ('flair_tra', local_mean_gauss, [3], True),
	               ('dw_tra_b1000_dmean', local_mean_gauss, [9], True),
		       ('dw_tra_b1000_dmean', local_mean_gauss, [7], True),
		       ('dw_tra_b1000_dmean', local_mean_gauss, [5], True),
		       ('dw_tra_b1000_dmean', local_mean_gauss, [3], True),
		       ('flair_tra', local_mean_gauss, [1], True),
		       ('t2_sag_tse', centerdistance_xdminus1, [2], True),
		       ('flair_tra', intensities, [], False),
		       ('t2_sag_tse', local_mean_gauss, [5], True),
	               ('adc_tra', local_mean_gauss, [9], True),
		       ('dw_tra_b1000_dmean', local_mean_gauss, [1], True),
		       ('t2_sag_tse', local_mean_gauss, [3], True),
		       ('t2_sag_tse', local_mean_gauss, [7], True),
		       ('dw_tra_b1000_dmean', intensities, [], False)]

def main():
	# loading the image mask
	m = load(sys.argv[2])[0].astype(numpy.bool)

	# extracting the required features and saving them
	for sequence, function_call, function_arguments, voxelspacing in features_to_extract:
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

if __name__ == "__main__":
	main()



