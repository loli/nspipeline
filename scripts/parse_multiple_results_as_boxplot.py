#!/usr/bin/python

"""
Parses evaluation files and creates comparitive boxplots of all evluation measures.
"""

# build-in modules
import argparse
import logging

# third-party modules

# path changes

# own modules
from medpy.core import Logger
from colourconfig import *

# constants
NAMES = [''] #['default', 'tuned'] # names for the evaluation files
EXLUDED_FILES = ['37', '44']

# information
__author__ = "Oskar Maier"
__version__ = "r0.1.0, 2014-06-22"
__email__ = "oskar.maier@googlemail.com"
__status__ = "Release"
__description__ = """
                  Parses evaluation files and creates comparitive boxplots of all
                  evluation measures.
                  
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

    # check names constant
    if not len(NAMES) == len(args.inputs):
        raise Exception('Please provide as many names to the NAMES constant as you pass evaluation files to the script.')

    # collector variables
    dms = []
    hds = []
    assds = []
    precisions = []
    recalls = []

    # parse evaluation files
    logger.info("Parsing the evaluation files.")
    for fn in args.inputs:
        eva = Evaluation()
        eva.parse(fn, EXLUDED_FILES)
        dms.append(eva.metric_result('DC[0,1]', -1))
        hds.append(eva.metric_result('HD(mm)', -1))
        assds.append(eva.metric_result('P2C(mm)', -1))
        precisions.append(eva.metric_result('prec.', -1))
        recalls.append(eva.metric_result('recall', -1))
        
    # create and save a boxplot for each metric
    make_boxplot(NAMES, dms, args.output, 'DM')
    make_boxplot(NAMES, hds, args.output, 'HD')
    make_boxplot(NAMES, assds, args.output, 'ASSD')
    make_boxplot(NAMES, precisions, args.output, 'precision')
    make_boxplot(NAMES, recalls, args.output, 'recall')
        
    

def __figure_set_colors(fig):
    import matplotlib

    ax = fig.add_subplot(1, 1, 1)
    for child in ax.get_children():
        if isinstance(child, matplotlib.spines.Spine):
            child.set_color(c_plotlines)

    ax.tick_params(axis='x', colors=c_text)
    ax.tick_params(axis='y', colors=c_text)


def make_boxplot(names, values, trgdir, name):
    "Make and save multi-element boxplot."
    import matplotlib.pyplot as plt

    # create ans stype plot
    fig = plt.figure()
    ax = set_figure_style(fig)
        
    # plot boxplot and style
    layout = plt.boxplot(values, notch=True, sym='o', patch_artist=True, widths=.3)
    set_boxplot_style(layout)

    # enable grid on y axes and hide behind boxplots
    ax.yaxis.grid(True)
    ax.set_axisbelow(True)
    
    # set xtick names
    plt.xticks(range(1, len(names)+1), names)

    #plt.show()
    plt.savefig("{}/exp01_reference_seqspace_{}.pdf".format(trgdir, name))


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

    def result(self, evaluation_block = 0):
        return self.results[evaluation_block]
        
    def metric_result(self, metric, evaluation_block = 0):
        return self.__get_metric(metric, evaluation_block)

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
    parser.add_argument('output', help='The target directory for the graphs.')
    parser.add_argument('inputs', nargs='+', help='The evaluation files.')
    parser.add_argument('-v', dest='verbose', action='store_true', help='Display more information.')
    parser.add_argument('-d', dest='debug', action='store_true', help='Display debug information.')
    parser.add_argument('-f', dest='force', action='store_true', help='Silently override existing output images.')
    return parser    

if __name__ == "__main__":
    main()        
