#!/usr/bin/python

"""
Remove small binary objects from a binary mask.
Note: Takes voxel-spacing into account.
<program>.py <in-binary-image> <out-binary-image> <threshold-size-in-mm>
"""

import sys
import numpy
from medpy.io import load, save, header
from medpy.filter import size_threshold

def main():
	thr = float(sys.argv[3])
	i, h = load(sys.argv[1])

	# adapt threshold by voxel spacing
	thr /= numpy.prod(header.get_pixel_spacing(h))
	# threshold binary objects
	i = size_threshold(i, thr, 'lt')

	save(i, sys.argv[2], h, True)

if __name__ == "__main__":
	main()


