#!/usr/bin/python

####
# Inverts a binary image
# arg1: the input image to invert
# arg2: the inverted output image
####

import sys

import numpy

from medpy.io import load, save

def main():
	infile = sys.argv[1]
	outfile = sys.argv[2]

	i, h = load(infile)
	i = i.astype(numpy.bool)
	h.set_sform(h.get_qform())
	save(~i, outfile, h)

if __name__ == "__main__":
    main()
