#!/usr/bin/python

"""
Parses an evaluation result produced by evaluate.sh resp. 
evaluate_original.sh and converts it into csv or latex conform
output. Output is written to stdout.
"""

# build-in modules
import argparse
import logging
import itertools

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
                  Parses multiple evaluation results and creates a graph over a varying
		  scale.
		  Only the average values are taken into account for the computation.
		  If multiple evaluation results exists in a file, only the last one is
		  considered.
                  
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

	# collector variables
	dms = []
	hds = []
	assds = []
	precisions = []
	recalls = []
	
	# parse evaluation files
	logger.info("Parsing the evaluation files.")
	parameters = []
	for fn in args.inputs:
		parameters.append(int(fn.split('.')[2])) #4
		eva = Evaluation()
		eva.parse(fn, EXLUDED_FILES)
		dms.append(eva.mean('DC[0,1]', -1))
		hds.append(eva.mean('HD(mm)', -1))
		assds.append(eva.mean('P2C(mm)', -1))
		precisions.append(eva.mean('prec.', -1))
		recalls.append(eva.mean('recall', -1))

	# print summary
	#print 'Metric\tmean\tstd\tmedian'
	#print 'DM\t{}\t{}\t{}'.format(numpy.mean(dms), numpy.std(dms), numpy.median(dms))
	#print 'HD\t{}\t{}\t{}'.format(numpy.mean(hds), numpy.std(hds), numpy.median(hds))
	#print 'ASSD\t{}\t{}\t{}'.format(numpy.mean(assds), numpy.std(assds), numpy.median(assds))
	#print 'Prec.\t{}\t{}\t{}'.format(numpy.mean(precisions), numpy.std(precisions), numpy.median(precisions))
	#print 'Recall\t{}\t{}\t{}'.format(numpy.mean(recalls), numpy.std(recalls), numpy.median(recalls))

	#print len(dms), len(hds), len(assds), len(precisions), len(recalls), len(args.inputs)
	if not len(dms) == len(hds) == len(assds) == len(precisions) == len(recalls) == len(args.inputs) == len(parameters):
		raise Exception("Could not parse all files. Breaking.")

	#plot(args.output, parameters, '#depth', (dms, precisions, recalls), (assds,), ('DC/F1', 'Prec.', 'Rec.'), ('ASSD',))
	#plot_minsamples(args.output, parameters, '#samples', (dms, precisions, recalls), (None,), ('DC/F1', 'Prec.', 'Rec.'), (None,))
	#plot_maxfeatures(args.output, parameters, '#features', (dms, precisions, recalls), (None,), ('DC/F1', 'Prec.', 'Rec.'), (None,))
	#plot_depth(args.output, parameters, '#tree-depth', (dms, precisions, recalls), (None,), ('DC/F1', 'Prec.', 'Rec.'), (None,))
	#plot_trees(args.output, parameters, '#forests', (dms, precisions, recalls), (None,), ('DC/F1', 'Prec.', 'Rec.'), (None,))
	#plot_onesided(args.output, parameters, 'sequence combination', (dms, precisions, recalls), ('DC/F1', 'Prec.', 'Rec.'))
	plot_sequence_combinations(args.output, parameters, 'sequence combination', (dms, ), (r'$DC/F_1$', ))
	
    	logger.info("Successfully terminated.")

def plot_twosided(filename, x, x_label, left, right, left_labels, right_labels):
	"Creates a plot with two y-scales and saves it."
	import matplotlib.pyplot as plt

	fig = plt.figure()

	ax = fig.add_subplot(111)
	for idx in range(len(left)):
		_y = [u for (v,u) in sorted(zip(x,left[idx]))] # sort y-data according to x
		_x = sorted(x) # sort x-data
		ax.plot(_x, _y, ':o', label=left_labels[idx])
	
	ax2 = ax.twinx()
	for idx in range(len(right)):
		_y = [u for (v,u) in sorted(zip(x,right[idx]))] # sort y-data according to x
		_x = sorted(x) # sort x-data
		ax2.plot(_x, _y, ':o', label=right_labels[idx])
		
	ax.legend(loc=0)
	ax2.legend(loc=0)
	ax.grid()	
	ax.set_xlabel(x_label)
	#ax.axvline(200, linewidth=2, color='y')# default value
	#ax.set_ylabel('[0,1]')
	#ax2.set_ylabel('mm')
	
	plt.show()
	#plt.savefig(filename)

