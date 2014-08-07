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
from medpy.metric import obj_tpr, obj_fpr, obj_assd

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
    dcs = []
    tprs = []
    fprs = []
    assds = []

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
    tprs = pool.map(wtpr, zip(t, s))
    fprs = pool.map(wfpr, zip(t, s))
    assds = pool.map(wassd, zip(t, s, [header.get_pixel_spacing(h) for h in ht]))
    #assds = [obj_assd(_t, _s, header.get_pixel_spacing(_h)) for _t, _s, _h in zip (t, s, ht)]

    # print case-wise results
    print 'Metrics:'
    print 'Case\tDC[0,1]\tTPR(%)\tFPR(%)\tASSD(mm)'
    for case, _dc, _tpr, _fpr, _assd in zip(cases, dcs, tprs, fprs, assds):
        print '{}\t{:>3,.3f}\t{:>4,.3f}\t{:>4,.3f}\t{:>3,.3f}'.format(case, _dc, _tpr, _fpr, _assd)

    # check for nan/inf values of failed cases and signal warning
    mask = numpy.isfinite(assds)
    if not numpy.all(mask):
        print 'WARNING: Average values only computed on {} of {} cases!'.format(numpy.count_nonzero(mask), mask.size)

        print 'DM  average\t{} +/- {} (Median: {})'.format(numpy.asarray(dcs)[mask].mean(), numpy.asarray(dcs)[mask].std(), numpy.median(numpy.asarray(dcs)[mask]))
        print 'TPR  average\t{} +/- {} (Median: {})'.format(numpy.asarray(tprs)[mask].mean(), numpy.asarray(tprs)[mask].std(), numpy.median(numpy.asarray(tprs)[mask]))
        print 'FPR  average\t{} +/- {} (Median: {})'.format(numpy.asarray(fprs)[mask].mean(), numpy.asarray(fprs)[mask].std(), numpy.median(numpy.asarray(fprs)[mask]))
        print 'ASSD average\t{} +/- {} (Median: {})'.format(numpy.asarray(assds)[mask].mean(), numpy.asarray(assds)[mask].std(), numpy.median(numpy.asarray(assds)[mask]))

def wdc(x):
    return dc(*x)

def wtpr(x):
    try:
        val = obj_tpr(*x)		
    except ZeroDivisionError:
	    val = numpy.inf
    return val

def wfpr(x):
    try:
        val = obj_fpr(*x)
    except ZeroDivisionError:
	    val = numpy.inf
    return val

def wassd(x):
    try:
	    val = obj_assd(*x)
    except RuntimeError:
	    val = numpy.inf
    return val

if __name__ == "__main__":
	main()
