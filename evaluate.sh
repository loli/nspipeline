#!/bin/bash

####
# Evaluate a segmentation in the original space instead of the sequences space.
####

## Changelog
# 2014-08-14 adapted to process multiple ground truth in cross-validation manner
# 20??-??-?? created

# include shared information
source $(dirname $0)/include.sh

# constants
SEQUENCESPACEONLY=false

# functions
function revert() {
	idx=$1
	vs=( $(voxelspacing "${segmentations}/${gtsettrain}/${idx}.${imgfiletype}") )
	vs2=$(joinarr " " ${vs[@]})
	runcond "imiImageResample -I ${sequencelesionsegmentation}/${gtsettrain}/${idx}/segmentation_post.${imgfiletype} -O ${tmpdir}/s${idx}.${imgfiletype} -R ${segmentations}/${gtsettrain}/${idx}.${imgfiletype} -s ${vs2} -b" /dev/null
	runcond "imiImageResample -I ${sequencebrainmasks}/${evaluationbasesequence}/${idx}.${imgfiletype} -O ${tmpdir}/m${idx}.${imgfiletype} -R ${segmentations}/${gtsettrain}/${idx}.${imgfiletype} -s ${vs2} -b" /dev/null
}

# main code
tmpdir=`mktemp -d`

for gtsettrain in ${gtsets[@]}; do
    
    # revert segmentation to original space for evaluation
    if [[ -z "$SEQUENCESPACEONLY" ]];then
        log 2 "Reverting segmentations...." "[$BASH_SOURCE:$FUNCNAME:$LINENO]"
        parallelize revert ${threadcount} allimages[@]
    fi

    for gtseteval in ${gtsets[@]}; do

        log 2 "#### EVAL SEGM CREATED WITH GT \"${gtsettrain}\" USING GT \"${gtseteval}\" ####" "[$BASH_SOURCE:$FUNCNAME:$LINENO]"

        if [[ -z "$SEQUENCESPACEONLY" ]];then
            log 2 "Evaluating in original space..." "[$BASH_SOURCE:$FUNCNAME:$LINENO]"
            runcond "${scripts}/evaluate_segmentations.py ${tmpdir}/s{}.${imgfiletype} ${segmentations}/${gtseteval}/{}.${imgfiletype} ${tmpdir}/m{}.${imgfiletype} $(joinarr " " ${allimages[@]})"
        fi

        log 2 "Evaluating in sequence space.." "[$BASH_SOURCE:$FUNCNAME:$LINENO]"
        runcond "${scripts}/evaluate_segmentations.py ${sequencelesionsegmentation}/${gtsettrain}/{}/segmentation_post.${imgfiletype} ${sequencesegmentations}/${gtseteval}/{}.${imgfiletype} ${sequencebrainmasks}/${evaluationbasesequence}/{}.${imgfiletype} $(joinarr " " ${allimages[@]})"

    done
    emptydircond ${tmpdir}
done
rmdircond "${tmpdir}"
