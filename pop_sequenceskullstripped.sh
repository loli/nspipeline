#!/bin/bash

#####
# Creates a brain mask using the base sequence image and extracts the
# skull from all sequences volumes.
#####

## Changelog
# 2013-03-25 Adapted to take any sequence as base sequence.
# 2013-11-04 Improved the mechanism and seperated the brain mask location from the skull-stripped images.
# 2013-10-16 created

# include shared information
source $(dirname $0)/include.sh

# constants
basesequence="flair_tra" # the base-sequence to use for the skull-stripping to

# functions
###
# Compute a brain mask using the base sequence
###
function compute_brainmask ()
{
	# grab parameters
	i=$1

	# created required directories
	mkdircond ${sequenceskullstripped}/${i}
	# continue if target file already exists
	if [ -f "${sequencebrainmasks}/${i}.${imgfiletype}" ]; then
		return
	fi
	# compute brain mask
	log 1 "Computing brain mask for ${sequencespace}/${i}/${basesequence}.${imgfiletype}" "[$BASH_SOURCE:$FUNCNAME:$LINENO]"
	runcond "fsl5.0-bet ${sequencespace}/${i}/${basesequence}.${imgfiletype} ${sequenceskullstripped}/${i}/${basesequence}.${imgfiletype} -m -R" /dev/null
	runcond "mv ${sequenceskullstripped}/${i}/${basesequence}_mask.${imgfiletype} ${sequencebrainmasks}/${i}.${imgfiletype}"
}

# main code
log 2 "Computing brain masks on base sequence ${basesequence}" "[$BASH_SOURCE:$FUNCNAME:$LINENO]"
parallelize compute_brainmask ${threadcount} images[@]

log 2 "Applying brainmask to remaining spectra" "[$BASH_SOURCE:$FUNCNAME:$LINENO]"
for i in "${images[@]}"; do
	for s in "${sequences[@]}"; do
		# skip if base sequence
		if [ "${s}" == "${basesequence}" ]; then
			continue
		fi

		srcfile="${sequencespace}/${i}/${s}.${imgfiletype}"
		trgfile="${sequenceskullstripped}/${i}/${s}.${imgfiletype}"

		# continue if target file already exists
		if [ -f "${trgfile}" ]; then
			log 1 "Target file ${trgfile} already exists. Skipping." "[$BASH_SOURCE:$FUNCNAME:$LINENO]"
			continue
		fi
		# continue and warn if source file doesn't exists
		if [ ! -f "${srcfile}" ]; then
			log 3 "Source file ${srcfile} does not exist. Skipping." "[$BASH_SOURCE:$FUNCNAME:$LINENO]"
			continue
		fi

		runcond "${scripts}/apply_binary_mask.py ${srcfile} ${sequencebrainmasks}/${i}.${imgfiletype} ${trgfile}" /dev/null
	done
done
log 2 "Done." "[$BASH_SOURCE:$FUNCNAME:$LINENO]"

