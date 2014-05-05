#!/usr/bin/python

# clean out nan and inf values in-place.
# arg1: the image to clean

import sys

import numpy

from medpy.io import load, save

i, h = load(sys.argv[1])

i[numpy.isnan(i)] = 0
i[numpy.isinf(i)] = 0

i = i.copy()

save(i, sys.argv[1], h)
