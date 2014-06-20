#!/usr/bin/python

"""
Parses an evaluation result produced by evaluate.sh resp. 
evaluate_original.sh and computes correlation with an
ordenal or continuous second variable.
"""

# Notes on statistical rank correlation measures:
# 1. Rank correlation between two continuous variables
#	Pearons r is suitable to look for a linear relationship between two continuous variables.
#	It employs the natural ranking i.e. takes the ral-valued distances between the values into account.
#	A normal distribution of at least one of the two compared variables is assumed. If this does not hold true, the Spearman rho should be used.
# 2. Rank correlation between two ordenal or an ordenal and a continuous variable
#	Spearman rho should be used here.
#	It ranks the variables first (i.e. 1, 2, 3, ...) and then searched for correlations between their ranks.
#	No normal distribution is assumed.
# 3. (Rank) correlation between continuous and nominal variables
#	No idea yet.

# build-in modules
import argparse
import logging

# third-party modules
import numpy
from scipy.stats import spearmanr, pearsonr

# own modules
from medpy.core import Logger

# constants
EXLUDED_CASES = ['37', '44'] #['37', '44']

VAR_FILE = '/data_humbug1/maier/Temp_Pipeline/NeuroImagePipeline/00original/IMAGECHARACTERISTICS_RANKED.csv'
VAR_IDENTIFIERS = ['cid', 'db', 'lesiontype', 'lesionload', 'lesionage', 'nihss', 'wmls', 'flair_noise', 't1_noise', 'dw_noise', 'multifocal'] # first one is case id
VAR_CORR_MEASURES = [None, spearmanr, spearmanr, pearsonr, pearsonr, pearsonr, spearmanr, spearmanr, spearmanr, spearmanr, spearmanr]

#REPLACEMENTS = [inf, 

# information
__author__ = "Oskar Maier"
__version__ = "r0.1.0, 2014-06-20"
__email__ = "oskar.maier@googlemail.com"
__status__ = "Release"
__description__ = """
                  Parses an evaluation result produced by evaluate.sh resp. 
		  evaluate_original.sh and computes correlation with an
		  ordenal or continuous second variable.
		  All measures are compared, the correlation results printed
		  and the scatter plots saved in the target directory.
                  
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

	# parse file with variables, extract case ids and sort everything according to them
	variables = numpy.genfromtxt(VAR_FILE, delimiter=';', skip_header=1, autostrip=True)
	variables = variables[numpy.argsort(variables[:,0])] # sort array by first column (case ids)
	var_ids = variables[:,0]

	# remove excluded cases
	for ecidx in EXLUDED_CASES:
		ecrow = numpy.where(var_ids == int(ecidx))[0]
		variables = numpy.vstack((variables[:ecrow], variables[ecrow+1:]))
		var_ids = var_ids[~(int(ecidx) == var_ids)]
	
	# parse evaluation files
	logger.info("Parsing the evaluation files.")
	eva = Evaluation()
	eva.parse(args.input, EXLUDED_CASES)
	headers = eva.header(-1)
	scores = eva.data(-1) # dm, hd, assd, prec., recall

	# iterate over variables
	for vidx in range(1, len(VAR_IDENTIFIERS)):
		var_name = VAR_IDENTIFIERS[vidx]
		var_data = var_ids = variables[:,vidx]
		
		# iterate over evaluation measures
		for eidx in range(len(headers)):
			emsr_name = headers[eidx]
			emsr_data = __get_score_ordered(scores, eidx)
			#print emsr_name
			#print emsr_data

			# compute respective correlation and print
			corr, p = VAR_CORR_MEASURES[vidx](emsr_data, var_data)			
			print '{:<10} vs. {:<13}:\t{:< 7.2}\t{:< 10.2}{}'.format(emsr_name, var_name, corr, p, VAR_CORR_MEASURES[vidx].__name__)

			# plot data s scatterplot
			plot(emsr_data, emsr_name, var_data, var_name, corr, p, VAR_CORR_MEASURES[vidx].__name__, args.output)


def plot(x, x_label, y, y_label, corr, p, t, directory):
	"Creates a scatterplot."
	import matplotlib.pyplot as plt
	import matplotlib

	fig = plt.figure()
	ax = fig.add_subplot(1, 1, 1)
	for child in ax.get_children():
	    if isinstance(child, matplotlib.spines.Spine):
		child.set_color('#004b5a')

	ax.tick_params(axis='x', colors='#004b5a')
	ax.tick_params(axis='y', colors='#004b5a')

	plt.grid()
	plt.title('{}: corr={:.2}, p={:.2}'.format(t, corr, p), color='#004b5a')
	plt.xlabel(x_label, color='#004b5a')
	plt.ylabel(y_label, color='#004b5a')

	plt.scatter(x, y, s=100, facecolors='#eac43d', edgecolors='#b08a06', alpha=1.)
	
	#plt.show()
	plt.savefig('{}/{}_{}.pdf'.format(directory, x_label, y_label))


def __get_score_ordered(scores, idx):
	"""
	Returns the evaluation measure at index idx of the scores ordered by the case id.
	"""	
	return [x[1][idx] for x in sorted(scores.items())]


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

	def header(self, evaluation_block = 0):
		return self.headers[evaluation_block]

	def data(self, evaluation_block = 0):
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
    parser.add_argument('output', help='The target directory.')
    parser.add_argument('input', help='The evaluation file to correlate with.')
    parser.add_argument('-v', dest='verbose', action='store_true', help='Display more information.')
    parser.add_argument('-d', dest='debug', action='store_true', help='Display debug information.')
    parser.add_argument('-f', dest='force', action='store_true', help='Silently override existing output images.')
    return parser    

if __name__ == "__main__":
    main()        
