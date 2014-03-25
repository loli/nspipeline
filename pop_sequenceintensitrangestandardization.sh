#!/bin/bash

#####
# Standarizes the intensity profiles of all images belonging to the same MRI sequence.
#####

## Changelog
# 2013-03-25 Updated to new structure.
# 2013-11-14 changed script to allow for intensity correction of an image, even if the model already exists
# 2013-11-05 adapted to new brain mask location
# 2013-10-22 created

# include shared information
source $(dirname $0)/include.sh

# main code
log 2 "Learning and adapting the intensity profiles" "[$BASH_SOURCE:$FUNCNAME:$LINENO]"
tmpdir=`mktemp -d`
for s in "${sequences[@]}"; do
	log 2 "Processing MRI sequence ${s}" "[$BASH_SOURCE:$FUNCNAME:$LINENO]"

	# if target model already exists, skip model creation for the whole sequence and remark upon it
	if [ -f "${sequenceintensitrangestandardization}/intensity_model_${s}.pkl" ]; then
		log 3 "The intensity model for the MRI sequence ${s} already exists. Skipping the model creation for the whole sequence." "[$BASH_SOURCE:$FUNCNAME:$LINENO]"
	else
		# collect all the images for training
		images_string=""
		masks_string=""
		for i in "${images[@]}"; do
			# if target file already exists, skip model creation for the whole sequence and remark upon it
			if [ -f "${sequenceintensitrangestandardization}/${i}/${s}.${imgfiletype}" ]; then
				log 3 "One of the target files for the MRI sequence ${s} already exists. Skipping the model creation and image transformation for the whole sequence." "[$BASH_SOURCE:$FUNCNAME:$LINENO]"
				continue 2
			fi
			# add image to list of images to use for training (always use all images)
			images_string="${images_string} ${sequencebiasfieldcorrected}/${i}/${s}.${imgfiletype}"
			masks_string="${masks_string} ${sequencebrainmasks}/${i}.${imgfiletype}"
		done

		# train the model without transforming the images
		runcond "medpy_intensity_range_standardization.py --masks ${masks_string} --save-model ${sequenceintensitrangestandardization}/intensity_model_${s}.pkl ${images_string}"
	fi

	# transform and post-process the images, them move them to their target location if not already existant
	for i in "${images[@]}"; do
		mkdircond ${sequenceintensitrangestandardization}/${i}
		if [ ! -f "${sequenceintensitrangestandardization}/${i}/${s}.${imgfiletype}" ]; then
			runcond "medpy_intensity_range_standardization.py --load-model ${sequenceintensitrangestandardization}/intensity_model_${s}.pkl --masks ${sequencebrainmasks}/${i}.${imgfiletype} --save-images ${tmpdir} ${sequencebiasfieldcorrected}/${i}/${s}.${imgfiletype}"
			runcond "${scripts}/condenseoutliers.py ${tmpdir}/${s}.${imgfiletype} ${sequenceintensitrangestandardization}/${i}/${s}.${imgfiletype}"
		fi
	done

	emptydircond ${tmpdir}
done
rmdircond ${tmpdir}
log 2 "Done." "[$BASH_SOURCE:$FUNCNAME:$LINENO]"


