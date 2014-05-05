#!/bin/bash

#####
# Roughly evaluates the results of the registration to t2space.
# This evaluation is not very informative, but might serve to detect failed registrations.
#####

## Changelog
# 2013-11-11 created

# include shared information
source $(dirname $0)/include.sh

# main code
log 2 "Evaluating against T2" "[$BASH_SOURCE:$FUNCNAME:$LINENO]"
for s in "${sequences[@]}"; do

	echo "image;mu" > ${t2space}/${s}.againstt2.eval.csv

	log 2 "Processing sequence ${s}" "[$BASH_SOURCE:$FUNCNAME:$LINENO]"
	for i in "${images[@]}"; do
		cmd="${scripts}/evaluate_mi.py ${t2space}/${i}/${s}.${imgfiletype} ${t2space}/${i}/t2_sag_tse.${imgfiletype}"
		$cmd >> ${t2space}/${s}.againstt2.eval.csv
	done
done
