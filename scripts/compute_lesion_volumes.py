#!/usr/bin/python

"""
Computes the lesion volumes, once percentual to the brain volume and once in mm, and
prints them to the stdout.

arg1: the directory with the lesion mask images
arg2: the directory with the brain mask images
"""

import os
import sys

import numpy

from medpy.io import load, header

def main():
	print 'lesion\tvolume (%)\tvolume (mm)'

	files = [f for f in os.listdir('{}'.format(sys.argv[1])) if os.path.isfile('{}/{}'.format(sys.argv[1], f))]
	for f in files:
		l, h = load('{}/{}'.format(sys.argv[1], f))
		m, _ = load('{}/{}'.format(sys.argv[2], f))

		lesion_voxel = numpy.count_nonzero(l)
		total_voxel = numpy.count_nonzero(m)

		volume_mm = numpy.prod(header.get_pixel_spacing(h)) * lesion_voxel
		volume_percentage = lesion_voxel / float(total_voxel)

		print '{}\t{}\t{}\t'.format(f[:-7], volume_percentage, volume_mm)

if __name__ == "__main__":
	main()

		
	
		
		
