#!/bin/bash

#####
# Train the decision forest with a training sample set.
#####

## Changelog
# 2013-05-08 created

# include shared information
source $(dirname $0)/include.sh

# main code
log 2 "Training random decision forests" "[$BASH_SOURCE:$FUNCNAME:$LINENO]"
for i in "${images[@]}"; do
	runcond "scripts/train_rdf.py ${sequencesamplesets}/${i}/trainingset.features.npy ${sequenceforests}/${i}.pkl ${maxdepth}"
done
log 2 "Done." "[$BASH_SOURCE:$FUNCNAME:$LINENO]"
