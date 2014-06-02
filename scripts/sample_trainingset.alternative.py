#!/usr/bin/python

"""
Sample a traning set for a case by drawing from all other images using stratified random sampling.

arg1: directory with case-folders containing feature files
arg2: directory containing segmentations
arg3: directory containing brain masks
arg4: target directory
arg5: file containing a struct identifying the features to sample
arg6: number of samples to draw OR a file which contains a set of indices identifying the samples to draw
arg7+: indices of all cases from which to draw the training sample
"""

import os
import sys
import imp
import numpy
import itertools

from medpy.io import load
from medpy.features.utilities import append, join
from sklearn.cross_validation import StratifiedShuffleSplit

# main settings
min_no_of_samples_per_class_and_case = 4

# debug settings
verboose = False
debug = False
override = False # activate override (will signal a warning)

# constants
trainingset_features_file = 'trainingset.features.npy'
trainingset_classes_file = 'trainingset.classes.npy'
trainingset_feature_names_file = 'trainingset.fnames.npy'
trainingset_sample_indices_file = 'trainingset.indices.npy'
trainingset_suffix = 'npy'

def main():
	# catch arguments
	src_dir = sys.argv[1]
	seg_dir = sys.argv[2]
	msk_dir = sys.argv[3]
	trg_dir = sys.argv[4]
	feature_cnf_file = sys.argv[5]
	n_samples = int(sys.argv[6])
	cases = sys.argv[7:]

	# load features to use and create proper names from them
	features_to_use = load_feature_names(feature_cnf_file)

	# warn if target sample set already exists
	if os.path.isfile('{}/{}.{}'.format(trg_dir, trainingset_features_file, trainingset_suffix)) or
	   os.path.isfile('{}/{}.{}'.format(trg_dir, trainingset_classes_file, trainingset_suffix)) or
	   os.path.isfile('{}/{}.{}'.format(trg_dir, trainingset_feature_names_file, trainingset_suffix)) or
	   os.path.isfile('{}/{}.{}'.format(trg_dir, trainingset_sample_indices_file, trainingset_suffix)):
		if override:
			print 'WARNING: The target directory {}/ already contains at least on of the files to create. Replacing.'.format(trg_dir)
		else:
			print 'WARNING: The target directory {}/ already contains at least on of the files to create. Skipping.'.format(trg_dir)
			sys.exit(1)

	# initializing collections
	training_set_selections = dict.fromkeys(training_set_cases)

	# iterate over cases, load their respective samples and perform a sampling for each
		

	# draw random stratified sample and extract training set indices
	sss = StratifiedShuffleSplit(classes, n_iter=1, train_size=n_samples)
	sample_indices, _ = sss.next()

	# save

def load_feature_struct(f):
	"Load the feature struct from a feature config file."
	d, m = os.path.split(os.path.splitext(f)[0])
	f, filename, desc = imp.find_module(m, [d])
	return imp.load_module(m, f, filename, desc).features_to_extract

def load_feature_names(f):
	"Load the feature names from a feature config file."
	fs = load_feature_struct(f)
	return [feature_struct_entry_to_name(e) for e in fs]

if __name__ == "__main__":
	main()
	

