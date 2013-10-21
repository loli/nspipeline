#!/bin/bash

#####
# Tranform all segmentation binary images to T2 space.
#####

## Changelog
# 2010-10-21 created

# include shared information
source $(dirname $0)/include.sh

# main code
log 2 "Tranforming all expert segmentation to T2 space" "[$BASH_SOURCE:$FUNCNAME:$LINENO]"
tmpdir=`mktemp -d`
for ((i = 0; i < ${#images[@]}; i++)); do
	
	# continue if target file already exists
	if [ -f "${t2segmentations}/${images[$i]}.${imgfiletype}" ]; then
		continue
	fi

	# edit transformation file (strange, array using syntax, since otherwise quotes '' are passed to sed)
	command=(sed -e 's/(FinalBSplineInterpolationOrder 3)/(FinalBSplineInterpolationOrder 0)/g' -e 's/(ResultImagePixelType \"float\")/(ResultImagePixelType \"char\")/g' "${t2space}/${images[$i]}/flair_tra.txt")
	#echo "Command: \"${command[*]}\""
	"${command[@]}" > "${tmpdir}/tf.txt"

	# run transformation
	cmd="transformix -out ${tmpdir} -tp ${tmpdir}/tf.txt -in ${segmentations}/${images[$i]}.${imgfiletype}"
	$cmd > /dev/null

	# copy transformed binary segmentation file
	cmd="mv ${tmpdir}/result.${imgfiletype} ${t2segmentations}/${images[$i]}.${imgfiletype}"
	$cmd

	emptydircond ${tmpdir}
done
rmdircond ${tmpdir}
log 2 "Done." "[$BASH_SOURCE:$FUNCNAME:$LINENO]"
