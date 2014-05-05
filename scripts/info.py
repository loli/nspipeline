#!/usr/bin/python

# Scans all image folders and creates a table with detailed information about each image.

import os
import sys
from medpy.io import load, save, header

DEBUG = True
FILE_ENDING = 'nii.gz'

def main():
	srcdir = sys.argv[1] # the image folder contianing the case folders (e.g. data/)
	target = sys.argv[2] # the target file where to save the table (in csv format)

	if DEBUG: print 'INFO: Processing all cases in folder {} and saving table as {}.'.format(srcdir, target)

	# check if output file already exists
	if os.path.isfile(target):
		print 'ERROR: Target file {} already exists. Breaking.'.format(target)
		sys.exit(-1)

	# open output file and prepare table header
	with open(target, 'w') as f:
		f.write('case;image-type;X;Y;Z;Xres;Yres;Zres;data-type;mean;min;max\n')

		# iterate over all cases and add an according line to the table
		for root, dirs, files in os.walk(srcdir):
			for case in sorted(dirs):
				if DEBUG: print 'INFO: Processing case {}.'.format(case)
				for root, dirs, files in os.walk('{}/{}'.format(srcdir, case)):
					for file_ in files:
						if file_.endswith(FILE_ENDING):
							imgtype = file_[:-(len(FILE_ENDING) + 1)]
							i, h = load('{}/{}/{}'.format(srcdir, case, file_))
							f.write('{};{};{};{};{};{};{};{}\n'.format(case, imgtype, ';'.join(map(str, i.shape)), ';'.join(map(str, header.get_pixel_spacing(h))), i.dtype, i.mean(), i.min(), i.max()))

	print 'Terminated.'

if __name__ == "__main__":
    main()
