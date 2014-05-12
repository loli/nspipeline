#!/usr/bin/python

# Compares to evaluation results for their significants according to the paired t-test.
# Note: The paired t-test calculates the T-test on TWO RELATED samples of scores. This is
# a two-sided test for the null hypothesis that 2 related or repeated samples have
# identical average (expected) values.
# @see: http://en.wikipedia.org/wiki/T-test#Dependent_t-test_for_paired_samples

# arg1: the first evaluation file
# arg2: the second evaluation file
# arg3: pass anything to print out the case-wise results and differences

pborder = 0.05

import sys
import numpy
from scipy.stats import ttest_rel

def parse_evaluation_file(fn):
	parse = False
	results = {}
	with open(fn, 'r') as f:
		for line in f.readlines():
			line = line.strip()
			if 'Average' in line or 'average' in line:
				parse = False
			if parse:
				vals = line.split('\t')
				results[vals[0]] = map(float, vals[1:])
			if 'Case' == line[:4]:
				parse = True
				headers = line.split('\t')
	if 0 == len(results):
		print 'Error: Invalid evaluation file {}.'.format(fn)
		sys.exit(-1)
	return results, headers

r1, h1 = parse_evaluation_file(sys.argv[1])
r2, h2 = parse_evaluation_file(sys.argv[2])
print_casewise = len(sys.argv) > 3

if not r1.keys() == r2.keys():
	print 'WARNING: The cases in the two evaluation files differ.'
	print 'Symmetric difference is: {}'.format(set.symmetric_difference(set(r1.iterkeys()), set(r2.iterkeys())))
	print 'Continuing, but considering common cases only: {}'.format(set.intersection(set(r1.iterkeys()), set(r2.iterkeys())))

	for key in set.difference(set(r1.keys()), r2.keys()):
		del r1[key]
	for key in set.difference(set(r2.keys()), r1.keys()):
		del r2[key]

if not h1 == h2:
	print 'ERROR: Incompatible quality metrics.'
	print 'Evaluation file {} contains {}.'.format(sys.argv[1], h1)
	print 'Evaluation file {} contains {}.'.format(sys.argv[2], h2)
	sys.exit(-1)


# print case-wise if requested
if print_casewise:
	print '\nCase\tRun\t{}'.format('\t'.join(h1[1:]))
	for key in sorted(r1):
		print '{}\tr1\t{}'.format(key, '\t'.join(map(str, r1[key])))
		print '\tr2\t{}'.format('\t'.join(map(str, r2[key])))
		print '\tdiff\t{}'.format('\t'.join(map(str, numpy.subtract(r1[key], r2[key]))))
	print


# remove failed cases
failedno = 0
failedkey = []
for key, scores in list(r1.iteritems()):
	if not numpy.all(numpy.isfinite(scores)):
		failedno += 1
		failedkey.append(key)
		del r1[key]
		del r2[key]
for key, scores in list(r2.iteritems()):
	if not numpy.all(numpy.isfinite(scores)):
		failedno += 1
		failedkey.append(key)
		del r1[key]
		del r2[key]
if not 0 == failedno:
	print 'WARNING: Statistics only computed for {} of {} cases, as some segmentations failed in at least one of the compared evaluation results!'.format(len(r1), len(r1) + failedno)


# print statistics
print 'Statistical significance between results obtained for run r1 ({}) against run r2 ({}) on {} cases:'.format(sys.argv[1], sys.argv[2], len(r1))
print 'Applied test: Paired t-test for two related samples of scores.'
print 'Metric\tmean-r1\tmean-r2\tdiff\tt-value\tp-value\tsignificant<{}'.format(pborder)
for idx, metric in enumerate(h1[1:]):
	r1v = [x[idx] for x in r1.itervalues()]
	r2v = [x[idx] for x in r2.itervalues()]
	t, p = ttest_rel(r1v, r2v)
	print '{}\t{:4.3f}\t{:4.3f}\t{:4.3f}\t{:4.3f}\t{:4.3f}\t{}'.format(metric, numpy.mean(r1v), numpy.mean(r2v), numpy.mean(r1v)-numpy.mean(r2v), t, p, p<pborder)
	





