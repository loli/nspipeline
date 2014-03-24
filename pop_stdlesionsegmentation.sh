#!/bin/bash

#####
# Creates the final segmentation of the brain lesions in std space.
# ! Remember to run pop_stdsegmentations.sh before this script.
#####

## Changelog
# 2013-11-25 created

# include shared information
source $(dirname $0)/include.sh

# main code
log 2 "Extracting features" "[$BASH_SOURCE:$FUNCNAME:$LINENO]"
function extract_features ()
{
	# grab parameters
	i=$1
	# run code
	mkdircond ${stdlesionsegmentation}/${i}
	cmd="${scripts}/extract_features_stdspace.py ${stdintensitrangestandardization}/${i}/ ${stdbrainmasks}/${i}.${imgfiletype} ${stdlesionsegmentation}/${i}/"
	#$cmd
}
parallelize extract_features ${threadcount} images[@]

log 2 "Drawing a training set for each leave-one-out case using stratified random sampling" "[$BASH_SOURCE:$FUNCNAME:$LINENO]"
function sample_trainingset ()
{
	# grab parameters
	i=$1
	# run code
	cmd="${scripts}/sample_trainingset.py ${stdlesionsegmentation}/ ${stdsegmentations} ${stdbrainmasks}/{}.${imgfiletype} ${i}"
	$cmd
}
parallelize sample_trainingset ${threadcount} images[@]

log 2 "Training random decision forests" "[$BASH_SOURCE:$FUNCNAME:$LINENO]"
for i in "${images[@]}"; do
	cmd="${scripts}/train_rdf.py ${stdlesionsegmentation}/${i}/trainingset.features.npy ${stdlesionsegmentation}/${i}/forest.pkl"
	$cmd
done

log 2 "Applying random decision forests to segment lesion" "[$BASH_SOURCE:$FUNCNAME:$LINENO]"
for i in "${images[@]}"; do
	cmd="${scripts}/apply_rdf.py ${stdlesionsegmentation}/${i}/forest.pkl ${stdlesionsegmentation}/${i}/ ${stdbrainmasks}/${i}.nii.gz ${stdlesionsegmentation}/${i}/segmentation.${imgfiletype}"
	$cmd
done

log 2 "Compute overall evaluation" "[$BASH_SOURCE:$FUNCNAME:$LINENO]"
cmd="${scripts}/evaluate_segmentations.py ${stdlesionsegmentation}/{}/segmentation.${imgfiletype} ${stdsegmentations}/{}.${imgfiletype} ${stdbrainmasks}/{}.${imgfiletype} ${images[@]}"
$cmd

log 2 "Done." "[$BASH_SOURCE:$FUNCNAME:$LINENO]"


