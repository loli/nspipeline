#!/usr/bin/python

"""
Parses an evaluation result produced by evaluate.sh resp. 
evaluate_original.sh and converts it into csv or latex conform
output. Output is written to stdout.
"""

# build-in modules
import argparse
import logging
import sys

# third-party modules
import numpy

# path changes

# own modules
from medpy.core import Logger
from medpy.io import load, save

# information
__author__ = "Oskar Maier"
__version__ = "r0.1.0, 2014-06-10"
__email__ = "oskar.maier@googlemail.com"
__status__ = "Release"
__description__ = """
                  Parses an evaluation file under the exclusion of some selected cases.
                  
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

	# prepare arguments
	excluded_cases = sys.argv[2:]
	
	# parse evaluation file
	eva = Evaluation()
	eva.parse(args.input, excluded_cases)
	print 'Parsed a total of {} cases after the exclusion of {}.'.format(eva.case_count(-1), excluded_cases)
	print 'DC', eva.mean('DC[0,1]', -1)
	print 'HD', eva.mean('HD(mm)', -1)
	print 'ASSD', eva.mean('P2C(mm)', -1)
	print 'Prec.', eva.mean('prec.', -1)
	print 'Recall', eva.mean('recall', -1)
	
    	logger.info("Successfully terminated.")

class Evaluation:
	"""
	Object constructed from an evaluation file.
	Call parse() method to initialize.
	"""
	def __init__(self):
		self.logger = Logger.getInstance()
		self.headers = []
		self.results = []
		self.parsed = False
		
	def parse(self, file_name, exluded_cases = []):
		"""Parse an evaluation file and initialize the object excluding the given cases."""
		# check if already parsed
		if self.parsed:
			raise Exception("Can only parse once, please initialize another Evaluation object.")
	
		# prepare signals and counters
		inside_evaluation_block = False
		inside_summary_block = False
		evaluation_blocks_encountered = 0

		# parse evaluation file
		self.logger.info("Parsing evaluation file {}.".format(file_name))
		with open(file_name, 'r') as f:
			for line in f.readlines():
				line = line.strip()
				if inside_evaluation_block:
					if 'WARNING' in line: # skip warnings
						continue
					elif 'average' in line: # stop condition approaching
						inside_summary_block = True
					elif inside_summary_block: # stop condition reached
						inside_evaluation_block = False
						inside_summary_block = False
						evaluation_blocks_encountered +=1
						self.logger.debug("Parsing of evaluation block terminated.")
						self.headers.append(header)
						self.results.append(result)
					else: # normal case evaluation line
						chunks = map(lambda x: x.strip(), line.split())
						if not chunks[0] in exluded_cases:
							result[chunks[0]] = map(float, chunks[1:])
				elif "Case" == line[:4]: # start condition
					inside_evaluation_block = True
					self.logger.debug("Evaluation block no. {} found.".format(evaluation_blocks_encountered + 1))
					header = map(lambda x: x.strip(), line.split())[1:]
					result = dict()
			if inside_summary_block: # stop condition reached
				inside_evaluation_block = False
				inside_summary_block = False
				evaluation_blocks_encountered +=1
				self.logger.debug("Parsing of evaluation block terminated.")
				self.headers.append(header)
				self.results.append(result)

		# set stated to parsed
		self.parsed = True

	def evaluation_block_count(self):
		return len(self.headers)
	
	def case_count(self, evaluation_block = 0):
		return len(self.results[evaluation_block])

	def header_count(self, evaluation_block = 0):
		return len(self.headers[evaluation_block])

	def headers(self, evaluation_block = 0):
		return self.headers[evaluation_block]

	def results(self, evaluation_block = 0):
		return self.results[evaluation_block]

	def mean(self, metric, evaluation_block = 0):
		return numpy.mean(self.__get_metric(metric, evaluation_block))

	def median(self, metric, evaluation_block = 0):
		return numpy.median(self.__get_metric(metric, evaluation_block))

	def std(self, metric, evaluation_block = 0):
		return numpy.std(self.__get_metric(metric, evaluation_block))

	def __get_metric(self, metric, evaluation_block = 0):
		if not self.__is_int(metric):
			metric = self.headers[evaluation_block].index(metric)
		return [x[metric] for x in self.results[evaluation_block].values()]

	def __is_int(self, s):
	    try:
		int(s)
		return True
	    except ValueError:
		return False

def getArguments(parser):
    "Provides additional validation of the arguments collected by argparse."
    return parser.parse_args()

def getParser():
    "Creates and returns the argparse parser object."
    parser = argparse.ArgumentParser(description=__description__)
    parser.add_argument('input', help='The evaluation file to parse.')
    parser.add_argument('cases', nargs='+', help='The cases to exclude.')
    parser.add_argument('-v', dest='verbose', action='store_true', help='Display more information.')
    parser.add_argument('-d', dest='debug', action='store_true', help='Display debug information.')
    return parser    

if __name__ == "__main__":
    main()        
