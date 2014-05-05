#!/bin/bash

#####
# Registers the FLAIR image to STD space, then transforms all sequences to it using SPM
#####

## Changelog
# 2014-04-02 adapted to use FLAIR as base image
# 2013-11-14 removed sform correction step, as no longer necessary with the new metadata approach in the pipeline
# 2013-11-11 added a step to remove final inf and nan value from the images
# 2013-11-11 changed to no combine the two registration steps, but rather executing them one after another
# 2013-11-07 fixed problem with SPM using sform instead of qform information
# 2013-11-06 added saveguard for when target file(s) already exist
# 2013-11-01 minor changes for bug-fixing
# 2013-10-31 created

# include shared information
source $(dirname $0)/include.sh

# constants
basesequence="flair_tra" # the base-sequence to warp with

# main code
tmpdir=`mktemp -d`

for i in "${images[@]}"; do
	log 2 "Processing case ${i}" "[$BASH_SOURCE:$FUNCNAME:$LINENO]"
	mkdircond ${stdspace}/${i}

	# continue if target file already exists (making assumption from basesequence to all sequences)
	if [ -f "${stdspace}/${i}/${basesequence}.${imgfiletype}" ]; then
		continue
	fi

	log 2 "Unpacking sequencespace images to .nii format" "[$BASH_SOURCE:$FUNCNAME:$LINENO]"
	for seq in "${sequences[@]}"; do
		runcond "medpy_convert.py ${sequencespace}/${i}/${seq}.${imgfiletype} ${tmpdir}/${seq}.nii"
	done

	log 2 "Create inverses of preliminary lesion mask in basesequence space" "[$BASH_SOURCE:$FUNCNAME:$LINENO]"
	runcond "${scripts}/invert.py ${sequencelesionsegmentation}/${i}/segmentation_post.${imgfiletype} ${tmpdir}/lesion_mask.nii"

	log 2 "Create and run SPM Normalize Estimate step" "[$BASH_SOURCE:$FUNCNAME:$LINENO]"
	runcond "${scripts}/make_spm_normalize_estimate.py ${tmpdir}/${basesequence}.nii ${tmpdir}/lesion_mask.nii ${tmpdir}/estimate.m"
	/usr/local/software/matlabR2014a/bin/matlab -nodisplay -nosplash -nodesktop -logfile "${tmpdir}/log" -r "addpath '${tmpdir}'; estimate;" > /dev/null

	log 2 "Check whether registration seemed to have failed" "[$BASH_SOURCE:$FUNCNAME:$LINENO]"
	runcond "${scripts}/check_spm_normalize_estimate_log.py ${tmpdir}/log 15"

	log 2 "Copy SPM/matlab basesequence-to-std transformation file to the target directory" "[$BASH_SOURCE:$FUNCNAME:$LINENO]"
	runcond "cp ${tmpdir}/${basesequence}_sn.mat ${stdspace}/${i}/${basesequence}.mat"

	log 2 "Create and run SPM Normalize Write / Warp step" "[$BASH_SOURCE:$FUNCNAME:$LINENO]"
	_images=""
	for seq in "${sequences[@]}"; do
		_images="${_images} ${tmpdir}/${seq}.nii"
	done
	runcond "${scripts}/make_spm_normalize_write.py ${tmpdir}/warp.m ${tmpdir}/${basesequence}_sn.mat ${_images}"
	/usr/local/software/matlabR2014a/bin/matlab -nodisplay -nosplash -nodesktop -logfile "${tmpdir}/wlog" -r "addpath '${tmpdir}'; warp;" > /dev/null

	log 2 "Move created images to the target directory" "[$BASH_SOURCE:$FUNCNAME:$LINENO]"
	for seq in "${sequences[@]}"; do
		runcond "medpy_convert.py ${tmpdir}/w${seq}.nii ${stdspace}/${i}/${seq}.${imgfiletype}"
	done

	log 2 "Clean created images" "[$BASH_SOURCE:$FUNCNAME:$LINENO]"
	for seq in "${sequences[@]}"; do
		runcond "${scripts}/clean.py ${stdspace}/${i}/${seq}.${imgfiletype}"
	done

	emptydircond ${tmpdir}
done

rmdircond ${tmpdir}
log 2 "Done." "[$BASH_SOURCE:$FUNCNAME:$LINENO]"
