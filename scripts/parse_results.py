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

# path changes

# own modules
from medpy.core import Logger
from medpy.io import load, save


# information
__author__ = "Oskar Maier"
__version__ = "r0.1.0, 2014-06-03"
__email__ = "oskar.maier@googlemail.com"
__status__ = "Release"
__description__ = """
                  Parses an evaluation result produced by evaluate.sh resp. 
		  evaluate_original.sh and converts it into csv or latex conform
		  output. Output is written to stdout.
                  
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

	# prepare signals and counters
	inside_evaluation_block = False
	inside_summary_block = False
	evaluation_blocks_encountered = 0

	# collector variables
	headers = []
	results = []
	summaries = []

	# parse evaluation file
	logger.info("Parsing the evaluation file.")
	with open(args.input, 'r') as f:
		for line in f.readlines():
			line = line.strip()
			if inside_evaluation_block:
				if 'WARNING' in line: # skip warnings
					continue
				elif 'average' in line: # summary block treated specially and marks approaching end
					inside_summary_block = True
					chunks = map(lambda x: x.strip(), line.split())
					summary.append(map(float, (chunks[2], chunks[4], chunks[6][:-1]))) # mean, std, median
				elif inside_summary_block: # stop condition
					inside_evaluation_block = False
					inside_summary_block = False
					evaluation_blocks_encountered +=1
					logger.debug("Parsing of evaluation block terminated.")
					headers.append(header)
					results.append(result)
					summaries.append(summary)
				else: # normal case evaluation line
					chunks = map(lambda x: x.strip(), line.split())
					result[chunks[0]] = map(float, chunks[1:])
			elif "Case" == line[:4]: # start condition
				inside_evaluation_block = True
				logger.debug("Evaluation block no. {} found.".format(evaluation_blocks_encountered + 1))
				header = map(lambda x: x.strip(), line.split())
				result = dict()
				summary = []
		if inside_summary_block: # stop condition
			inside_evaluation_block = False
			inside_summary_block = False
			evaluation_blocks_encountered +=1
			logger.debug("Parsing of evaluation block terminated.")
			headers.append(header)
			results.append(result)
			summaries.append(summary)

	# check data integrity
	logger.debug("Checking data integrity.")
	evaluation_blocks_to_remove = []
	for eb_no in range(evaluation_blocks_encountered):
		logger.debug("Checking data integrity of block no. {}.".format(eb_no + 1))
		expected_length = len(headers[eb_no]) - 1
		for case, entries in results[eb_no].iteritems():
			if not expected_length == len(entries):
				logger.warning("Inconsistency found: Case {} does not contain the expected number of {} quality measures, but {}. Removing block.".format(case, expected_length, len(entries)))
				evaluation_blocks_to_remove.append(eb_no)
		if not expected_length == len(summaries[eb_no]):
			logger.warning("Inconsistency found: The summaries do not contain the expected number of {} entries, but {}. Removing block.".format(expected_length, len(summaries[eb_no])))
			evaluation_blocks_to_remove.append(eb_no)
		

	if 0 == len(evaluation_blocks_to_remove):
		logger.info("The integrity of all evaluation blocks could be established.")
	else:
		logger.info("Removing {} of {} blocks from the further processing.".format(len(evaluation_blocks_to_remove), evaluation_blocks_encountered))
			
	for eb_no in evaluation_blocks_to_remove:
		del headers[eb_no]
		del results[eb_no]
		del summaries[eb_no]

	# print results
	logger.info("------------------------------")
	for eb_no, (header, result, summary) in enumerate(zip(headers, results, summaries)):
		print 'Evaluation block {}:'.format(eb_no + 1)
		print 'Note: All cases containing a nan or inf value where excluded from the computation of the summaries (except in boxplot case).'
		if 'latex' == args.format :
			print_latex(header, result, summary)
		elif 'csv' == args.format :
			print_csv(header, result, summary)
		elif 'boxplot' == args.format :
			print_boxplot(header, result, eb_no)
		logger.info("------------------------------")
	    
    	logger.info("Successfully terminated.")

def print_boxplot(header, result, prefix):
	"Prints the results ready for gnuplot parsing."
	import matplotlib.pyplot as plt

	# determine invalid data (defined as where DC = 0.0)
	invalid_case_indices = []
	if 'DC[0,1]' in header:
		dc_pos = header.index('DC[0,1]') - 1 # first is 'Cases'
		data = [d[dc_pos] for d in result.itervalues()]
		while 0.0 in data:
			invalid_case_indices.append(data.index(0.0))
			del data[data.index(0.0)]

	# create and save a plot for each evaluation measure
	for i, h in enumerate(header[1:]):
		# collect data by evaluation type
		data = [d[i] for d in result.itervalues()]
		
		# remove invalid cases from the data and collect them separately
		invalid = []
		for idx in invalid_case_indices:
			invalid.append(data[idx])
			del data[idx]
		
		# plot boxplot as well as data points
		plt.plot([1] * len(data), data, 'go')
		plt.boxplot(data, notch=1)
		#plt.plot([1] * len(invalid), invalid, 'ro')
		#plt.show()
		plt.savefig("tmp/{}_boxplot_{}.pdf".format(prefix, h))
		plt.clf()

def print_latex(header, result, summary):
	"Prints the parsed evaluation results in latex table format."
	l = lambda x: '{:.2f}'.format(round(x, 2))
	print 'Note: requires \\usepackage{booktabs} in preamble'
	print '\\begin{tabular}{lrrrrr}'
	print '\\toprule'
	print '{}\\\\'.format(' & '.join(header))
	print '\\midrule'
	for case, entries in sorted(result.items()):
		print '{} & {}\\\\'.format(case, ' & '.join(map(l, entries)))
	print '\\cmidrule(r){2-6}'
	print 'average & {}\\\\'.format(' & '.join([l(s[0]) for s in summary]))
	print 'std & {}\\\\'.format(' & '.join([l(s[1]) for s in summary]))
	print 'mean & {}\\\\'.format(' & '.join([l(s[2]) for s in summary]))
	print '\\bottomrule'
	print '\end{tabular}'

def print_csv(header, result, summary):
	"Prints the parsed evaluation results in csv table format."
	print '{}'.format(';'.join(header))
	for case, entries in sorted(result.items()):
		print '{};{}'.format(case, ';'.join(map(str, entries)))
	print 'average;{}'.format(';'.join([str(s[0]) for s in summary]))
	print 'std;{}'.format(';'.join([str(s[1]) for s in summary]))
	print 'mean;{}'.format(';'.join([str(s[2]) for s in summary]))

def getArguments(parser):
    "Provides additional validation of the arguments collected by argparse."
    return parser.parse_args()

def getParser():
    "Creates and returns the argparse parser object."
    parser = argparse.ArgumentParser(description=__description__)
    parser.add_argument('input', help='Evauation file.')
    #parser.add_argument('target', help='Target file resp. folder.')
    parser.add_argument('format', help='The format of the output.', choices=['latex', 'csv', 'boxplot'])
    parser.add_argument('-v', dest='verbose', action='store_true', help='Display more information.')
    parser.add_argument('-d', dest='debug', action='store_true', help='Display debug information.')
    parser.add_argument('-f', dest='force', action='store_true', help='Silently override existing output images.')
    return parser    

if __name__ == "__main__":
    main()        
