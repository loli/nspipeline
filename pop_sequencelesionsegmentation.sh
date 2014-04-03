#!/bin/bash

#####
# Creates a preliminary segmentation of the brain lesion in sequence space.
# ! Remember to run pop_sequencesegmentations.sh before this script.
#####

## Changelog
# 2013-03-25 Updated to new, variable version.
# 2013-11-25 Updated to use new script to distinguish between sequence space and std space features
# 2013-11-05 adapted to new brain mask location
# 2013-10-29 created

# include shared information
source $(dirname $0)/include.sh

# main code
log 2 "Extracting the features" "[$BASH_SOURCE:$FUNCNAME:$LINENO]"
function extract_features ()
{
	i=$1
	mkdircond ${sequencelesionsegmentation}/${i}
	runcond "${scripts}/extract_features_sequencespace.py ${sequenceintensitrangestandardization}/${i}/ ${sequencebrainmasks}/${i}.${imgfiletype} ${sequencelesionsegmentation}/${i}/"
}
parallelize extract_features ${threadcount} images[@]

log 2 "Drawing a training set for each leave-one-out case using stratified random sampling" "[$BASH_SOURCE:$FUNCNAME:$LINENO]"
function sample_trainingset ()
{
	i=$1
	runcond "${scripts}/sample_trainingset.py ${sequencelesionsegmentation}/ ${sequencesegmentations} ${sequencebrainmasks}/{}.${imgfiletype} ${i}"
}
parallelize sample_trainingset ${threadcount} images[@]

log 2 "Training random decision forests" "[$BASH_SOURCE:$FUNCNAME:$LINENO]"
for i in "${images[@]}"; do
	runcond "${scripts}/train_rdf.py ${sequencelesionsegmentation}/${i}/trainingset.features.npy ${sequencelesionsegmentation}/${i}/forest.pkl"
done

log 2 "Applying random decision forests to segment lesion" "[$BASH_SOURCE:$FUNCNAME:$LINENO]"
for i in "${images[@]}"; do
	runcond "${scripts}/apply_rdf.py ${sequencelesionsegmentation}/${i}/forest.pkl ${sequencelesionsegmentation}/${i}/ ${sequencebrainmasks}/${i}.nii.gz ${sequencelesionsegmentation}/${i}/segmentation.nii.gz"
done

log 2 "Compute overall evaluation" "[$BASH_SOURCE:$FUNCNAME:$LINENO]"
runcond "${scripts}/evaluate_segmentations.py ${sequencelesionsegmentation}/{}/segmentation.${imgfiletype} ${sequencesegmentations}/{}.${imgfiletype} ${sequencebrainmasks}/{}.${imgfiletype} $(joinarr " " ${images[@]})"

log 2 "Done." "[$BASH_SOURCE:$FUNCNAME:$LINENO]"


