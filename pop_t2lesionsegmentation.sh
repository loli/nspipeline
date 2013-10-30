#!/bin/bash

#####
# Creates a preliminary segmentation of the brain lesion in T2 space.
#####

## Changelog
# 2010-10-29 created

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
	cmd="${scripts}/extract_features.py ${t2intensitrangestandardization}/${i}/ ${t2skullstripped}/${i}/t2_sag_tse_mask.${imgfiletype} ${t2lesionsegmentation}/${i}/"
	#$cmd
}
parallelize extract_features ${threadcount} images[@]

log 2 "Drawing a training set for each leave-one-out case using stratified random sampling" "[$BASH_SOURCE:$FUNCNAME:$LINENO]"
function sample_trainingset ()
{
	# grab parameters
	i=$1
	# run code
	cmd="${scripts}/sample_trainingset.py ${t2lesionsegmentation}/ ${t2segmentations} ${t2skullstripped}/{}/t2_sag_tse_mask.${imgfiletype} ${i}"
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
	cmd="${scripts}/apply_rdf.py ${t2lesionsegmentation}/${i}/forest.pkl ${t2lesionsegmentation}/${i}/ ${t2skullstripped}/${i}/t2_sag_tse_mask.nii.gz ${t2lesionsegmentation}/${i}/segmentation.nii.gz"
	$cmd
done

log 2 "Compute overall evaluation" "[$BASH_SOURCE:$FUNCNAME:$LINENO]"
cmd="${scripts}/evaluate_segmentations.py ${t2lesionsegmentation}/{}/segmentation.${imgfiletype} ${t2segmentations}/{}.${imgfiletype} ${t2skullstripped}/{}/t2_sag_tse_mask.${imgfiletype} ${images[@]}"
$cmd

log 2 "Done." "[$BASH_SOURCE:$FUNCNAME:$LINENO]"


