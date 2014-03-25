#!/bin/bash

#####
# Creates a preliminary segmentation of the brain lesion in T2 space.
# ! Remember to run pop_t2segmentations.sh before this script.
#####

## Changelog
# 2013-11-25 Updated to use new script to distinguish between t2 space and std spcae features
# 2013-11-05 adapted to new brain mask location
# 2013-10-29 created

# include shared information
source $(dirname $0)/include.sh

# main code
log 2 "Extracting the features" "[$BASH_SOURCE:$FUNCNAME:$LINENO]"
function extract_features ()
{
	# grab parameters
	i=$1
	# run code
	mkdircond ${t2lesionsegmentation}/${i}
	cmd="${scripts}/extract_features_stdspace.py ${t2intensitrangestandardization}/${i}/ ${t2brainmasks}/${i}.${imgfiletype} ${t2lesionsegmentation}/${i}/"
	$cmd
}
parallelize extract_features ${threadcount} images[@]

log 2 "Drawing a training set for each leave-one-out case using stratified random sampling" "[$BASH_SOURCE:$FUNCNAME:$LINENO]"
function sample_trainingset ()
{
	# grab parameters
	i=$1
	# run code
	cmd="${scripts}/sample_trainingset.py ${t2lesionsegmentation}/ ${t2segmentations} ${t2brainmasks}/{}.${imgfiletype} ${i}"
	$cmd
}
parallelize sample_trainingset ${threadcount} images[@]

log 2 "Training random decision forests" "[$BASH_SOURCE:$FUNCNAME:$LINENO]"
for i in "${images[@]}"; do
	cmd="${scripts}/train_rdf.py ${t2lesionsegmentation}/${i}/trainingset.features.npy ${t2lesionsegmentation}/${i}/forest.pkl"
	$cmd
done

log 2 "Applying random decision forests to segment lesion" "[$BASH_SOURCE:$FUNCNAME:$LINENO]"
for i in "${images[@]}"; do
	cmd="${scripts}/apply_rdf.py ${t2lesionsegmentation}/${i}/forest.pkl ${t2lesionsegmentation}/${i}/ ${t2brainmasks}/${i}.nii.gz ${t2lesionsegmentation}/${i}/segmentation.nii.gz"
	$cmd
done

log 2 "Compute overall evaluation" "[$BASH_SOURCE:$FUNCNAME:$LINENO]"
cmd="${scripts}/evaluate_segmentations.py ${t2lesionsegmentation}/{}/segmentation.${imgfiletype} ${t2segmentations}/{}.${imgfiletype} ${t2brainmasks}/{}.${imgfiletype} ${images[@]}"
$cmd

log 2 "Done." "[$BASH_SOURCE:$FUNCNAME:$LINENO]"


