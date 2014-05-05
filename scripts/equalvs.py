#!/usr/bin/python

# Checks whether the (equally named) images in two folders have the same voxel spacing
# You can additionally supply a "-i" switch at the end to treat the second folder as flat structure (e.g. the ones containing masks or segmentations)

import os
import sys
import numpy
from medpy.io import load, save, header

DEBUG = True
FILE_ENDING = 'nii.gz'

def main():
	onedir = sys.argv[1] # the first folder containing case folders
	twodir = sys.argv[2] # the second folder containing case folders
	nocase = (len(sys.argv) > 3 and sys.argv[3] == '-i')

	if DEBUG: print 'INFO: Comparing all cases in folders {} and {}.'.format(onedir, twodir)

	# iterate over first folder and compare voxel spacings with equivalent image in second folder
	print "Case\tvs same\tshape same"
	for root, dirs, files in os.walk(onedir):
		for case in sorted(dirs):
			for root, dirs, files in os.walk('{}/{}'.format(onedir, case)):
				for file_ in files:
					if file_.endswith(FILE_ENDING):
						i, hi = load('{}/{}/{}'.format(onedir, case, file_))
						if nocase:
							j, hj = load('{}/{}.{}'.format(twodir, case, FILE_ENDING))
						else:
							j, hj = load('{}/{}/{}'.format(twodir, case, file_))
						vs_same = numpy.array_equal(header.get_pixel_spacing(hi), header.get_pixel_spacing(hj))
						shape_same = numpy.array_equal(i.shape, j.shape)
						print '{}\t{}\t{}'.format(case, vs_same, shape_same)
						if not vs_same:
							print "\t{} vs {}".format(header.get_pixel_spacing(hi), header.get_pixel_spacing(hj))
						if not shape_same:
							print "\t{} vs {}".format(i.shape, j.shape)
	print 'Terminated.'

if __name__ == "__main__":
    main()