def plot_onesided(filename, x, x_label, left, left_labels):
	"Creates a plot with on y-scale and saves it."
	import matplotlib.pyplot as plt

	fig = plt.figure()

	ax = fig.add_subplot(111)
	for idx in range(len(left)):
		_y = [u for (v,u) in sorted(zip(x,left[idx]))] # sort y-data according to x
		_x = sorted(x) # sort x-data
		ax.plot(_x, _y, ':o', label=left_labels[idx])
		
	ax.legend(loc=0)
	ax.grid()	
	ax.set_xlabel(x_label)
	
	#plt.show()
	plt.savefig(filename)

def _enhance(sequences):
	order = ['FL', 'DW', 'AD', 'T1', 'T2']
	ret = []
	for o in order:
		if o in sequences:
			ret.append(o)
		else:
			ret.append('| ')
	return ret
	

def plot_sequence_combinations(filename, x, x_label, left, left_labels):
	import matplotlib.pyplot as plt
	import matplotlib

	# prepare x-axes labels
	sequences = ['FL', 'DW', 'AD', 'T1', 'T2']
	#sequences = ['F', 'D', 'A', 'T', 'T']
	combinations = []
	for l in range(1, len(sequences) + 1):
		combinations.extend(itertools.combinations(sequences, l))
	combinations = map(_enhance, combinations)

	# prepare figure
	fig = plt.figure()
	ax = fig.add_subplot(111)

	# prepare and draw background rectangles
	## Rectangle( (x,y)-corner, width, height, color=name|hexcode, alpha=float)
	rect1 = matplotlib.patches.Rectangle((-0.5, 0),  5, 1, color='#00FFFF', alpha=0.5)
	rect2 = matplotlib.patches.Rectangle(( 4.5, 0), 10, 1, color='#FFFF00', alpha=0.5)
	rect3 = matplotlib.patches.Rectangle((14.5, 0), 10, 1, color='#00FFFF', alpha=0.5)
	rect4 = matplotlib.patches.Rectangle((24.5, 0), 5, 1, color='#FFFF00', alpha=0.5)
	rect5 = matplotlib.patches.Rectangle((29.5, 0), 1, 1, color='#00FFFF', alpha=0.5)
	rect_flair = matplotlib.patches.Rectangle((-0.5, 0.6), len(left[0]), 0.1, color='#FF0000', alpha=0.3)
	ax.add_patch(rect1)
	ax.add_patch(rect2)
	ax.add_patch(rect3)
	ax.add_patch(rect4)
	ax.add_patch(rect5)
	ax.add_patch(rect_flair)
	ax.axhline(0.631, linewidth=2, color='y') # default value
	
	# make main figure
	for idx in range(len(left)):
		_y = [u for (v,u) in sorted(zip(x,left[idx]))] # sort y-data according to x
		_x = sorted(x) # sort x-data
		plt.plot(_x, _y, 'o', label=left_labels[idx], markersize=10.)
		
	ax.legend(loc=0)
	ax.grid()
	plt.xticks(range(len(combinations)), ['\n'.join(x) for x in combinations], fontsize='x-small', family='monospace')
	#plt.xlabel(['\n'.join(x) for x in combinations], )
	plt.xlim(-0.5, len(_x) - 0.5)
	plt.ylim(0.1, 0.75)

	# make upper x-axes
	ax2 = ax.twiny()
	ax2.set_xlim(-0.5, len(_x) - 0.5)
	ax2.tick_params(length=0, width=0, labelsize=15)  # labelsize, labelcolor='#0000FF'
	ax2.set_xticks([2, 9.5, 19.5, 27, 30])
	ax2.set_xticklabels([1, 2, 3, 4, 5])
	ax2.set_xlabel('#sequences')

	# show/plot figure
	plt.subplots_adjust(left=0.08, right=0.92, top=0.9, bottom=0.17)
	#plt.show()
	plt.savefig(filename)

