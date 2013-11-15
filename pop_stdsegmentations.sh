#!/bin/bash

#####
# Tranform all segmentation binary images to T2 space.
#####

## Changelog
# 2013-11-15 created

# include shared information
source $(dirname $0)/include.sh

# main code
tmpdir=`mktemp -d`
for i in "${images[@]}"; do
	log 2 "Tranforming expert segmentation of case ${i} to std space" "[$BASH_SOURCE:$FUNCNAME:$LINENO]"

	# continue if target file already exists
	if [ -f "${stdsegmentations}/${i}.${imgfiletype}" ]; then
		continue
	fi

	#log 2 "Unpacking original mask image to .nii format" "[$BASH_SOURCE:$FUNCNAME:$LINENO]"
	cmd="medpy_convert.py ${t2segmentations}/${i}.${imgfiletype} ${tmpdir}/${i}.nii"
	$cmd

	#log 2 "Create and run SPM Normalize Write / Warp step" "[$BASH_SOURCE:$FUNCNAME:$LINENO]"
	cmd="${scripts}/make_spm_normalize_write_mask.py ${tmpdir}/warp.m ${stdspace}/${i}/t2_sag_tse.mat ${tmpdir}/${i}.nii"
	$cmd
	matlab -nodisplay -nosplash -nodesktop -r "addpath '${tmpdir}'; warp;" > ${tmpdir}/log #/dev/null

	#log 2 "Move created mask to the target directory" "[$BASH_SOURCE:$FUNCNAME:$LINENO]"
	cmd="medpy_convert.py ${tmpdir}/w${i}.nii ${stdsegmentations}/${i}.${imgfiletype}"
	$cmd

	#log 2 "Clean created mask" "[$BASH_SOURCE:$FUNCNAME:$LINENO]"
	cmd="${scripts}/clean.py ${stdsegmentations}/${i}.${imgfiletype}"
	$cmd

	emptydircond ${tmpdir}
done
rmdircond ${tmpdir}
log 2 "Done." "[$BASH_SOURCE:$FUNCNAME:$LINENO]"
