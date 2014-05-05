#!/bin/bash

#####
# Uses the floating point brain mask shipped with the std brain to extract the brain from all image in std space.
#####

## Changelog
# 2014-04-04 adapted to new style
# 2013-11-14 added a step to correct the brain masks metadata
# 2013-11-11 created

# include shared information
source $(dirname $0)/include.sh

# constants
basesequence="flair_tra" # the base-sequence to use as reference

# main code
tmpdir=`mktemp -d`

log 2 "Reslicing brain mask" "[$BASH_SOURCE:$FUNCNAME:$LINENO]"
runcond "medpy_resample.py /home/maier/Applications/spm8/apriori/brainmask.nii ${tmpdir}/brainmask.${imgfiletype} 1,1,1"

log 2 "Aligning brain mask and threshold" "[$BASH_SOURCE:$FUNCNAME:$LINENO]"
function align_brainmask ()
{
	# grab parameters
	i=$1
	# created required directories
	mkdircond ${stdskullstripped}/${i}
	# continue if target file already exists
	if [ -f "${stdbrainmasks}/${i}.${imgfiletype}" ]; then
		return
	fi
	# align brain mask
	runcond "${scripts}/align.py ${tmpdir}/brainmask.${imgfiletype} ${stdspace}/${i}/${basesequence}.${imgfiletype} ${tmpdir}/${i}_maskf.${imgfiletype}"
	# threshold brainmask
	runcond "${scripts}/threshold.py ${tmpdir}/${i}_maskf.${imgfiletype} 0.8 ${stdbrainmasks}/${i}.${imgfiletype}"
	# correct nifit orientation metadata in-place
	runcond "${scripts}/niftimodifymetadata.py ${stdbrainmasks}/${i}.${imgfiletype} sf=qf qfc=2 sfc=2"
}
parallelize align_brainmask ${threadcount} images[@]
emptydircond ${tmpdir}
rmdircond ${tmpdir}

log 2 "Applying brainmask to spectra" "[$BASH_SOURCE:$FUNCNAME:$LINENO]"
function apply_brainmask ()
{
	# grab parameters
	i=$1
	# for each spectrum
	for s in "${sequences[@]}"; do
		# continue if target file already exists
		if [ -f "${stdskullstripped}/${i}/${s}.${imgfiletype}" ]; then
			continue
		fi
		runcond "${scripts}/apply_binary_mask.py ${stdspace}/${i}/${s}.${imgfiletype} ${stdbrainmasks}/${i}.${imgfiletype} ${stdskullstripped}/${i}/${s}.${imgfiletype}"
	done
}
parallelize apply_brainmask ${threadcount} images[@]

log 2 "Done." "[$BASH_SOURCE:$FUNCNAME:$LINENO]"

