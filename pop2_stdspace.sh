#!/bin/bash

#####
# Registers the T2 image to STD space, then transforms all sequences to it using SPM
#####

## Changelog
# 2010-10-31 created

# include shared information
source $(dirname $0)/include.sh

# main code
tmpdir=`mktemp -d`

for i in "${images[@]}"; do
	log 2 "Processing case $idx" "[$BASH_SOURCE:$FUNCNAME:$LINENO]"

	log 2 "Unpacking original images to .nii format" "[$BASH_SOURCE:$FUNCNAME:$LINENO]"
	for s in "${sequences[@]}"; do
		cmd="medpy_convert.py ${originals}/${i}/${seq}.${imgfiletype} ${tmpdir}/${seq}.nii"
		$cmd
	done

	log 2 "Create inverses of preliminary lesion mask in T2 space" "[$BASH_SOURCE:$FUNCNAME:$LINENO]"
	cmd="${scripts}/invert.py ${t2segmentations}/${i}.${imgfiletype} ${tmpdir}/lesion_mask.nii"
	$cmd

	log 2 "Create and run SPM Normalize Estimate step" "[$BASH_SOURCE:$FUNCNAME:$LINENO]"
	cmd="${scripts}/make_spm_normalize_estimate.py ${tmpdir}/${seq}.nii ${tmpdir}/lesion_mask.nii"
	$cmd
	cmd="matlab -nodisplay -nosplash -nodesktop -r \"addpath '${tmpdir}'; estimate;\" > ${tmpdir}/log"
	$cmd

	log 2 "Check whether registration seemed to have failed" "[$BASH_SOURCE:$FUNCNAME:$LINENO]"
	cmd="${scripts}/check_spm_normalize_estimate_log.py ${tmpdir}/log"
	$cmd

	log 2 "Create matlab scripts that modify the transformation parameters to include the inter-sequence registration performed by elastix" "[$BASH_SOURCE:$FUNCNAME:$LINENO]"
	for s in "${sequences[@]}"; do
		if [ "${s}" == "t2_sag_tse" ]; then
			continue
		fi
		cmd="${scripts}/prepare_combination_of_transformation_matrices.py ${tmpdir} ${tmpdir}/t2_sag_tse_sn.mat ${seq}"
		$cmd
	done

	log 2 "Execute the created matlab scripts" "[$BASH_SOURCE:$FUNCNAME:$LINENO]"
	for s in "${sequences[@]}"; do
		if [ "${s}" == "t2_sag_tse" ]; then
			continue
		fi
		cmd="matlab -nodisplay -nosplash -nodesktop -r \"addpath '${tmpdir}'; ${seq}_combine;\" > /dev/null"
		$cmd
	done

	log 2 "Create and run SPM Normalize Write / Warp step" "[$BASH_SOURCE:$FUNCNAME:$LINENO]"
	for s in "${sequences[@]}"; do
		cmd="${scripts}/make_spm_normalize_write.py ${tmpdir}/${seq}.nii ${tmpdir}/${seq}_sn.mat"
		$cmd
		cmd="matlab -nodisplay -nosplash -nodesktop -r \"addpath '${tmpdir}'; ${seq}_warp;\" > /dev/null"
		$cmd
	done

	emptydircond ${tmpdir}
done

rmdircond ${tmpdir}
log 2 "Done." "[$BASH_SOURCE:$FUNCNAME:$LINENO]"
