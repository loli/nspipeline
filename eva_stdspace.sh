#!/bin/bash

#####
# Roughly evaluates the results of the registration to stdspace.
# This evaluation is not very speaking, but might serve to detect failed registrations.
#####

## Changelog
# 2013-11-07 created

# include shared information
source $(dirname $0)/include.sh

# main code
log 2 "Evaluating against std brain" "[$BASH_SOURCE:$FUNCNAME:$LINENO]"
for s in "${sequences[@]}"; do

	echo "image;ssd;mu" > ${stdspace}/${s}.againststd.eval.csv

	log 2 "Processing sequence ${s}" "[$BASH_SOURCE:$FUNCNAME:$LINENO]"
	for i in "${images[@]}"; do
		cmd="${scripts}/evaluate_stdspace.py ${stdspace}/${i}/${s}.${imgfiletype} /home/maier/Applications/spm8/templates/T2.nii /home/maier/Applications/spm8/apriori/brainmask.nii"
		$cmd >> ${stdspace}/${s}.againststd.eval.csv
	done
done

log 2 "Evaluating against T2" "[$BASH_SOURCE:$FUNCNAME:$LINENO]"
for s in "${sequences[@]}"; do

	echo "image;seq;mu" > ${stdspace}/${s}.againstt2.eval.csv

	log 2 "Processing sequence ${s}" "[$BASH_SOURCE:$FUNCNAME:$LINENO]"
	for i in "${images[@]}"; do
		cmd="${scripts}/evaluate_mi.py ${stdspace}/${i}/${s}.${imgfiletype} ${stdspace}/${i}/t2_sag_tse.${imgfiletype}"
		$cmd >> ${stdspace}/${s}.againstt2.eval.csv
	done
done
