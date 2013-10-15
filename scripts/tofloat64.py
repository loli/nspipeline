#!/usr/bin/python

"""
Load the input image, convert its data to numpy.float64, then save it under output.
"""

import sys
import numpy
from medpy.io import load, save

def main():
	i, h = load(sys.argv[1])
	save(i.astype(numpy.float64), sys.argv[2], h)

if __name__ == "__main__":
	main()


