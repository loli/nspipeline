#!/usr/bin/python

"""
Passes a header from one image file to another (with the usual adaptions of data type, etc. undetaken).
arg1: the image to correct (in-place)
arg2: the template image, whose header to take
"""

import sys
import numpy

from medpy.io import load, save

def main():
	# load input image
	i, _ = load(sys.argv[1])

	# load template image
	_, h = load(sys.argv[2])
	
	# save input image with adapted header in place
	j = i.copy()
	save(j, sys.argv[1], h)

if __name__ == "__main__":
	main()

