#!/usr/bin/python

"""
Thresholds an image according to a value (True where intensity >= value).
arg1: the input image
arg2: the threshold
arg3: the output image
"""

import sys
import numpy

from medpy.io import load, save

def main():
	i, h = load(sys.argv[1])
	thr = float(sys.argv[2])

	o = i >= thr

	save(o, sys.argv[3], h)

if __name__ == "__main__":
	main()
