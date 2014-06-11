####
# Configuration file: Denotes the features to extract
####

from medpy.features.intensity import intensities, centerdistance, centerdistance_xdminus1, local_mean_gauss, local_histogram, hemispheric_difference, median, guassian_gradient_magnitude, shifted_mean_gauss
from medpy.features.intensity import indices as indices_feature

_flair = [
	('flair_tra', intensities, [], False),
	#('flair_tra', shifted_mean_gauss, [(2, 2, 2), 3], True),
	#('flair_tra', shifted_mean_gauss, [(2, 2, -2), 3], True),
	#('flair_tra', shifted_mean_gauss, [(2, -2, 2), 3], True),
	#('flair_tra', shifted_mean_gauss, [(-2, 2, 2), 3], True),
	#('flair_tra', shifted_mean_gauss, [(2, -2, -2), 3], True),
	#('flair_tra', shifted_mean_gauss, [(-2, 2, -2), 3], True),
	#('flair_tra', shifted_mean_gauss, [(-2, -2, 2), 3], True),
	#('flair_tra', shifted_mean_gauss, [(-2, -2, -2), 3], True),
	#('flair_tra', shifted_mean_gauss, [(1, 1, 1), 3], True),
	#('flair_tra', shifted_mean_gauss, [(1, 1, -1), 3], True),
	#('flair_tra', shifted_mean_gauss, [(1, -1, 1), 3], True),
	#('flair_tra', shifted_mean_gauss, [(-1, 1, 1), 3], True),
	#('flair_tra', shifted_mean_gauss, [(1, -1, -1), 3], True),
	#('flair_tra', shifted_mean_gauss, [(-1, 1, -1), 3], True),
	#('flair_tra', shifted_mean_gauss, [(-1, -1, 1), 3], True),
	#('flair_tra', shifted_mean_gauss, [(-1, -1, -1), 3], True),
	#('flair_tra', shifted_mean_gauss, [(4, 4, 4), 3], True),
	#('flair_tra', shifted_mean_gauss, [(4, 4, -4), 3], True),
	#('flair_tra', shifted_mean_gauss, [(4, -4, 4), 3], True),
	#('flair_tra', shifted_mean_gauss, [(-4, 4, 4), 3], True),
	#('flair_tra', shifted_mean_gauss, [(4, -4, -4), 3], True),
	#('flair_tra', shifted_mean_gauss, [(-4, 4, -4), 3], True),
	#('flair_tra', shifted_mean_gauss, [(-4, -4, 4), 3], True),
	#('flair_tra', shifted_mean_gauss, [(-4, -4, -4), 3], True),
	('flair_tra', local_mean_gauss, [3], True),
	('flair_tra', local_mean_gauss, [5], True),
	('flair_tra', local_mean_gauss, [7], True),
	#('flair_tra', guassian_gradient_magnitude, [5], True),
	#('flair_tra', median, [7], True),
	#('flair_tra', indices_feature, [], True),
	('flair_tra', local_histogram, [11, 'image', (0, 100), 5, None, None, 'ignore', 0], False), #11 bins, 5*2=10mm region
	('flair_tra', local_histogram, [11, 'image', (0, 100), 10, None, None, 'ignore', 0], False), #11 bins, 10*2=20mm region
	('flair_tra', local_histogram, [11, 'image', (0, 100), 15, None, None, 'ignore', 0], False), #11 bins, 15*2=30mm region
	('flair_tra', centerdistance_xdminus1, [0], True),
	('flair_tra', centerdistance_xdminus1, [1], True),
	('flair_tra', centerdistance_xdminus1, [2], True)
]

