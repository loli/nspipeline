#!/bin/bash

#####
# Removes intensity in-homogenities in the images.
#####

## Changelog
# 2010-11-11 created

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
		
		cmd="cmtk mrbias --mask ${stdbrainmasks}/${i}.${imgfiletype} ${stdskullstripped}/${i}/${s}.${imgfiletype} ${stdbiasfieldcorrected}/${i}/${s}.${imgfiletype}" # note: already multitasking
		$cmd > /dev/null

	done
done
log 2 "Done." "[$BASH_SOURCE:$FUNCNAME:$LINENO]"
