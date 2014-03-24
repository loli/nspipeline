#!/usr/bin/python

"""
Train a decision forest on a training set.
arg1: the training set file (.features.npy)
arg2: the decision forest target file
"""

import sys
import pickle
import numpy

from sklearn.ensemble.forest import ExtraTreesClassifier

# constants
n_jobs = 6

def main():
	# catch parameters
	training_set_features = sys.argv[1]
	training_set_classes = training_set_features.replace('features', 'classes')
	forest_file = sys.argv[2]

        # loading training features
        with open(training_set_features, 'r') as f:
            training_feature_vector = numpy.load(f)
        with open(training_set_classes , 'r') as f:
            training_class_vector = numpy.load(f)

        # prepare and train the decision forest
        forest = ExtraTreesClassifier(n_estimators=200,
                            criterion = 'entropy',
                            max_features = None,
                            min_samples_split = 2,
                            min_samples_leaf = 1,
                            bootstrap = True,
                            oob_score = False,
                            random_state=0,
                            n_jobs=n_jobs,
                            compute_importances=True)
        forest.fit(training_feature_vector, training_class_vector)

	# saving the decision forest
	with open(forest_file, 'wb') as f:
		pickle.dump(forest, f)

if __name__ == "__main__":
	main()
