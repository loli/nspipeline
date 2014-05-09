#!/bin/bash

#####
# Extracts a number of features as defined in a python-style config file.
#####

## Changelog
# 2013-05-08 created

# include shared information
source $(dirname $0)/include.sh

# main code
log 2 "Extracting the features" "[$BASH_SOURCE:$FUNCNAME:$LINENO]"
function extract_features ()
{
	i=$1
	mkdircond ${sequencefeatures}/${i}
	runcond "${scripts}/extract_features.py ${sequenceintensitrangestandardization}/${i}/ ${sequencebrainmasks}/${i}.${imgfiletype} ${sequencefeatures}/${i}/ ${featurecnf}"
}
parallelize extract_features ${threadcount} images[@]
log 2 "Done." "[$BASH_SOURCE:$FUNCNAME:$LINENO]"
