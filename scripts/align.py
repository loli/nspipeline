#!/usr/bin/python

"""
Aligns the first input image to the second taking origin into account and assuming the same voxel spacing.
Note: This might require the image to be truncated.
arg1: the image to align
arg2: the reference image
arg3: the target output image
"""

import sys
import numpy

from medpy.io import load, save, header

def main():
	i1, h1 = load(sys.argv[1])
	i2, h2 = load(sys.argv[2])

	# shift image to align origins
	origin_h1 = numpy.sign(h1.get_qform()[0:3,0:3]).dot(header.get_offset(h1))
	origin_h2 = numpy.sign(h2.get_qform()[0:3,0:3]).dot(header.get_offset(h2))
	origin_difference_pixel = (origin_h1 - origin_h2) / numpy.asarray(header.get_pixel_spacing(h1))
	# negative values: shift image 1 by this upon inserting (which is the smae as cutting the output image)
	# positive values: cut image 1 by this at inserting and also cut right side by length of output image plus this value
	o = numpy.zeros(i2.shape, i2.dtype)
	o_slicer = []
	i_slicer = []
	for j, p in enumerate(origin_difference_pixel):
		if p >= 0:
			i_slicer.append(slice(0,      min(i1.shape[j], o.shape[j] - abs(p))))
			o_slicer.append(slice(abs(p), min(i1.shape[j] + abs(p), o.shape[j])))
		else:
			i_slicer.append(slice(abs(p), min(i1.shape[j], o.shape[j] + abs(p))))
			o_slicer.append(slice(0,      min(i1.shape[j] - abs(p), o.shape[j])))

	o[o_slicer] = i1[i_slicer]
	header.set_offset(h1, header.get_offset(h2))
	
	save(o, sys.argv[3], h1)

if __name__ == "__main__":
	main()
