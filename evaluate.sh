#!/bin/bash

####
# Evaluate the results of a segmentation
####

# include shared information
source $(dirname $0)/include.sh

# main code
log 2 "Compute overall evaluation" "[$BASH_SOURCE:$FUNCNAME:$LINENO]"
runcond "${scripts}/evaluate_segmentations.py ${sequencelesionsegmentation}/{}/segmentation_post.${imgfiletype} ${sequencesegmentations}/{}.${imgfiletype} ${sequencebrainmasks}/{}.${imgfiletype} $(joinarr " " ${images[@]})"

