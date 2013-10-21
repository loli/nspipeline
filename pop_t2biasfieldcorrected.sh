#!/bin/bash

#####
# Removes intensity in-homogenities in the images.
#####

## Changelog
# 2010-10-17 created

# include shared information
source $(dirname $0)/include.sh

# main code
log 2 "Correcting the bias fields" "[$BASH_SOURCE:$FUNCNAME:$LINENO]"
for ((i = 0; i < ${#images[@]}; i++)); do
	mkdircond ${t2biasfieldcorrected}/${images[$i]}
	for s in "${sequences[@]}"; do

		# continue if target file already exists
		if [ -f "${t2biasfieldcorrected}/${images[$i]}/${s}.${imgfiletype}" ]; then
			continue
		fi
		
		cmd="cmtk mrbias --mask ${t2skullstripped}/${images[$i]}/t2_sag_tse_mask.${imgfiletype} ${t2skullstripped}/${images[$i]}/${s}.${imgfiletype} ${t2biasfieldcorrected}/${images[$i]}/${s}.${imgfiletype}"
		$cmd > /dev/null

	done
done
log 2 "Done." "[$BASH_SOURCE:$FUNCNAME:$LINENO]"
