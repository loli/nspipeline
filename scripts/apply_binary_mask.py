#!/usr/bin/python

"""
Apply a binary mask to an image, keeping only the intensity values where the maks is True.
All other are set to zero.
<program>.py <in-image> <binary-mask> <out-image>
"""

import sys
import numpy
from medpy.io import load, save

def main():
	i, h = load(sys.argv[1])
	m = load(sys.argv[2])[0].astype(numpy.bool)
	i[~m] = 0
	save(i, sys.argv[3], h)

if __name__ == "__main__":
	main()


