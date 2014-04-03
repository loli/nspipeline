#!/usr/bin/python

"""
Evaluate the segmentation created.
arg1: the segmentation result for each case, with a {} in place of the case number
arg2: the ground truth segmentation, with a {} in place of the case number
arg3: the cases mask file, with a {} in place of the case number
arg4+: the cases to evaluate
"""

import sys
import math
import time
from multiprocessing.pool import Pool

import numpy

from medpy.io import load, header
from medpy.metric import dc, hd, assd, precision, recall

# constants
n_jobs = 6
silent = True

def main():
	# catch parameters
	segmentation_base_string = sys.argv[1]
	ground_truth_base_string = sys.argv[2]
	mask_file_base_string = sys.argv[3]
	cases = sys.argv[4:]

	# evaluate each case and collect the scores
	hds = []
	assds = []
	precisions = []
	recalls = []
	dcs = []

	# load images and apply mask to segmentation and ground truth (to remove ground truth fg outside of brain mask)
	splush = [load(segmentation_base_string.format(case)) for case in cases]
	tplush = [load(ground_truth_base_string.format(case)) for case in cases]
	masks = [load(mask_file_base_string.format(case))[0].astype(numpy.bool) for case in cases]

	s = [s.astype(numpy.bool) & m for (s, _), m in zip(splush, masks)]
	t = [t.astype(numpy.bool) & m for (t, _), m in zip(tplush, masks)]
	hs = [h for _, h in splush]
	ht = [h for _, h in tplush]

	# compute and append metrics (Pool-processing)
	pool = Pool(n_jobs)
	dcs = pool.map(wdc, zip(t, s))
	precisions = pool.map(wprecision, zip(s, t))
	recalls = pool.map(wrecall, zip(s, t))
	hds = pool.map(whd, zip(t, s, [header.get_pixel_spacing(h) for h in ht]))
	assds = pool.map(wassd, zip(t, s, [header.get_pixel_spacing(h) for h in ht]))

	# print results
	print 'Metrics:'
	print 'Case\tDC[0,1]\tHD(mm)\tP2C(mm)\tprec.\trecall'
    	for case, _dc, _hd, _assd, _pr, _rc in zip(cases, dcs, hds, assds, precisions, recalls):
        	print '{}\t{:>3,.3f}\t{:>4,.3f}\t{:>4,.3f}\t{:>3,.3f}\t{:>3,.3f}'.format(case, _dc, _hd, _assd, _pr, _rc)
        
    	print 'DM  average\t{} +/- {}'.format(numpy.asarray(dcs).mean(), numpy.asarray(dcs).std())
    	print 'HD  average\t{} +/- {}'.format(numpy.asarray(hds).mean(), numpy.asarray(hds).std())
    	print 'ASSD average\t{} +/- {}'.format(numpy.asarray(assds).mean(), numpy.asarray(assds).std())
    	print 'Prec. average\t{} +/- {}'.format(numpy.asarray(precisions).mean(), numpy.asarray(precisions).std())
    	print 'Rec. average\t{} +/- {}'.format(numpy.asarray(recalls).mean(), numpy.asarray(recalls).std())

def wdc(x):
	return dc(*x)
def whd(x):
	return hd(*x)
def wprecision(x):
	return precision(*x)
def wrecall(x):
	return recall(*x)
def wassd(x):
	return assd(*x)

if __name__ == "__main__":
	main()
