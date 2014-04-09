#!/bin/bash

#####
# Tranform all segmentation binary images to basesequence space.
#####

## Changelog
# 2013-11-15 created

# include shared information
source $(dirname $0)/include.sh

# constants
basesequence="flair_tra" # the base-sequence to use

# main code
tmpdir=`mktemp -d`
for i in "${images[@]}"; do
	log 2 "Tranforming expert segmentation of case ${i} to std space" "[$BASH_SOURCE:$FUNCNAME:$LINENO]"

	# continue if target file already exists
	if [ -f "${stdsegmentations}/${i}.${imgfiletype}" ]; then
		continue
	fi

	#log 2 "Unpacking original mask image to .nii format" "[$BASH_SOURCE:$FUNCNAME:$LINENO]"
	runcond "medpy_convert.py ${sequencesegmentations}/${i}.${imgfiletype} ${tmpdir}/${i}.nii"

	#log 2 "Create and run SPM Normalize Write / Warp step" "[$BASH_SOURCE:$FUNCNAME:$LINENO]"
	runcond "${scripts}/make_spm_normalize_write_mask.py ${tmpdir}/warp.m ${stdspace}/${i}/${basesequence}.mat ${tmpdir}/${i}.nii"
	/usr/local/software/matlabR2014a/bin/matlab -nodisplay -nosplash -nodesktop -r "addpath '${tmpdir}'; warp;" > ${tmpdir}/log #/dev/null

	#log 2 "Move created mask to the target directory" "[$BASH_SOURCE:$FUNCNAME:$LINENO]"
	runcond "medpy_convert.py ${tmpdir}/w${i}.nii ${stdsegmentations}/${i}.${imgfiletype}"

	#log 2 "Clean created mask" "[$BASH_SOURCE:$FUNCNAME:$LINENO]"
	runcond "${scripts}/clean.py ${stdsegmentations}/${i}.${imgfiletype}"
	echo $tmpdir
	exit 0
	emptydircond ${tmpdir}
done
rmdircond ${tmpdir}
log 2 "Done." "[$BASH_SOURCE:$FUNCNAME:$LINENO]"
