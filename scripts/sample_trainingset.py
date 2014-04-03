#!/usr/bin/python

"""
Sample a traning set for a case by drawing from all other images using sstratified random sampling.
arg1: directory with case-folders containing feature files
arg2: directory containing segmentations
arg3: string pointing to the cases brain masks with a {} in place of the case number
arg4: index of current case
"""

import os
import sys
import numpy
import itertools

from medpy.io import load
from medpy.features.utilities import append, join

# main settings
total_no_of_samples = 250000
min_no_of_samples_per_class_and_case = 4

# debug settings
verboose = False
debug = False

def main():
	# prepare settings
	left_out_case = sys.argv[4]
	src_dir = sys.argv[1]
	seg_dir = sys.argv[2]
	msk_str = sys.argv[3]
	trg_dir = '{}/{}/'.format(src_dir, left_out_case)

	# collect cases present
	cases = []
	for _file in os.listdir(src_dir):
		if True == os.path.isdir(os.path.join(src_dir, _file)):
			cases.append(_file)
	cases.sort()

	if verboose: print 'Preparing leave-{}-out training set'.format(left_out_case)
	# determine cases to use to the training set build in this round
	training_set_cases = list(cases)
	training_set_cases.remove(left_out_case)
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
		mask = load(msk_str.format(case))[0].astype(numpy.bool)
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
		feature_list = []
		for _file in os.listdir(os.path.join(src_dir, case)):
			if _file.endswith('.npy') and _file.startswith('feature.'):
				feature_list.append(_file[:-4])
				with open(os.path.join(src_dir, case, _file), 'r') as f:
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
		numpy.save(f, feature_list)
		
	if verboose: print
			
	if verboose: print 'Done.'

if __name__ == "__main__":
	main()




