#!/bin/bash

#####
# Removes intensity in-homogenities in the images.
#####

## Changelog
# 2010-11-04 imporved code
# 2010-10-17 created

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
		
		cmd="cmtk mrbias --mask ${t2brainmasks}/${i}.${imgfiletype} ${t2skullstripped}/${i}/${s}.${imgfiletype} ${t2biasfieldcorrected}/${i}/${s}.${imgfiletype}" # note: already multitasking
		$cmd > /dev/null

	done
done
log 2 "Done." "[$BASH_SOURCE:$FUNCNAME:$LINENO]"
