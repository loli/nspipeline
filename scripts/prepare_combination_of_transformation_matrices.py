#!/usr/bin/python

####
# Reads in and parses a elastix transformation file, extracting the euler transform parameters and converting them into a proper rigid transformation matrix.
# Then creates a Matlab script to combine the matrix with one found in a provided SPM warping matlab struct, creating a new such struct.
# arg1: the elastix transformation file
# arg2: the input SPM warp struct
# arg3: the output SPM war struct
# arg4: the target script name
####

import sys

import numpy

from math import cos, sin

def main():
	elastixtf = sys.argv[1]
	inputspms = sys.argv[2]
	outputspms = sys.argv[3]
	target = sys.argv[4]
	
	rigid_matrix = extract_rigid_tranformation_matrix(elastixtf)
	rigid_matrix_string = ' ; ' .join([', '.join(map(str, row)) for row in rigid_matrix])

	script = script_template.format(elastixtf, inputspms, outputspms, inputspms, rigid_matrix_string, outputspms)

	with open(target, 'w') as f:
		f.write(script)

def extract_rigid_tranformation_matrix(elastix_tf_file):
	# read transformation file
	with open(elastix_tf_file, 'r') as f:
		for line in f.readlines():
			line = line.strip()
			if "TransformParameters" in line:
				line = line.split(' ')
				parameters = line[1:]
				parameters[-1] = parameters[-1][:-1]
				parameters = map(float, parameters)
				break

	# prepare extracted parameters
	x_r, y_r, z_r = parameters[:3] #radians
	x_t, y_t, z_t = parameters[3:] # translations

	# create rotation matrices (in homogeneous coordinates)
	rotation_x = numpy.asarray([[1,        0, 	  0, 0],
				    [0, cos(x_r), -sin(x_r), 0],
				    [0, sin(x_r),  cos(x_r), 0],
				    [0,        0, 	  0, 1]])
	rotation_y = numpy.asarray([[ cos(y_r), 0, sin(y_r), 0],
				    [	     0, 1, 	  0, 0],
				    [-sin(y_r), 0, cos(y_r), 0],
				    [	     0, 0,        0, 1]])
	rotation_z = numpy.asarray([[cos(z_r), -sin(z_r), 0, 0],
				    [sin(z_r),  cos(z_r), 0, 0],
				    [	    0, 	       0, 1, 0],
				    [	    0, 	       0, 0, 1]])

	# create transaltion matrix (in homogeneous coordinates)
	translation = numpy.asarray([[0, 0, 0, x_t],
				     [0, 0, 0, y_t],
				     [0, 0, 0, z_t],
				     [0, 0, 0,   0]])

	# combine matrices to final rigid tranformation matrix
	rigid = numpy.dot(numpy.dot(rotation_x, rotation_y), rotation_z) + translation

	return rigid

script_template = """
% Script to combine the elastix rigid transformation from {} with the SPM affine transformation from {} and save them into the new SPM struct file {}.

S = load('{}');
affine_transformation_matrix = S.Affine;
rigid_transformation_matrix = [{}];
final_transformation_matrix = affine_transformation_matrix * rigid_transformation_matrix;
S.Affine = final_transformation_matrix;
save('{}', '-struct', 'S');

exit;
"""

if __name__ == "__main__":
    main()
