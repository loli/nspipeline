#!/bin/bash

#####
# Creates a brain mask using the base sequence image and extracts the
# skull from all sequences volumes.
#####

## Changelog
# 2014-08-12 Adapted to work with different skull-stripping base sequences for different target sequences
# 2013-03-25 Adapted to take any sequence as base sequence.
# 2013-11-04 Improved the mechanism and seperated the brain mask location from the skull-stripped images.
# 2013-10-16 created

# include shared information
source $(dirname $0)/include.sh

# functions
###
# Compute a brain mask using the base sequence
###
function compute_brainmask ()
{
	# grab parameters
	i=$1

	# created required directories
	mkdircond ${sequenceskullstripped}/${basesequence}/${i}
	# continue if target file already exists
	if [ -f "${sequencebrainmasks}/${basesequence}/${i}.${imgfiletype}" ]; then
		return
	fi
	# compute brain mask
	log 1 "Computing brain mask for ${sequencespace}/${i}/${basesequence}.${imgfiletype}" "[$BASH_SOURCE:$FUNCNAME:$LINENO]"
	runcond "fsl5.0-bet ${sequencespace}/${i}/${basesequence}.${imgfiletype} ${sequenceskullstripped}/${basesequence}/${i}/${basesequence}.${imgfiletype} -m -R" /dev/null
	runcond "mv ${sequenceskullstripped}/${basesequence}/${i}/${basesequence}_mask.${imgfiletype} ${sequencebrainmasks}/${basesequence}/${i}.${imgfiletype}"
}

# main code
for scid in "${!sc_train_brainmasks[@]}"; do
    basesequence=${sc_train_brainmasks[$scid]}
    images=( ${sc_train_images[$scid]} )
    sequences=( ${sc_sequences[$scid]} )

    mkdircond ${sequenceskullstripped}/${basesequence}
    mkdircond ${sequencebrainmasks}/${basesequence}
    
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
		    trgfile="${sequenceskullstripped}/${basesequence}/${i}/${s}.${imgfiletype}"

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

		    runcond "${scripts}/apply_binary_mask.py ${srcfile} ${sequencebrainmasks}/${basesequence}/${i}.${imgfiletype} ${trgfile}" /dev/null
	    done
    done
done
log 2 "Done." "[$BASH_SOURCE:$FUNCNAME:$LINENO]"




