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
from scipy.ndimage.morphology import binary_erosion
from scipy.spatial.distance import cdist
from sklearn.metrics.metrics import precision_recall_fscore_support

from medpy.io import load, header

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
	p2cs = []
	prfs = []
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
	prfs = pool.map(precision_recall_fscore, zip(t, s))
	dcs = pool.map(dice_coefficient, zip(t, s))
	hd_p2c = pool.map(hausdorff_p2c_distances, zip(t, s, ht, hs))
	hds = [hd for hd, _ in hd_p2c]
	p2cs = [p2c for _, p2c in hd_p2c]

	# print results
	print 'Metrics:'
	print 'Case\tDC[0,1]\tHD(mm)\tP2C(mm)\tprec.\trecall\tfscore'
    	for case, dc, hd, p2c, prf in zip(cases, dcs, hds, p2cs, prfs):
        	print '{}\t{:>3,.3f}\t{:>4,.3f}\t{:>4,.3f}\t{:>3,.3f}\t{:>3,.3f}\t{:>3,.3f}'.format(case, dc, hd, p2c, *map(float, prf))
        
    	print 'DM  average\t{} +/- {}'.format(numpy.asarray(dcs).mean(), numpy.asarray(dcs).std())
    	print 'HD  average\t{} +/- {}'.format(numpy.asarray(hds).mean(), numpy.asarray(hds).std())
    	print 'P2C average\t{} +/- {}'.format(numpy.asarray(p2cs).mean(), numpy.asarray(p2cs).std())
    	print 'PRF average\t{} +/- {}'.format(numpy.asarray(prfs).mean(0), numpy.asarray(prfs).std(0))

def hausdorff_p2c_distances((i, j, hi, hj)):
    """
    Joint version of hausdorff and point-to-curve distances for faster computation.
    
    @return (hausdorff_distance, p2c_distance)
    """
    # pre-process inputs
    if None == hj: hj = hi
    
    # compute pairwise (euclidean) distances and draw the minimum of each
    di, dj = __pairwise_min_border_distance(i, j, hi, hj)
    
    # compute hausdorff and p2c distance
    hd = float(max(di.max(), dj.max()))
    p2c = 1/2. * (sum(di) / float(len(di)) + sum(dj) / float(len(dj)))
    
    # return distances
    return (hd, p2c)
    
    
def hausdorff_distance(i, j, hi, hj = None):
    """
    Computes the Hausdorff distance in mm between two binary objects.
    @param i an n-dimensional image treated as boolean type
    @param j an n-dimensional image treated as boolean type
    @param hi header of image i
    @param hj header of image j, if None, assuming that i and j share the pixel spacing
    
    @return the Hausdorff distance between the two sample contained in the input images    
    """
    # pre-process inputs
    if None == hj: hj = hi
    
    # compute pairwise (euclidean) distances and draw the minimum of each
    di, dj = __pairwise_min_border_distance(i, j, hi, hj)
    
    # compute and return hausdorff distance
    return float(max(di.max(), dj.max()))
    
    
def point2curve_distance(i, j, hi, hj = None):
    """
    Computes the point-to-curve (P2C) distance in mm between two binary objects.
    
    @param i an n-dimensional image treated as boolean type
    @param j an n-dimensional image treated as boolean type
    @param hi header of image i
    @param hj header of image j, if None, assuming that i and j share the pixel spacing
    
    @return the dice coefficient between the two sample contained in the input images    
    """
    # compute pairwise (euclidean) distances and draw the minimum of each direction
    di, dj = __pairwise_min_border_distance(i, j, hi, hj)
    
    # compute and return symmetric average distance
    return 1/2. * (sum(di) / float(len(di)) + sum(dj) / float(len(dj)))
    
def dice_coefficient((i, j)):
    """
    Computes the dice coefficient between two samples expressed as binary images of
    arbitrary dimensionality. Voxel spacing is irrelevant for the dice coefficient.
    
    @param i an n-dimensional image treated as boolean type
    @param j an n-dimensional image treated as boolean type
    
    @return the dice coefficient between the two sample contained in the input images
    """
    # pre-process inputs
    i = i.astype(numpy.bool)
    j = j.astype(numpy.bool)
    
    # compute intersection size in voxels
    intersection= numpy.count_nonzero(i & j)
    
    # compute the separate segmentation sizes
    size_i = numpy.count_nonzero(i)
    size_j = numpy.count_nonzero(j)
    
    # compute and return dice coefficient
    return 2 * intersection / float(size_i + size_j)
    
