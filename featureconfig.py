####
# Configuration file: Denotes the features to extract
####

from medpy.features.intensity import intensities, centerdistance, centerdistance_xdminus1, local_mean_gauss, local_histogram, hemispheric_difference, median, guassian_gradient_magnitude
from medpy.features.intensity import indices as indices_feature

_features_to_extract = [
	('flair_tra', intensities, [], False),
	('flair_tra', local_mean_gauss, [3], True),
	('flair_tra', local_mean_gauss, [5], True),
	('flair_tra', local_mean_gauss, [7], True),
	#('flair_tra', guassian_gradient_magnitude, [5], True),
	#('flair_tra', median, [7], True),
	('flair_tra', local_histogram, [11, 'image', (0, 100), 5, None, None, 'ignore', 0], False), #11 bins, 5*2=10mm region
	('flair_tra', local_histogram, [11, 'image', (0, 100), 10, None, None, 'ignore', 0], False), #11 bins, 10*2=20mm region
	('flair_tra', local_histogram, [11, 'image', (0, 100), 15, None, None, 'ignore', 0], False), #11 bins, 15*2=30mm region
	('flair_tra', centerdistance_xdminus1, [0], True),
	('flair_tra', centerdistance_xdminus1, [1], True),
	('flair_tra', centerdistance_xdminus1, [2], True)
]

features_to_extract = [
	('t1_sag_tfe', intensities, [], False),
	('t1_sag_tfe', local_mean_gauss, [3], True),
	('t1_sag_tfe', local_mean_gauss, [5], True),
	('t1_sag_tfe', local_mean_gauss, [7], True),
	#('flair_tra', guassian_gradient_magnitude, [5], True),
	#('flair_tra', median, [7], True),
	('t1_sag_tfe', local_histogram, [11, 'image', (0, 100), 5, None, None, 'ignore', 0], False), #11 bins, 5*2=10mm region
	('t1_sag_tfe', local_histogram, [11, 'image', (0, 100), 10, None, None, 'ignore', 0], False), #11 bins, 10*2=20mm region
	('t1_sag_tfe', local_histogram, [11, 'image', (0, 100), 15, None, None, 'ignore', 0], False), #11 bins, 15*2=30mm region
	('t1_sag_tfe', centerdistance_xdminus1, [0], True),
	('t1_sag_tfe', centerdistance_xdminus1, [1], True),
	('t1_sag_tfe', centerdistance_xdminus1, [2], True)
]

#t1_sag_tfe
