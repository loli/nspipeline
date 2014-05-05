#!/usr/bin/python

"""
Corrects a (possibly) wrong sform in a NifTi header by copying the qform to it,
arg1: the image to correct
arg2: the target output image
"""

import sys

from medpy.io import load, save

def main():
	# load input image
	i, h = load(sys.argv[1])

	# correct sfrom
	h.set_sform(h.get_qform())

	# save
	save(i, sys.argv[2], h)

if __name__ == "__main__":
	main()
