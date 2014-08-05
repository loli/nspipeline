#!/usr/bin/python

# arg1: src1 directory
# arg2: src2 directory
# arg3: trgt directory

import sys
import numpy
from medpy.features.utilities import append

def main():
    # catch arguments
    src1_dir = sys.argv[1]
    src2_dir = sys.argv[2]
    trgt_dir = sys.argv[3]

    fnames1 = numpy.load('{}/trainingset.fnames.npy'.format(src1_dir))
    fnames2 = numpy.load('{}/trainingset.fnames.npy'.format(src2_dir))
    if not numpy.all(fnames1 == fnames2):
        raise Exception('Feature names indicate that the two source sets are incompatible.')
    numpy.save('{}/trainingset.fnames.npy'.format(trgt_dir), fnames1)

    ftrs1 = numpy.load('{}/trainingset.features.npy'.format(src1_dir))
    ftrs2 = numpy.load('{}/trainingset.features.npy'.format(src2_dir))
    numpy.save('{}/trainingset.features.npy'.format(trgt_dir), append(ftrs1, ftrs2))

    cls1 = numpy.load('{}/trainingset.classes.npy'.format(src1_dir))
    cls2 = numpy.load('{}/trainingset.classes.npy'.format(src2_dir))
    numpy.save('{}/trainingset.classes.npy'.format(trgt_dir), append(cls1, cls2))	
	
if __name__ == "__main__":
	main()


