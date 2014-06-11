#!/usr/bin/python

"""
Joins a number of binary masks into an single uint file with consecutive numbers. Where
intersection occurs, the higer numbers are given priority.
"""

# build-in modules
import sys

# third-party modules
import numpy

# path changes

# own modules
from medpy.io import load, save

# information

# code
def main():
	output_file = sys.argv[1]
	input_files = sys.argv[2:]

	mask_identifier = 1

	output_data, output_header = load(input_files[0])
	output_data = output_data.astype(numpy.uint8)
	output_data[output_data > 0] = mask_identifier

	
	for input_file in input_files[1:]:
		mask_identifier += 1
		input_data, _ = load(input_file)
		output_data[input_data > 0] = mask_identifier

	save(output_data, output_file, output_header, True)
		

if __name__ == "__main__":
    main()
