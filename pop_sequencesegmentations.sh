#!/bin/bash

#####
# Tranform all segmentation binary images to the base sequence space.
#####

## Changelog
# 2014-03-25 Adapted to work with arbitrary base sequence, treating flair_tra special.
# 2013-11-06 added an additional step, correcting precision errors in the image header
# 2013-11-05 optimized
# 2013-10-21 created

# include shared information
source $(dirname $0)/include.sh

# constants
basesequence="flair_tra" # the base-sequence the images have been registered to to

# functions
###
# Binary resampling of a mask
###
function bresample ()
{
	srcfile=$1
	trgfile=$2
	vs=$3
	
	# warn and skip if source file not present
	if [ ! -f "${srcfile}" ]; then
		log 3 "Original round truth for case not found under ${srcfile}. Skipping." "[$BASH_SOURCE:$FUNCNAME:$LINENO]"
		return
	fi

	# process if target file not yet existing
	if [ ! -f "${trgfile}" ]; then
		log 1 "Resampling to ${trgfile} with ${vs}" "[$BASH_SOURCE:$FUNCNAME:$LINENO]"
		runcond "medpy_resample.py ${srcfile} ${trgfile} ${vs} -o1"
	fi
}

# main code
if [ ${basesequence} == "flair_tra" ]; then
	log 2 "Adapting all expert segmentation to (possibly resampled) flair_tra space" "[$BASH_SOURCE:$FUNCNAME:$LINENO]"
	# check on first flair case, whether a resampling on the flair images has been conducted
	ovs=( $(voxelspacing "${originals}/${images[0]}/flair_tra.${imgfiletype}") )
	nvs=( $(voxelspacing "${sequencespace}/${images[0]}/flair_tra.${imgfiletype}") )
	equal=true
	for i in "${!ovs[@]}"; do
		if [ ! "${ovs[$i]}" == "${nvs[$i]}" ]; then
			equal=false
			break
		fi
	done
	
	# if equal, simply link masks, if not, resample masks
	if $equal; then
		log 2 "Detected flair_tra sequence to not have been resampled. Performing linking." "[$BASH_SOURCE:$FUNCNAME:$LINENO]"
		cwd=$(pwd)
		for i in "${images[@]}"; do
			lncond "${cwd}/${segmentations}/${i}.${imgfiletype}" "${sequencesegmentations}/${i}.${imgfiletype}"
		done
	else
		log 2 "Detected flair_tra sequence to have been resampled. Performing binary resampling." "[$BASH_SOURCE:$FUNCNAME:$LINENO]"
		for i in "${images[@]}"; do
			bresample "${segmentations}/${i}.${imgfiletype}" "${sequencesegmentations}/${i}.${imgfiletype}" $(joinarr "," ${nvs[@]})
		done
	fi

else
	# transfom using the flair transformation matrix
	log 2 "Tranforming all expert segmentation to ${basesequence} space" "[$BASH_SOURCE:$FUNCNAME:$LINENO]"

	tmpdir=`mktemp -d`
	for i in "${images[@]}"; do

		# continue if target file already exists
		if [ -f "${sequencesegmentations}/${i}.${imgfiletype}" ]; then
			continue
		fi

		# edit transformation file (strange, array using syntax, since otherwise quotes '' are passed to sed)
		command=(sed -e 's/(FinalBSplineInterpolationOrder 3)/(FinalBSplineInterpolationOrder 0)/g' -e 's/(ResultImagePixelType \"float\")/(ResultImagePixelType \"char\")/g' "${sequencespace}/${i}/flair_tra.txt")
		#echo "Command: \"${command[*]}\""
		"${command[@]}" > "${tmpdir}/tf.txt"

		# run transformation
		runcond "transformix -out ${tmpdir} -tp ${tmpdir}/tf.txt -in ${segmentations}/${i}.${imgfiletype}" /dev/null

		# copy transformed binary segmentation file
		runcond "mv ${tmpdir}/result.${imgfiletype} ${sequencesegmentations}/${i}.${imgfiletype}"

		# adapt header, as elastix seems to use another precision, which might lead to error later
		runcond "${scripts}/pass_header.py ${sequencesegmentations}/${i}.${imgfiletype} ${sequencespace}/${i}/${basesequence}.${imgfiletype}"

		emptydircond ${tmpdir}
	done
	rmdircond ${tmpdir}
fi

log 2 "Done." "[$BASH_SOURCE:$FUNCNAME:$LINENO]"
