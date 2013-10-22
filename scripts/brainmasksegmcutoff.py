#!/usr/bin/python

"""
Takes a brain mask and a segmentation as input and checks, whether and if, how many voxel the brain mask cuts from the segmentation.
"""

import sys
import numpy
from medpy.io import load, save

def main():
	m = load(sys.argv[1])[0].astype(numpy.bool)
	s = load(sys.argv[2])[0].astype(numpy.bool)

	intc = numpy.count_nonzero(~m & s)

	print "Non-intersecting part of the segmentation:"
	print "{} out of {} voxels".format(intc, numpy.count_nonzero(s))

if __name__ == "__main__":
	main()


