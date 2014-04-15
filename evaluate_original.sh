#!/bin/bash

####
# Evaluate a segmentation in the original space instead of the sequences space.
####

# include shared information
source $(dirname $0)/include.sh

# main code
tmpdir=`mktemp -d`

function revert()
{
	idx=$1
	vs=( $(voxelspacing "${segmentations}/${idx}.${imgfiletype}") )
	vs2=$(joinarr " " ${vs[@]})
	runcond "imiImageResample -I ${sequencelesionsegmentation}/${idx}/segmentation_post.${imgfiletype} -O ${tmpdir}/s${idx}.${imgfiletype} -R ${segmentations}/${idx}.${imgfiletype} -s ${vs2} -b" /dev/null
	runcond "imiImageResample -I ${sequencebrainmasks}/${idx}.${imgfiletype} -O ${tmpdir}/m${idx}.${imgfiletype} -R ${segmentations}/${idx}.${imgfiletype} -s ${vs2} -b" /dev/null
}

# revert segmentation to original space for evaluation
log 2 "Reverting segmentations...." "[$BASH_SOURCE:$FUNCNAME:$LINENO]"
parallelize revert ${threadcount} images[@]

log 2 "Evaluating in original space..." "[$BASH_SOURCE:$FUNCNAME:$LINENO]"
runcond "${scripts}/evaluate_segmentations.py ${tmpdir}/s{}.${imgfiletype} ${segmentations}/{}.${imgfiletype} ${tmpdir}/m{}.${imgfiletype} $(joinarr " " ${images[@]})"

log 2 "Evaluating in sequence space.." "[$BASH_SOURCE:$FUNCNAME:$LINENO]"
runcond "${scripts}/evaluate_segmentations.py ${sequencelesionsegmentation}/{}/segmentation_post.${imgfiletype} ${sequencesegmentations}/{}.${imgfiletype} ${sequencebrainmasks}/{}.${imgfiletype} $(joinarr " " ${images[@]})"

emptydircond ${tmpdir}
rmdircond "${tmpdir}"
