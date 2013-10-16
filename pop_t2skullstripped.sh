#!/bin/bash

#####
# Creates a brain mask using the T2 (alternatively T1) image and extracts the
# skull from all sequences volumes.
#####

## Changelog
# 2010-10-16 created

# include shared information
source $(dirname $0)/include.sh

# main code
log 2 "Computing brain mask on T2" "[$BASH_SOURCE:$FUNCNAME:$LINENO]"
tmpdir=`mktemp -d`
for ((i = 0; i < ${#images[@]}; i++)); do
	mkdircond ${t2skullstripped}/${images[$i]}

	# continue if target file already exists
	if [ -f "${t2skullstripped}/${images[$i]}/t2_sag_tse.${imgfiletype}" ]; then
		continue
	fi

	cmd="fsl5.0-bet ${t2space}/${images[$i]}/t2_sag_tse.${imgfiletype} ${t2skullstripped}/${images[$i]}/t2_sag_tse.${imgfiletype} -m -R"
	$cmd > /dev/null

	emptydircond ${tmpdir}
done
rmdircond ${tmpdir}
log 2 "Done." "[$BASH_SOURCE:$FUNCNAME:$LINENO]"

log 2 "Applying brainmask to other spectra" "[$BASH_SOURCE:$FUNCNAME:$LINENO]"
for ((i = 0; i < ${#images[@]}; i++)); do
	mkdircond ${t2skullstripped}/${images[$i]}
	for s in "${sequences[@]}"; do
		# catch T2 since it has been already processed
		if [ "${s}" == "t2_sag_tse" ]; then
			continue
		fi

		# continue if target file already exists
		if [ -f "${t2skullstripped}/${images[$i]}/${s}.${imgfiletype}" ]; then
			continue
		fi

		cmd="${scripts}/apply_binary_mask.py ${t2space}/${images[$i]}/${s}.${imgfiletype} ${t2skullstripped}/${images[$i]}/t2_sag_tse_mask.${imgfiletype} ${t2skullstripped}/${images[$i]}/${s}.${imgfiletype}"
		$cmd > /dev/null
	done
done
log 2 "Done." "[$BASH_SOURCE:$FUNCNAME:$LINENO]"

