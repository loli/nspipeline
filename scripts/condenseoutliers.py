#!/usr/bin/python

"""
Apply a percentile threshold to the image, condensing all outliers to the percentile values.
<program>.py <in-image> <out-image>
"""

import sys
import numpy
from medpy.io import load, save

def main():
	i, h = load(sys.argv[1])
	li = numpy.percentile(i, (1, 99.9))
	i[i < li[0]] = li[0]
	i[i > li[1]] = li[1]
	save(i, sys.argv[2], h)

if __name__ == "__main__":
	main()


