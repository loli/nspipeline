#!/bin/bash

#####
# Removes intensity in-homogenities in the images.
#####

## Changelog
# 2013-11-14 added a step to correct the nifti metadata
# 2013-11-04 imporved code
# 2013-10-17 created

# include shared information
source $(dirname $0)/include.sh

# main code
log 2 "Correcting the bias fields" "[$BASH_SOURCE:$FUNCNAME:$LINENO]"
for i in "${images[@]}"; do
	mkdircond ${t2biasfieldcorrected}/${i}
	for s in "${sequences[@]}"; do

		# continue if target file already exists
		if [ -f "${t2biasfieldcorrected}/${i}/${s}.${imgfiletype}" ]; then
			continue
		fi
		
		# esitmate and correct bias field
		cmd="cmtk mrbias --mask ${t2brainmasks}/${i}.${imgfiletype} ${t2skullstripped}/${i}/${s}.${imgfiletype} ${t2biasfieldcorrected}/${i}/${s}.${imgfiletype}" # note: already multitasking
		$cmd > /dev/null

		# correct nifit orientation metadata in-place
		cmd="${scripts}/niftimodifymetadata.py ${t2biasfieldcorrected}/${i}/${s}.${imgfiletype} qf=aff sf=aff qfc=1 sfc=1"
		$cmd
	done
done
log 2 "Done." "[$BASH_SOURCE:$FUNCNAME:$LINENO]"
