#!/bin/bash

#####
# Uses the floating point brain mask shipped with the std brain to extract the brain from all image in std space.
#####

## Changelog
# 2013-11-14 added a step to correct the brain masks metadata
# 2013-11-11 created

# include shared information
source $(dirname $0)/include.sh

# main code
tmpdir=`mktemp -d`

log 2 "Reslicing brain mask" "[$BASH_SOURCE:$FUNCNAME:$LINENO]"
cmd="medpy_resample.py /home/maier/Applications/spm8/apriori/brainmask.nii ${tmpdir}/brainmask.${imgfiletype} 1,1,1"
$cmd

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
	cmd="${scripts}/align.py ${tmpdir}/brainmask.${imgfiletype} ${stdspace}/${i}/t2_sag_tse.${imgfiletype} ${tmpdir}/${i}_maskf.${imgfiletype}"
	$cmd
	# threshold brainmask
	cmd="${scripts}/threshold.py ${tmpdir}/${i}_maskf.${imgfiletype} 0.8 ${stdbrainmasks}/${i}.${imgfiletype}"
	$cmd
	# correct nifit orientation metadata in-place
	cmd="${scripts}/niftimodifymetadata.py ${stdbrainmasks}/${i}.${imgfiletype} sf=qf qfc=2 sfc=2"
	$cmd
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
		cmd="${scripts}/apply_binary_mask.py ${stdspace}/${i}/${s}.${imgfiletype} ${stdbrainmasks}/${i}.${imgfiletype} ${stdskullstripped}/${i}/${s}.${imgfiletype}"
		$cmd > /dev/null
	done
}
parallelize apply_brainmask ${threadcount} images[@]

log 2 "Done." "[$BASH_SOURCE:$FUNCNAME:$LINENO]"

