#!/usr/bin/python

"""
Sample a traning set for a case by drawing from all other images using stratified random sampling.

arg1: directory with case-folders containing feature files
arg2: directory containing segmentations
arg3: directory containing brain masks
arg4: target directory
arg5: file containing a struct identifying the features to sample
arg6: number of samples to draw
arg7+: indices of all cases from which to draw the training sample
"""

import os
import sys
import imp
import numpy
import pickle
import itertools

from medpy.io import load
from medpy.features.utilities import append, join

# main settings
min_no_of_samples_per_class_and_case = 4

# debug settings
verboose = False
debug = False
override = True # activate override (will signal a warning)

def main():
	# catch arguments
	src_dir = sys.argv[1]
	seg_dir = sys.argv[2]
	msk_dir = sys.argv[3]
	trg_dir = sys.argv[4]
	feature_cnf_file = sys.argv[5]
	total_no_of_samples = int(sys.argv[6])
	training_set_cases = sys.argv[7:]

	# load features to use and create proper names from them
	features_to_use = load_feature_names(feature_cnf_file)

	# warn if target sample set already exists
	if os.path.isfile('{}/trainingset.features.npy'.format(trg_dir)):
		if override:
			print 'WARNING: The target file {}/trainingset.features.npy already exists and will be replaced by a new sample.'.format(trg_dir)
		else:
			print 'WARNING: The target file {}/trainingset.features.npy already exists. Skipping.'.format(trg_dir)
			sys.exit(0)

	if verboose: print 'Preparing leave-out training set'
	# initialize collection variables
	training_set_foreground_selections = dict.fromkeys(training_set_cases)
	training_set_background_selections = dict.fromkeys(training_set_cases)
	
	# use stratified random sampling to select a number of sample for each case
	for case in training_set_cases:
		if verboose: print 'Stratified random sampling of case {}'.format(case)
		# determine number of samples to draw from this case
		samples_to_draw = int(total_no_of_samples / len(training_set_cases))
		if debug: print 'samples_to_draw', samples_to_draw
		# load class memberships of case as binary array
		mask = load(os.path.join(msk_dir, '{}.nii.gz'.format(case)))[0].astype(numpy.bool)
		truth = load(os.path.join(seg_dir, '{}.nii.gz'.format(case)))[0].astype(numpy.bool)
		class_vector = truth[mask]
		# determine how many fg and bg samples to draw from this case
		ratio = numpy.count_nonzero(~class_vector) / float(numpy.count_nonzero(class_vector))
		fg_samples_to_draw = int(samples_to_draw / (ratio + 1))
		bg_samples_to_draw = int(samples_to_draw / (ratio + 1) * ratio)
		if debug: print 'fg_samples_to_draw', fg_samples_to_draw
		if debug: print 'bg_samples_to_draw', bg_samples_to_draw
		if debug: print 'ratio fg:bg', '1:{}'.format(ratio)
		# check for exceptions
		if fg_samples_to_draw < min_no_of_samples_per_class_and_case: raise Exception('Current setting would lead to a drawing of only {} fg samples for case {}!'.format(fg_samples_to_draw, case))
		if bg_samples_to_draw < min_no_of_samples_per_class_and_case: raise Exception('Current setting would lead to a drawing of only {} bg samples for case {}!'.format(bg_samples_to_draw, case))
		if fg_samples_to_draw > numpy.count_nonzero(class_vector):
			raise Exception('Current settings would require to draw {} fg samples, but only {} present for case {}!'.format(fg_samples_to_draw, numpy.count_nonzero(class_vector), case))
		if bg_samples_to_draw > numpy.count_nonzero(~class_vector):
			raise Exception('Current settings would require to draw {} bg samples, but only {} present for case {}!'.format(bg_samples_to_draw, numpy.count_nonzero(~class_vector), case))
		# get sample indices and split into fg and bg indices
		samples_indices = numpy.arange(len(class_vector))
		fg_samples_indices = samples_indices[class_vector]
		bg_samples_indices = samples_indices[~class_vector]
		if debug: print 'fg_samples_indices.shape', fg_samples_indices.shape
		if debug: print 'bg_samples_indices.shape', bg_samples_indices.shape
		# randomly draw the required number of sample indices
		numpy.random.shuffle(fg_samples_indices)
		numpy.random.shuffle(bg_samples_indices)
		fg_sample_selection = fg_samples_indices[:fg_samples_to_draw]
		bg_sample_selection = bg_samples_indices[:bg_samples_to_draw]
		if debug: print 'fg_sample_selection.shape', fg_sample_selection.shape
		if debug: print 'bg_sample_selection.shape', bg_sample_selection.shape
		# add to collection
		training_set_foreground_selections[case] = fg_sample_selection
		training_set_background_selections[case] = bg_sample_selection
		
	# load the features of each case, draw the samples from them and append them to a training set
	fg_samples = []
	bg_samples = []
	for case in training_set_cases:
		if verboose: print 'Sampling features of case {}'.format(case)
		
		# loading and sampling features piece-wise to avoid excessive memory requirements
		fg_samples_case = []
		bg_samples_case = []
		for feature_name in features_to_use:
			_file = os.path.join(src_dir, case, '{}.npy'.format(feature_name))
			if not os.path.isfile(_file):
				raise Exception('The feature "{}" for case {} could not be found in folder "{}". Breaking.'.format(feature_name, case, os.path.join(src_dir, case)))
			with open(_file, 'r') as f:
				feature_vector = numpy.load(f)
				fg_samples_case.append(feature_vector[training_set_foreground_selections[case]])
				bg_samples_case.append(feature_vector[training_set_background_selections[case]])
				
		# join and append feature vector from this case
		fg_samples.append(join(*fg_samples_case))
		bg_samples.append(join(*bg_samples_case))
		
	# prepare training set as numpy array and the class memberships
	fg_samples = append(*fg_samples)
	bg_samples = append(*bg_samples)
	samples_class_memberships = numpy.zeros(len(fg_samples) + len(bg_samples), dtype=numpy.bool)
	samples_class_memberships[:len(fg_samples)] += numpy.ones(len(fg_samples), dtype=numpy.bool)
	samples_feature_vector = append(fg_samples, bg_samples)
	
	if debug: print 'samples_feature_vector', samples_feature_vector.shape
	if debug: print 'class_memberships', samples_class_memberships.shape
	
	# save feature vector, feature names and class membership vector as leave-one-out training set
	if verboose: print 'Saving training data set'
	with open('{}/trainingset.features.npy'.format(trg_dir), 'wb') as f:
		numpy.save(f, samples_feature_vector)
	with open('{}/trainingset.classes.npy'.format(trg_dir), 'wb') as f:
		numpy.save(f, samples_class_memberships)
	with open('{}/trainingset.fnames.npy'.format(trg_dir), 'wb') as f:
		numpy.save(f, features_to_use)
	with open('{}/trainingset.fgselections.pkl'.format(trg_dir), 'wb') as f:
		pickle.dump(training_set_foreground_selections, f)
	with open('{}/trainingset.bgselections.pkl'.format(trg_dir), 'wb') as f:
		pickle.dump(training_set_background_selections, f)
		
	if verboose: print
			
	if verboose: print 'Done.'

def feature_struct_entry_to_name(fstruct):
	seq, fcall, fargs, _ = fstruct
	return 'feature.{}.{}.{}'.format(seq, fcall.func_name, '_'.join(['arg{}'.format(i) for i in fargs]))
	
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




