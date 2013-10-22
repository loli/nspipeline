#!/usr/bin/python

"""
Apply a lower threshold to an image and condense all intensities below to the threshold value.
<program>.py <in-image> <threshold> <out-image>
"""

import sys
import numpy
from medpy.io import load, save

def main():
	i, h = load(sys.argv[1])
	thr = int(sys.argv[2])
	i[i < thr] = thr
	save(i, sys.argv[3], h)

if __name__ == "__main__":
	main()


