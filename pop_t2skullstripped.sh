#!/bin/bash

#####
# Creates a brain mask using the T2 (alternatively T1) image and extracts the
# skull from all sequences volumes.
#####

## Changelog
# 2013-11-04 Improved the mechanism and seperated the brain mask location from the skull-stripped images.
# 2013-10-16 created

# include shared information
source $(dirname $0)/include.sh

# main code
log 2 "Computing brain mask on T2" "[$BASH_SOURCE:$FUNCNAME:$LINENO]"
function compute_brainmask ()
{
	# grab parameters
	i=$1
	# created required directories
	mkdircond ${t2skullstripped}/${i}
	# continue if target file already exists
	if [ -f "${t2brainmasks}/${i}.${imgfiletype}" ]; then
		return
	fi
	# compute brain mask
	cmd="fsl5.0-bet ${t2space}/${i}/t2_sag_tse.${imgfiletype} ${t2skullstripped}/${i}/t2_sag_tse.${imgfiletype} -m -R"
	$cmd > /dev/null
	cmd="mv ${t2skullstripped}/${i}/t2_sag_tse_mask.${imgfiletype} ${t2brainmasks}/${i}.${imgfiletype}"
	$cmd
}
parallelize compute_brainmask ${threadcount} images[@]
log 2 "Done." "[$BASH_SOURCE:$FUNCNAME:$LINENO]"

log 2 "Applying brainmask to other spectra" "[$BASH_SOURCE:$FUNCNAME:$LINENO]"
for i in "${images[@]}"; do
	for s in "${sequences[@]}"; do
		# continue if target file already exists
		if [ -f "${t2skullstripped}/${i}/${s}.${imgfiletype}" ]; then
			continue
		fi

		cmd="${scripts}/apply_binary_mask.py ${t2space}/${i}/${s}.${imgfiletype} ${t2brainmasks}/${i}.${imgfiletype} ${t2skullstripped}/${i}/${s}.${imgfiletype}"
		$cmd > /dev/null
	done
done
log 2 "Done." "[$BASH_SOURCE:$FUNCNAME:$LINENO]"

