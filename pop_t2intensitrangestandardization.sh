#!/bin/bash

#####
# Standarizes the intensity profiles of all images belonging to the same MRI sequence.
#####

## Changelog
# 2010-11-05 adapted to new brain mask location
# 2010-10-22 created

# include shared information
source $(dirname $0)/include.sh

# main code
log 2 "Learning and adapting the intensity profiles" "[$BASH_SOURCE:$FUNCNAME:$LINENO]"
tmpdir=`mktemp -d`
for s in "${sequences[@]}"; do
	log 2 "Processing MRI sequence ${s}" "[$BASH_SOURCE:$FUNCNAME:$LINENO]"

	# if target model already exists, skip model creation for the whole sequence and remark upon it
	if [ -f "${t2intensitrangestandardization}/intensity_model_${s}.pkl" ]; then
		log 3 "The intensity model for the MIR sequence ${s} already exists. Skipping the model creation and image transformation for the whole sequence." "[$BASH_SOURCE:$FUNCNAME:$LINENO]"
		continue
	fi

	# collect all the images for training
	images_string=""
	masks_string=""
	for i in "${images[@]}"; do
		# if target file already exists, skip model creation for the whole sequence and remark upon it
		if [ -f "${t2intensitrangestandardization}/${i}/${s}.${imgfiletype}" ]; then
			log 3 "One of the target files for the MIR sequence ${s} already exists. Skipping the model creation and image transformation for the whole sequence." "[$BASH_SOURCE:$FUNCNAME:$LINENO]"
			continue 2
		fi
		# add image to list of images to use for training (always use all images)
		images_string="${images_string} ${t2biasfieldcorrected}/${i}/${s}.${imgfiletype}"
		masks_string="${masks_string} ${t2brainmasks}/${i}.${imgfiletype}"
	done

	# train the model without transforming the images
	cmd="medpy_intensity_range_standardization.py --masks ${masks_string} --save-model ${t2intensitrangestandardization}/intensity_model_${s}.pkl ${images_string}"
	$cmd

	# transform and post-process the images, them move them to their target location
	for i in "${images[@]}"; do
		mkdircond ${t2intensitrangestandardization}/${i}
		cmd="medpy_intensity_range_standardization.py --load-model ${t2intensitrangestandardization}/intensity_model_${s}.pkl --masks ${t2brainmasks}/${i}.${imgfiletype} --save-images ${tmpdir} ${t2biasfieldcorrected}/${i}/${s}.${imgfiletype} -f"
		$cmd
		cmd="${scripts}/condenseoutliers.py ${tmpdir}/${s}.${imgfiletype} ${t2intensitrangestandardization}/${i}/${s}.${imgfiletype}"
		$cmd
	done

	emptydircond ${tmpdir}
done
rmdircond ${tmpdir}
log 2 "Done." "[$BASH_SOURCE:$FUNCNAME:$LINENO]"


