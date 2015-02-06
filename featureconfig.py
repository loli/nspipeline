####
# Configuration file: Denotes the features to extract
####

from medpy.features.intensity import intensities, centerdistance, centerdistance_xdminus1, local_mean_gauss, local_histogram, hemispheric_difference, median, guassian_gradient_magnitude, shifted_mean_gauss
from medpy.features.intensity import indices as indices_feature

T2 = [
	('T2', intensities, [], False),
	('T2', local_mean_gauss, [3], True),
	('T2', local_mean_gauss, [5], True),
	('T2', local_mean_gauss, [7], True),
	('T2', local_histogram, [11, 'image', (0, 100), 5, None, None, 'ignore', 0], False), #11 bins, 5*2=10mm region
	('T2', local_histogram, [11, 'image', (0, 100), 10, None, None, 'ignore', 0], False), #11 bins, 10*2=20mm region
	('T2', local_histogram, [11, 'image', (0, 100), 15, None, None, 'ignore', 0], False), #11 bins, 15*2=30mm region
	('T2', centerdistance_xdminus1, [0], True),
	('T2', centerdistance_xdminus1, [1], True),
	('T2', centerdistance_xdminus1, [2], True)
]

FLAIR = [
	('FLAIR', intensities, [], False),
	('FLAIR', local_mean_gauss, [3], True),
	('FLAIR', local_mean_gauss, [5], True),
	('FLAIR', local_mean_gauss, [7], True),
	('FLAIR', local_histogram, [11, 'image', (0, 100), 5, None, None, 'ignore', 0], False), #11 bins, 5*2=10mm region
	('FLAIR', local_histogram, [11, 'image', (0, 100), 10, None, None, 'ignore', 0], False), #11 bins, 10*2=20mm region
	('FLAIR', local_histogram, [11, 'image', (0, 100), 15, None, None, 'ignore', 0], False) #11 bins, 15*2=30mm region
]

T1mprage = [
	('T1mprage', intensities, [], False),
	('T1mprage', local_mean_gauss, [3], True),
	('T1mprage', local_mean_gauss, [5], True),
	('T1mprage', local_mean_gauss, [7], True),
	('T1mprage', local_histogram, [11, 'image', (0, 100), 5, None, None, 'ignore', 0], False), #11 bins, 5*2=10mm region
	('T1mprage', local_histogram, [11, 'image', (0, 100), 10, None, None, 'ignore', 0], False), #11 bins, 10*2=20mm region
	('T1mprage', local_histogram, [11, 'image', (0, 100), 15, None, None, 'ignore', 0], False) #11 bins, 15*2=30mm region
]

T1mprageCE = [
	('T1mprageCE', intensities, [], False),
	('T1mprageCE', local_mean_gauss, [3], True),
	('T1mprageCE', local_mean_gauss, [5], True),
	('T1mprageCE', local_mean_gauss, [7], True),
	('T1mprageCE', local_histogram, [11, 'image', (0, 100), 5, None, None, 'ignore', 0], False), #11 bins, 5*2=10mm region
	('T1mprageCE', local_histogram, [11, 'image', (0, 100), 10, None, None, 'ignore', 0], False), #11 bins, 10*2=20mm region
	('T1mprageCE', local_histogram, [11, 'image', (0, 100), 15, None, None, 'ignore', 0], False) #11 bins, 15*2=30mm region
]

PD = [
	('PD', intensities, [], False),
	('PD', local_mean_gauss, [3], True),
	('PD', local_mean_gauss, [5], True),
	('PD', local_mean_gauss, [7], True),
	('PD', local_histogram, [11, 'image', (0, 100), 5, None, None, 'ignore', 0], False), #11 bins, 5*2=10mm region
	('PD', local_histogram, [11, 'image', (0, 100), 10, None, None, 'ignore', 0], False), #11 bins, 10*2=20mm region
	('PD', local_histogram, [11, 'image', (0, 100), 15, None, None, 'ignore', 0], False) #11 bins, 15*2=30mm region
]

PM_WM = [
	('PM_WM', intensities, [], False),
	('PM_WM', local_mean_gauss, [3], True),
	('PM_WM', local_mean_gauss, [5], True),
	('PM_WM', local_mean_gauss, [7], True),
	('PM_WM', local_histogram, [11, 'image', (0, 100), 5, None, None, 'ignore', 0], False), #11 bins, 5*2=10mm region
	('PM_WM', local_histogram, [11, 'image', (0, 100), 10, None, None, 'ignore', 0], False), #11 bins, 10*2=20mm region
	('PM_WM', local_histogram, [11, 'image', (0, 100), 15, None, None, 'ignore', 0], False) #11 bins, 15*2=30mm region
]

PM_GM = [
	('PM_GM', intensities, [], False),
	('PM_GM', local_mean_gauss, [3], True),
	('PM_GM', local_mean_gauss, [5], True),
	('PM_GM', local_mean_gauss, [7], True),
	('PM_GM', local_histogram, [11, 'image', (0, 100), 5, None, None, 'ignore', 0], False), #11 bins, 5*2=10mm region
	('PM_GM', local_histogram, [11, 'image', (0, 100), 10, None, None, 'ignore', 0], False), #11 bins, 10*2=20mm region
	('PM_GM', local_histogram, [11, 'image', (0, 100), 15, None, None, 'ignore', 0], False) #11 bins, 15*2=30mm region
]

PM_CSF = [
	('PM_CSF', intensities, [], False),
	('PM_CSF', local_mean_gauss, [3], True),
	('PM_CSF', local_mean_gauss, [5], True),
	('PM_CSF', local_mean_gauss, [7], True),
	('PM_CSF', local_histogram, [11, 'image', (0, 100), 5, None, None, 'ignore', 0], False), #11 bins, 5*2=10mm region
	('PM_CSF', local_histogram, [11, 'image', (0, 100), 10, None, None, 'ignore', 0], False), #11 bins, 10*2=20mm region
	('PM_CSF', local_histogram, [11, 'image', (0, 100), 15, None, None, 'ignore', 0], False) #11 bins, 15*2=30mm region
]

features_to_extract = T2 + FLAIR + T1mprage + PD


