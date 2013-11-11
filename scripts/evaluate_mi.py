#!/usr/bin/python

"""
Mutual information evaluation.
arg1: first image
arg2: second image
"""

import sys

import numpy

from medpy.io import load, save
from medpy.metric.image import mutual_information

def main():
	# load input images
	i1, h1 = load(sys.argv[1])
	i2, h2 = load(sys.argv[2])

	# clean images
	i1 = clean(i1)
	i2 = clean(i2)

	# smooth images
	#i1 = gauss(i1, h1, sigma=2)
	#i2 = gauss(i2, h2, sigma=2)

	# mutual information
	mu = mutual_information(i1[(i1 > 0) & (i2 > 0)], i2[(i1 > 0) & (i2 > 0)])

	# print
	print '{};{};'.format(sys.argv[1], mu)

def clean(i, cval = 0):
	"""
	Removes all nan and inf from the image and replace them with a constant value.
	"""
	i[numpy.isnan(i)] = 0
	i[numpy.isinf(i)] = 0
	return i

def gauss(i, h, sigma=6):
	"""
	Applies a gaussian smoothing to the image with the supplied kernel size in mmm.
	"""
	sigmas = [sigma * ps for ps in header.get_pixel_spacing(h)]
	i = gaussian_filter(i, sigma=sigmas)
	return i

if __name__ == "__main__":
	main()
