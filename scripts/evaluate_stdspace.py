#!/usr/bin/python

"""
Roughly evaluates the registration to STD space.
arg1: the image to evalute
arg2: the std space template
arg3: the std space template's brain mask
"""

import sys

import numpy
from scipy.ndimage.interpolation import zoom
from scipy.ndimage.filters import gaussian_filter

from medpy.io import load, save, header
from medpy.metric.image import mutual_information

# Threshold: only pixel with a normalized intensity value above this in the brain mask are considered for the evaluation
thr = 0.9

def main():
	# load input images
	i, h = load(sys.argv[1])
	tpli, tplh = load(sys.argv[2])
	m, _ = load(sys.argv[3])

	# clean image
	i = clean(i)

	# smooth image
	i = gauss(i, h, sigma=6)

	# align both images
	i, h = align(i, h, tpli, tplh)

	# normalize both images
	i /= i.max()
	tpli /= tpli.max()

	# sum of squared differences
	ssd = numpy.sum(numpy.square(i[m>thr]-tpli[m>thr])) / float(len(i[m>thr]))
		
	# mutual information
	mu = mutual_information(i[m>thr], tpli[m>thr])

	# print
	print '{};{};{}'.format(sys.argv[1], ssd, mu)

def clean(i, cval = 0):
	"""
	Removes all nan and inf from the image and replace them with a constant value.
	"""
	i[numpy.isnan(i)] = 0
	i[numpy.isinf(i)] = 0
	return i

def gauss(i, h, sigma=6):
	"""
	Applies a gaussian smoothing to the image with the supplied kernel size in mmm.
	"""
	sigmas = [sigma * ps for ps in header.get_pixel_spacing(h)]
	i = gaussian_filter(i, sigma=sigmas)
	return i

def resample(img, hdr, ps):
	"""
	Resamples the image i to the provided pixel spacing.
	"""
	# compute zoom values
	zoom_factors = [old / float(new) for new, old in zip(ps, header.get_pixel_spacing(hdr))]

	# zoom image
	img = zoom(img, zoom_factors, order=2) # order = bspline order

	# set new voxel spacing
	header.set_pixel_spacing(hdr, ps)

	# return image and header
	return img, hdr


def align(i, h, refi, refh):
	"""
	Aligns the image i to the reference image refi.
	Note that this might include cropping and resampling.
	Note that only works for 3D images.

	@param i the input image to align to the reference image
	@param h the input image's header (Note: must be of type NifTi)
	@param refi the reference image
	@param refh the reference image's header

	@return i, h the aligned input image and its modified header
	"""	
	# resample input image if required
	if not numpy.all(numpy.asarray(header.get_pixel_spacing(h)) == numpy.asarray(header.get_pixel_spacing(refh))):
		i, h = resample(i, h, header.get_pixel_spacing(refh))

	# shift image to align origins
	origin_h = numpy.sign(h.get_qform()[0:3,0:3]).dot(header.get_offset(h))
	origin_refh = numpy.sign(refh.get_qform()[0:3,0:3]).dot(header.get_offset(refh))
	origin_difference_pixel = (origin_h - origin_refh) / numpy.asarray(header.get_pixel_spacing(h))
	# negative values: shift image 1 by this upon inserting (which is the same as cutting the output image)
	# positive values: cut image 1 by this at inserting and also cut right side by length of output image plus this value
	o = numpy.zeros(refi.shape, refi.dtype)
	o_slicer = []
	i_slicer = []
	for j, p in enumerate(origin_difference_pixel):
		if p >= 0:
			i_slicer.append(slice(0,      min(i.shape[j], o.shape[j] - abs(p))))
			o_slicer.append(slice(abs(p), min(i.shape[j] + abs(p), o.shape[j])))
		else:
			i_slicer.append(slice(abs(p), min(i.shape[j], o.shape[j] + abs(p))))
			o_slicer.append(slice(0,      min(i.shape[j] - abs(p), o.shape[j])))

	o[o_slicer] = i[i_slicer]
	header.set_offset(h, header.get_offset(refh))
	
	return o, h

if __name__ == "__main__":
	main()
