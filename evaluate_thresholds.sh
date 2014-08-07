#!/bin/bash

####
# Evaluate the results of a segmentation
####

# include shared information
source $(dirname $0)/include.sh

# constants
thresholds=('0.175' '0.2' '0.225' '0.25' '0.275' '0.3')

dryrun=true

# main code
log 2 "Evluating for different thresholds" "[$BASH_SOURCE:$FUNCNAME:$LINENO]"
for t in "${thresholds[@]}"; do
    log 2 "Applying threshold ${t}" "[$BASH_SOURCE:$FUNCNAME:$LINENO]"
    function threshold () {
        i=$1
        runcond "${scripts}/threshold.py ${sequencelesionsegmentation}/${i}/probabilities.nii.gz $t ${sequencelesionsegmentation}/${i}/segmentation.nii.gz"
    }
    parallelize threshold ${threadcount} images[@]
    
    log 2 "Evaluating" "[$BASH_SOURCE:$FUNCNAME:$LINENO]"
    runcond "${scripts}/evaluate_segmentations.py ${sequencelesionsegmentation}/{}/segmentation.${imgfiletype} ${sequencesegmentations}/{}.${imgfiletype} ${sequencebrainmasks}/{}.${imgfiletype} $(joinarr " " ${images[@]})"
done