def precision_recall_fscore((i, j)):
    """
    Computes precision, recall and f-score between two samples.
    
    @param i an n-dimensional image treated as boolean type
    @param j an n-dimensional image treated as boolean type
    
    @return (precision, recall, fscore) as numpy array    
    """
    # pre-process inputs
    i = i.astype(numpy.bool).flat
    j = j.astype(numpy.bool).flat
    
    return numpy.asarray(precision_recall_fscore_support(i, j, average='weighted')).T[0:3]
    
def __pairwise_min_border_distance(i, j, hi, hj = None):
    """
    Takes two images containing a binary object each and computes the pairwise distances
    between their border voxels.
    
    @param i an n-dimensional image treated as boolean type
    @param j an n-dimensional image treated as boolean type
    @param hi header of image i
    @param hj header of image j, if None, assuming that i and j share the pixel spacing
    
    @return (min distances along i axes, min distance along j axes) of pairwise distances
    """
    # pre-process inputs
    i = i.astype(numpy.bool)
    j = j.astype(numpy.bool)
    if None == hj: hj = hi
    
    # remove all but the one-pixel border of the samples in the images
    i -= binary_erosion(i)
    j -= binary_erosion(j)
    
    # extract location of border voxels
    Xi = numpy.asarray(numpy.nonzero(i)).T
    Xj = numpy.asarray(numpy.nonzero(j)).T
    
    # convert to real world space (i.e. mm)
    Xi *= numpy.asarray(header.get_pixel_spacing(hi))
    Xj *= numpy.asarray(header.get_pixel_spacing(hj))

    # compute pairwise (euclidean) distances, extract minima along both axes and return
    return __friendly_min_cdist(Xi, Xj)
    
def __friendly_min_cdist(XA, XB, max_memory_gb = 10.):
    """
    Calls scipy cdist and returns the min-values along each axis.
    To avoid memory problems, takes care that the supplied amount in GB is never crossed.
    
    @return (min distances along XA axes, min distance along XB axes)
    """
    # determine required memory in GB for cdist calculation 
    matrix_size_in_elements = XA.shape[0] * XB.shape[0]
    matrix_size_in_bits = matrix_size_in_elements * 64
    matrix_size_in_gb = matrix_size_in_bits / 1024. / 1024. / 1024.
    
    # determine number of required chunks and steplength
    no_chunks = int(math.ceil(matrix_size_in_gb / max_memory_gb))
    step_length = int(math.ceil(XB.shape[0] / float(no_chunks)))
    
    # prepare result variables
    min_dist_XA = None
    min_dist_XB = []
    
    # execute cdist step-wise and collect results
    t_passed = []
    mean = 0
    for chunk in xrange(no_chunks):
        t = time.time()
        
        slicer = slice(chunk * step_length, (chunk + 1) * step_length)
        
	if not silent:
	        sys.stdout.write('\rFriendly pairwise cdist computation chunk {} / {} (~{}s remaining)'.format(chunk + 1, no_chunks, int(mean * (no_chunks - chunk))))
        	#sys.stdout.write('{} GB chunk-size\n'.format(XA.shape[0] * XB[slicer].shape[0] * 64 / 1024. / 1024. / 1024.))
        	sys.stdout.flush()
        
        d = cdist(XA, XB[slicer])
        
        if None == min_dist_XA:
            min_dist_XA = d.min(1)
        else:
            min_dist_XA = numpy.minimum(min_dist_XA, d.min(1))
            
        min_dist_XB.extend(d.min(0))
        
        t_passed.append(time.time() - t)
        
        mean = sum(t_passed) / len(t_passed)
        
    if not silent: print
    
    # return min distances along XA and XB sets    
    return min_dist_XA, numpy.asarray(min_dist_XB)
    

if __name__ == "__main__":
	main()
