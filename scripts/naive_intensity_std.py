#!/usr/bin/python

# normalizes an images intensities by zero mean and unit variance
# normalizes an images intensities by zero modus and unit variance
# arg1: the image to normalize
# arg2: the image mask
# arg3: the normalized image

import sys
import numpy

from medpy.io import load, save

i, h = load(sys.argv[1])
m = load(sys.argv[2])[0].astype(numpy.bool)

# APPROACH 01: zero-mean and one-std
i = i.astype(numpy.float)
i -= i.mean()
i /= i.std()

# APPROACH 02: zero-modus and one-std
#hist, bin_edges = numpy.histogram(i[m], bins=100)
#modus_pos = numpy.argmax(hist)
#lower, upper = bin_edges[modus_pos:modus_pos+2]
#modus = (upper - lower) / 2.
#i[m] -= modus
#i[m] /= i.std()

save(i, sys.argv[3], h)
