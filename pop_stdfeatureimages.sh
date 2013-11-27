#!/bin/bash

#####
# Segments the matters from the T2 brian images and creates hemispheric difference version of different smoothing parameters of the images.
#####

## Changelog
# 2013-11-14 created

# include shared information
source $(dirname $0)/include.sh

# constants
active_sigmas=(0 1)
reference_sigmas=(0 1)

# main code
tmpdir=`mktemp -d`

log 2 "Segment brain tissues from T2 images" "[$BASH_SOURCE:$FUNCNAME:$LINENO]"
for i in "${images[@]}"; do
	mkdircond ${stdfeatureimages}/${i}
	# proceed only if not yet existant (assuming from white probability map to others)
	if [ ! -f "${stdfeatureimages}/${i}/tissue_probability_white.${imgfiletype}" ]; then
		# convert required images to .nii fromat for SPM to be able to read it
		cmd="medpy_convert.py ${stdintensitrangestandardization}/${i}/t2_sag_tse.${imgfiletype} ${tmpdir}/t2.nii"
		$cmd
		cmd="medpy_convert.py ${stdbrainmasks}/${i}.${imgfiletype} ${tmpdir}/mask.nii"
		$cmd
		# prepare matlab script
		cmd="${scripts}/make_spm_segment.py ${tmpdir}/t2.nii ${tmpdir}/mask.nii ${tmpdir}/segment.m"
		$cmd
		# run matlab script
		matlab -nodisplay -nosplash -nodesktop -r "addpath '${tmpdir}'; segment;" > ${tmpdir}/log
		# copy results to target location
		cmd="medpy_convert.py ${tmpdir}/c1* ${stdfeatureimages}/${i}/tissue_probability_white.${imgfiletype}"
		$cmd
		cmd="medpy_convert.py ${tmpdir}/c2* ${stdfeatureimages}/${i}/tissue_probability_gray.${imgfiletype}"
		$cmd
		cmd="medpy_convert.py ${tmpdir}/c3* ${stdfeatureimages}/${i}/tissue_probability_csf.${imgfiletype}"
		$cmd
	fi
	emptydircond ${tmpdir}
done
rmdircond ${tmpdir}


# !Not required, as extracted directly without intermediate image!
# for each spectrum
#for as in "${active_sigmas[@]}"; do
#	continue
#	for rs in "${reference_sigmas[@]}"; do
#		log 2 "Computing hemispheric difference maps for active and reference sigmas ${as} resp ${rs}" "[$BASH_SOURCE:$FUNCNAME:$LINENO]"
#		for s in "${sequences[@]}"; do
#			function compute_hd_map ()
#			{
#				# grab parameters
#				i=$1
#				# created required directories
#				mkdircond ${stdfeatureimages}/${i}
#				# continue if target file already exists
#				if [ -f "${stdfeatureimages}/${i}/${s}.as${as}_rs${rs}.${imgfiletype}" ]; then
#					return
#				fi
#				# extract
#				cmd="${scripts}/feature_hemispheric_difference.py ${stdintensitrangestandardization}/${i}/${s}.${imgfiletype} ${as} ${rs} 0 10 ${stdfeatureimages}/${i}/${s}.as${as}_rs${rs}.${imgfiletype}"
#				$cmd
#			}
#			parallelize compute_hd_map ${threadcount} images[@]
#		done
#	done
#done
log 2 "Done." "[$BASH_SOURCE:$FUNCNAME:$LINENO]"

