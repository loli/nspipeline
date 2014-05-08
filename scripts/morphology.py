#!/usr/bin/python

"""
Applies a post-processing morphological step to binary images.
Note: Takes voxel-spacing into account.
Note: Does not remove small objects if the binary mask would be empty afterwards.
<program>.py <in-binary-image> <out-binary-image> <parameter1> <parameter2>
"""

import sys
import numpy
from medpy.io import load, save, header
from scipy.ndimage.morphology import binary_opening, binary_closing,\
    binary_erosion, binary_dilation, binary_fill_holes

def main():
	i, h = load(sys.argv[1])
	ibo, ibc, ibe, ibd = map(int, sys.argv[3:])

    	i = binary_fill_holes(i)

	if not 0 == ibo: i = binary_opening(i, structure=None, iterations=ibo)
	if not 0 == ibc: i = binary_closing(i, structure=None, iterations=ibc)

	if not 0 == ibe: i = binary_erosion(i, structure=None, iterations=ibe)
	if not 0 == ibd: i = binary_dilation(i, structure=None, iterations=ibd)

	#i = morphology2d(binary_opening, i, structure=1, iterations=1)
	#i = morphology2d(binary_closing, i, structure=1, iterations=1)

	#i = morphology2d(binary_erosion, i, structure=1, iterations=1)
	#i = morphology2d(binary_dilation, i, structure=1, iterations=1)

	if 0 == numpy.count_nonzero(i):
		raise Warning("{}: empty segmentation resulted".format(sys.argv[1]))

	save(i, sys.argv[2], h, True)

def morphology2d(operation, arr, structure = None, iterations=1, dimension = 2):
	res = numpy.zeros(arr.shape, numpy.bool)
	for sl in range(processed.shape[dimension]):	
		res[:,:,sl] = operation(arr[:,:,sl], structure, iterations)
	return res

if __name__ == "__main__":
	main()


