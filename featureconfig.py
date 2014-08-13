####
# Configuration file: Denotes the features to extract
####

from medpy.features.intensity import intensities, centerdistance, centerdistance_xdminus1, local_mean_gauss, local_histogram, hemispheric_difference, median, guassian_gradient_magnitude, shifted_mean_gauss
from medpy.features.intensity import indices as indices_feature

flair_tra = [
	('flair_tra', intensities, [], False),
	('flair_tra', local_mean_gauss, [3], True),
	('flair_tra', local_mean_gauss, [5], True),
	('flair_tra', local_mean_gauss, [7], True),
	('flair_tra', local_histogram, [11, 'image', (0, 100), 5, None, None, 'ignore', 0], False), #11 bins, 5*2=10mm region
	('flair_tra', local_histogram, [11, 'image', (0, 100), 10, None, None, 'ignore', 0], False), #11 bins, 10*2=20mm region
	('flair_tra', local_histogram, [11, 'image', (0, 100), 15, None, None, 'ignore', 0], False), #11 bins, 15*2=30mm region
	('flair_tra', centerdistance_xdminus1, [0], True),
	('flair_tra', centerdistance_xdminus1, [1], True),
	('flair_tra', centerdistance_xdminus1, [2], True)
]

dw_tra_b1000_dmean = [
	('dw_tra_b1000_dmean', intensities, [], False),
	('dw_tra_b1000_dmean', local_mean_gauss, [3], True),
	('dw_tra_b1000_dmean', local_mean_gauss, [5], True),
	('dw_tra_b1000_dmean', local_mean_gauss, [7], True),
	('dw_tra_b1000_dmean', local_histogram, [11, 'image', (0, 100), 5, None, None, 'ignore', 0], False), #11 bins, 5*2=10mm region
	('dw_tra_b1000_dmean', local_histogram, [11, 'image', (0, 100), 10, None, None, 'ignore', 0], False), #11 bins, 10*2=20mm region
	('dw_tra_b1000_dmean', local_histogram, [11, 'image', (0, 100), 15, None, None, 'ignore', 0], False) #11 bins, 15*2=30mm region
]

t1_sag_tfe = [
	('t1_sag_tfe', intensities, [], False),
	('t1_sag_tfe', local_mean_gauss, [3], True),
	('t1_sag_tfe', local_mean_gauss, [5], True),
	('t1_sag_tfe', local_mean_gauss, [7], True),
	('t1_sag_tfe', local_histogram, [11, 'image', (0, 100), 5, None, None, 'ignore', 0], False), #11 bins, 5*2=10mm region
	('t1_sag_tfe', local_histogram, [11, 'image', (0, 100), 10, None, None, 'ignore', 0], False), #11 bins, 10*2=20mm region
	('t1_sag_tfe', local_histogram, [11, 'image', (0, 100), 15, None, None, 'ignore', 0], False) #11 bins, 15*2=30mm region
]

features_to_extract = flair_tra + t1_sag_tfe + dw_tra_b1000_dmean


