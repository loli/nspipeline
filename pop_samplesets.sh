#!/bin/bash

#####
# Samples a number of training samples randomly using a set of selected features.
#####

## Changelog
# 2013-05-08 created

# include shared information
source $(dirname $0)/include.sh

# main code
log 2 "Drawing a training set for each leave-one-out case using stratified random sampling" "[$BASH_SOURCE:$FUNCNAME:$LINENO]"
function sample_trainingset ()
{
	local i=$1
	mkdircond ${sequencesamplesets}/${i}
	local _images=( $(delEl "${i}" images[@]) )
	runcond "${scripts}/sample_trainingset.py ${sequencefeatures}/ ${sequencesegmentations}/ ${sequencebrainmasks}/ ${sequencesamplesets}/${i}/ ${featurecnf} ${samplesize} $(joinarr " " ${_images[@]})"
}
parallelize sample_trainingset ${threadcount} images[@]
log 2 "Done." "[$BASH_SOURCE:$FUNCNAME:$LINENO]"
