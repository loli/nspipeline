#!/usr/bin/python

####
# Checks a the output created by a SPM Normalize Estimate operation for potentially failed registrations. If detected, prints a warning.
# arg1: the log file containing the output
# arg2: the FWHM score threshold
####

import sys

def main():
	logfile = sys.argv[1]
	fwhm_threshold = float(sys.argv[2])

	with open(logfile, 'r') as f:
		fwhm_found = False
		for line in f.readlines():
			line = line.strip()
			if 'FWHM' in line:
				fwhm_found = True
				segments = line.split('=')
				fwhm_value = float(segments[1].strip().split(' ')[0])
				fwhm_std = float(segments[2].strip().split(' ')[0])
			elif fwhm_found:
				print 'Registration terminated with FWHM {} +/- {}.'.format(fwhm_value, fwhm_std)
				if fwhm_value > fwhm_threshold:
					print 'WARNING: Registration terminated with a score FWHM value of {}, which is above the threshold {}.'.format(fwhm_value, fwhm_threshold)
				fwhm_found = False

if __name__ == "__main__":
    main()
