#!/usr/bin/python

"""
Extracts the hemispheric difference features from an image.
arg1: the input image
arg2: the active sides sigma for gaussian smoothing in mm
arg3: the reference sides sigma for gaussian smoothing in mm
arg4: the cut plane dimension (usually coronal plane, mostly 0)
arg5: the elements to take into account for the interpolation of the central slice
arg6: the output image
"""

import sys

import numpy
from scipy.interpolate import interp1d
from scipy.ndimage.filters import gaussian_filter

from medpy.io import load, save, header

# constants

def main():
	i, h = load(sys.argv[1])

	# fetch commandline parameters
	CUT_PLANE = int(sys.argv[4]) # dimension in which to cut = coronal plane
	SIGMA_ACTIVE = int(sys.argv[2]) # gaussian smoothing kernel in mm for the active image
	SIGMA_REFERENCE = int(sys.argv[3]) # gaussian smoothing kernel in mm for the reference image
	INTERPOLATION_RANGE = int(sys.argv[5]) # how many neighbouring values to take into account when interpolating the medial longitudinal fissure line

	# split the head into a dexter and sinister half along the saggital plane
	# this is assumed to be consistent with a cut of the brain along the medial longitudinal fissure, thus separating it into its hemispheres
	medial_longitudinal_fissure = int(i.shape[CUT_PLANE] / 2)
	medial_longitudinal_fissure_excluded = i.shape[CUT_PLANE] % 2

	slicer = [slice(None)] * i.ndim
	slicer[CUT_PLANE] = slice(None, medial_longitudinal_fissure)
	left_hemisphere = i[slicer]

	slicer[CUT_PLANE] = slice(medial_longitudinal_fissure + medial_longitudinal_fissure_excluded, None)
	right_hemisphere = i[slicer]

	# flip right hemisphere image along cut plane
	slicer[CUT_PLANE] = slice(None, None, -1)
	right_hemisphere = right_hemisphere[slicer]

	# substract once left from right and once right from left hemisphere
	right_hemisphere_difference = substract(right_hemisphere, left_hemisphere, SIGMA_ACTIVE, SIGMA_REFERENCE, header.get_pixel_spacing(h)) # * -1
	left_hemisphere_difference = substract(left_hemisphere, right_hemisphere, SIGMA_ACTIVE, SIGMA_REFERENCE, header.get_pixel_spacing(h))

	# re-flip right hemisphere image to original orientation
	right_hemisphere_difference = right_hemisphere_difference[slicer]

	# estimate the medial longitudinal fissure if required
	if 1 == medial_longitudinal_fissure_excluded:
		left_slicer = [slice(None)] * i.ndim
		right_slicer = [slice(None)] * i.ndim
		left_slicer[CUT_PLANE] = slice(-1 * INTERPOLATION_RANGE, None)
		right_slicer[CUT_PLANE] = slice(None, INTERPOLATION_RANGE)
		interp_data_left = left_hemisphere_difference[left_slicer]
		interp_data_right = right_hemisphere_difference[right_slicer]
		interp_indices_left = range(-1 * interp_data_left.shape[CUT_PLANE], 0)
		interp_indices_right = range(1, interp_data_right.shape[CUT_PLANE] + 1)
		interp_data = numpy.concatenate((left_hemisphere_difference[left_slicer], right_hemisphere_difference[right_slicer]), CUT_PLANE)
		interp_indices = numpy.concatenate((interp_indices_left, interp_indices_right), 0)
		medial_longitudinal_fissure_estimated = interp1d(interp_indices, interp_data, kind='cubic', axis=CUT_PLANE)(0)
		# add singleton dimension
		slicer[CUT_PLANE] = numpy.newaxis
		medial_longitudinal_fissure_estimated = medial_longitudinal_fissure_estimated[slicer]

	# stich images back together
	if 1 == medial_longitudinal_fissure_excluded:
		hemisphere_difference = numpy.concatenate((left_hemisphere_difference, medial_longitudinal_fissure_estimated, right_hemisphere_difference), CUT_PLANE)
	else:
		hemisphere_difference = numpy.concatenate((left_hemisphere_difference, right_hemisphere_difference), CUT_PLANE)

	# save result
	save(hemisphere_difference, sys.argv[6], h)

def substract(active, reference, active_sigma, reference_sigma, pixel_spacing):
	"""
	Smoothes both images and then substracts the reference from the active image.
	"""
	active_kernel = [active_sigma * ps for ps in pixel_spacing]
	active_smoothed = gaussian_filter(active, sigma = active_kernel)

	reference_kernel = [reference_sigma * ps for ps in pixel_spacing]
	reference_smoothed = gaussian_filter(reference, sigma = reference_kernel)

	#save(active_smoothed, 'l{}'.format(sys.argv[2]), h)
	#save(reference_smoothed, 'r{}'.format(sys.argv[2]), h)

	return active_smoothed - reference_smoothed

if __name__ == "__main__":
	main()