_dw = [
	('dw_tra_b1000_dmean', intensities, [], False),
	('dw_tra_b1000_dmean', local_mean_gauss, [3], True),
	('dw_tra_b1000_dmean', local_mean_gauss, [5], True),
	('dw_tra_b1000_dmean', local_mean_gauss, [7], True),
	#('dw_tra_b1000_dmean', guassian_gradient_magnitude, [5], True),
	#('dw_tra_b1000_dmean', median, [7], True),
	('dw_tra_b1000_dmean', local_histogram, [11, 'image', (0, 100), 5, None, None, 'ignore', 0], False), #11 bins, 5*2=10mm region
	('dw_tra_b1000_dmean', local_histogram, [11, 'image', (0, 100), 10, None, None, 'ignore', 0], False), #11 bins, 10*2=20mm region
	('dw_tra_b1000_dmean', local_histogram, [11, 'image', (0, 100), 15, None, None, 'ignore', 0], False) #11 bins, 15*2=30mm region
	#('dw_tra_b1000_dmean', centerdistance_xdminus1, [0], True),
	#('dw_tra_b1000_dmean', centerdistance_xdminus1, [1], True),
	#('dw_tra_b1000_dmean', centerdistance_xdminus1, [2], True)
]

_adc = [
	('adc_tra', intensities, [], False),
	('adc_tra', local_mean_gauss, [3], True),
	('adc_tra', local_mean_gauss, [5], True),
	('adc_tra', local_mean_gauss, [7], True),
	#('adc_tra', guassian_gradient_magnitude, [5], True),
	#('adc_tra', median, [7], True),
	('adc_tra', local_histogram, [11, 'image', (0, 100), 5, None, None, 'ignore', 0], False), #11 bins, 5*2=10mm region
	('adc_tra', local_histogram, [11, 'image', (0, 100), 10, None, None, 'ignore', 0], False), #11 bins, 10*2=20mm region
	('adc_tra', local_histogram, [11, 'image', (0, 100), 15, None, None, 'ignore', 0], False) #11 bins, 15*2=30mm region
	#('adc_tra', centerdistance_xdminus1, [0], True),
	#('adc_tra', centerdistance_xdminus1, [1], True),
	#('adc_tra', centerdistance_xdminus1, [2], True)
]

_t1 = [
	('t1_sag_tfe', intensities, [], False),
	('t1_sag_tfe', local_mean_gauss, [3], True),
	('t1_sag_tfe', local_mean_gauss, [5], True),
	('t1_sag_tfe', local_mean_gauss, [7], True),
	#('t1_sag_tfe', guassian_gradient_magnitude, [5], True),
	#('t1_sag_tfe', median, [7], True),
	('t1_sag_tfe', local_histogram, [11, 'image', (0, 100), 5, None, None, 'ignore', 0], False), #11 bins, 5*2=10mm region
	('t1_sag_tfe', local_histogram, [11, 'image', (0, 100), 10, None, None, 'ignore', 0], False), #11 bins, 10*2=20mm region
	('t1_sag_tfe', local_histogram, [11, 'image', (0, 100), 15, None, None, 'ignore', 0], False) #11 bins, 15*2=30mm region
	#('t1_sag_tfe', centerdistance_xdminus1, [0], True),
	#('t1_sag_tfe', centerdistance_xdminus1, [1], True),
	#('t1_sag_tfe', centerdistance_xdminus1, [2], True)
]

_t2 = [
	('t2_sag_tse', intensities, [], False),
	('t2_sag_tse', local_mean_gauss, [3], True),
	('t2_sag_tse', local_mean_gauss, [5], True),
	('t2_sag_tse', local_mean_gauss, [7], True),
	#('t2_sag_tse', guassian_gradient_magnitude, [5], True),
	#('t2_sag_tse', median, [7], True),
	('t2_sag_tse', local_histogram, [11, 'image', (0, 100), 5, None, None, 'ignore', 0], False), #11 bins, 5*2=10mm region
	('t2_sag_tse', local_histogram, [11, 'image', (0, 100), 10, None, None, 'ignore', 0], False), #11 bins, 10*2=20mm region
	('t2_sag_tse', local_histogram, [11, 'image', (0, 100), 15, None, None, 'ignore', 0], False) #11 bins, 15*2=30mm region
	#('t2_sag_tse', centerdistance_xdminus1, [0], True),
	#('t2_sag_tse', centerdistance_xdminus1, [1], True),
	#('t2_sag_tse', centerdistance_xdminus1, [2], True)
]

features_to_extract = _flair # + _t1 + _t2 + _dw + _adc


