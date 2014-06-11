#!/usr/bin/python

"""
Parses an evaluation result produced by evaluate.sh resp. 
evaluate_original.sh and converts it into csv or latex conform
output. Output is written to stdout.
"""

# build-in modules
import argparse
import logging

# third-party modules
import numpy

# path changes

# own modules
from medpy.core import Logger
from medpy.io import load, save

# constants
EXLUDED_FILES = ['37', '44']


# information
__author__ = "Oskar Maier"
__version__ = "r0.1.0, 2014-06-04"
__email__ = "oskar.maier@googlemail.com"
__status__ = "Release"
__description__ = """
                  Parses multiple time results and prints them in orderly fashion.
                  
                  Copyright (C) 2013 Oskar Maier
                  This program comes with ABSOLUTELY NO WARRANTY; This is free software,
                  and you are welcome to redistribute it under certain conditions; see
                  the LICENSE file or <http://www.gnu.org/licenses/> for details.   
                  """

# code
def main():
	args = getArguments(getParser())

	# prepare logger
	logger = Logger.getInstance()
	if args.debug: logger.setLevel(logging.DEBUG)
	elif args.verbose: logger.setLevel(logging.INFO)

	for fn in args.inputs:
		print fn
		with open(fn, 'r') as f:
			for line in f.readlines():
				line = line.strip()
				if 'elapsed' in line:
					chunks = line.split()
					print chunks[0], chunks[2], chunks[3]
				elif 'real' in line:
					_tmp = line.split()[1]
				elif 'user' in line:
					print line.split()[1], _tmp

def getArguments(parser):
    "Provides additional validation of the arguments collected by argparse."
    return parser.parse_args()

def getParser():
    "Creates and returns the argparse parser object."
    parser = argparse.ArgumentParser(description=__description__)
    parser.add_argument('inputs', nargs='+', help='The input time files.')
    parser.add_argument('-v', dest='verbose', action='store_true', help='Display more information.')
    parser.add_argument('-d', dest='debug', action='store_true', help='Display debug information.')
    return parser    

if __name__ == "__main__":
    main()        
