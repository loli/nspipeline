#!/bin/bash

#####
# Removes intensity in-homogenities in the images.
#####

## Changelog
# 2013-11-14 added a step to correct the nifti metadata
# 2013-11-11 created

# include shared information
source $(dirname $0)/include.sh

# main code
log 2 "Correcting the bias fields" "[$BASH_SOURCE:$FUNCNAME:$LINENO]"
for i in "${images[@]}"; do
	mkdircond ${stdbiasfieldcorrected}/${i}
	for s in "${sequences[@]}"; do

		echo ${stdbiasfieldcorrected}/${i}/${s}.${imgfiletype}
		# continue if target file already exists
		if [ -f "${stdbiasfieldcorrected}/${i}/${s}.${imgfiletype}" ]; then
			continue
		fi
		
		# esitmate and correct bias field
		cmd="cmtk mrbias --mask ${stdbrainmasks}/${i}.${imgfiletype} ${stdskullstripped}/${i}/${s}.${imgfiletype} ${stdbiasfieldcorrected}/${i}/${s}.${imgfiletype}" # note: already multitasking
		$cmd > /dev/null

		# correct nifit orientation metadata in-place
		cmd="${scripts}/niftimodifymetadata.py ${t2stdbiasfieldcorrected}/${i}/${s}.${imgfiletype} qf=aff sf=aff qfc=2 sfc=2"
		$cmd
	done
done
log 2 "Done." "[$BASH_SOURCE:$FUNCNAME:$LINENO]"
