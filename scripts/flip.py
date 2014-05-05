#!/usr/bin/python

####
# Flips an image along the given dimensions in-place.
# arg1: the image to flip
# arg2: the dimension along which to flip
####

import sys

import numpy

from medpy.io import load, save

def main():
	_file = sys.argv[1]
	dim = int(sys.argv[2])

	i, h = load(_file)
	i = flip_axis(i, dim).copy()
	save(i, _file, h)

def flip_axis(arr, axis=0):
    arr = numpy.asanyarray(arr)
    arr = arr.swapaxes(0, axis)
    arr = numpy.flipud(arr)
    return arr.swapaxes(axis, 0)

if __name__ == "__main__":
    main()