def plot_minsamples(filename, x, x_label, left, right, left_labels, right_labels):
	"Creates a plot with two y-scales and saves it."
	import matplotlib.pyplot as plt

	fig = plt.figure()

	ax = fig.add_subplot(111)
	for idx in range(len(left)):
		_y = [u for (v,u) in sorted(zip(x,left[idx]))] # sort y-data according to x
		_x = sorted(x) # sort x-data
		ax.plot(_x, _y, ':o', label=left_labels[idx])
		
	ax.legend(loc=0)
	ax.grid()	
	ax.set_xlabel(x_label)
	ax.axvline(2, linewidth=2, color='y') # default value
	
	#plt.show()
	plt.savefig(filename, bbox_inches='tight')

def plot_maxfeatures(filename, x, x_label, left, right, left_labels, right_labels):
	"Creates a plot with two y-scales and saves it."
	import matplotlib.pyplot as plt

	fig = plt.figure()

	ax = fig.add_subplot(111)
	for idx in range(len(left)):
		_y = [u for (v,u) in sorted(zip(x,left[idx]))] # sort y-data according to x
		_x = sorted(x) # sort x-data
		ax.plot(_x, _y, ':o', label=left_labels[idx])
		
	ax.legend(loc=0)
	ax.grid()	
	ax.set_xlabel(x_label)
	ax.axvline(6, linewidth=2, color='y') # default value
	
	#plt.show()
	plt.savefig(filename)

def plot_trees(filename, x, x_label, left, right, left_labels, right_labels):
	"Creates a plot with two y-scales and saves it."
	import matplotlib.pyplot as plt

	fig = plt.figure()
	ax = fig.add_subplot(111)

	for idx in range(len(left)):
		_y = [u for (v,u) in sorted(zip(x,left[idx]))] # sort y-data according to x
		_x = sorted(x) # sort x-data
		ax.plot(_x, _y, ':o', label=left_labels[idx])
		
	ax.legend(loc=0)
	ax.grid()	
	ax.set_xlabel(x_label)
	ax.axvline(200, linewidth=2, color='y') # default value
	
	#plt.show()
	plt.savefig(filename)

def plot_depth(filename, x, x_label, left, right, left_labels, right_labels):
	"Creates a plot with two y-scales and saves it."
	import matplotlib.pyplot as plt

	fig = plt.figure()
	ax = fig.add_subplot(111)

	for idx in range(len(left)):
		_y = [u for (v,u) in sorted(zip(x,left[idx]))] # sort y-data according to x
		_x = sorted(x) # sort x-data
		ax.plot(_x, _y, ':o', label=left_labels[idx])
		
	ax.legend(loc=0)
	ax.grid()	
	ax.set_xlabel(x_label)
	ax.axvline(100, linewidth=2, color='y') # max encountered value	
	
	#plt.show()
	plt.savefig(filename)

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
    parser.add_argument('output', help='The target image/file.')
    parser.add_argument('inputs', nargs='+', help='The input evaluation files.')
    parser.add_argument('-v', dest='verbose', action='store_true', help='Display more information.')
    parser.add_argument('-d', dest='debug', action='store_true', help='Display debug information.')
    parser.add_argument('-f', dest='force', action='store_true', help='Silently override existing output images.')
    return parser    

if __name__ == "__main__":
    main()        
