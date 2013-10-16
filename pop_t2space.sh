#!/bin/bash

#####
# Registers all spectra to the T2 image (T1 would also be possible) and create
# transformed images as well as saving the elastix transformation files.
# Note that ADC are not registered to the T2 themselves, bur tranformed using the
# DW transformation matrix, as they share the same space.
#####

## Changelog
# 2010-10-16 ADC images are now not registered directly, but rather transformed with the DW transformation matrix
# 2010-10-15 created

# include shared information
source $(dirname $0)/include.sh

# main code
log 2 "Registering all sequence to T2" "[$BASH_SOURCE:$FUNCNAME:$LINENO]"
# prepare temporary directory
tmpdir=`mktemp -d`
for ((i = 0; i < ${#images[@]}; i++)); do
	mkdircond ${t2space}/${images[$i]}
	for s in "${sequences[@]}"; do
		# catch T2 and continue, since it is the fixed image and does not need registration
		if [ "${s}" == "t2_sag_tse" ]; then
			continue
		fi
		# catch ADC and continue, since these are transformed with the DW transformation matrices
		if [ "${s}" == "adc_tra" ]; then
			continue
		fi
		# continue if target file already exists
		if [ -f "${t2space}/${images[$i]}/${s}.${imgfiletype}" ]; then
			continue
		fi

		# perform rigid registration
		log 1 "Registering ${originals}/${images[$i]}/${s}.${imgfiletype} to ${originals}/${images[$i]}/t2_sag_tse.${imgfiletype} using tmp dir ${tmpdir}"
		cmd="elastix -f ${originals}/${images[$i]}/t2_sag_tse.${imgfiletype} -m ${originals}/${images[$i]}/${s}.${imgfiletype} -out ${tmpdir} -p ${configs}/elastix_t2space_rigid_cfg.txt"
		$cmd > /dev/null
		# copy resulting files
		cmd="cp ${tmpdir}/result.0.nii.gz ${t2space}/${images[$i]}/${s}.${imgfiletype}"
		$cmd
		cmd="cp ${tmpdir}/TransformParameters.0.txt ${t2space}/${images[$i]}/${s}.txt"
		$cmd
		# clean up
		emptydircond ${tmpdir}
	done
done
# remove temporary directory
rmdircond ${tmpdir}
log 2 "Done." "[$BASH_SOURCE:$FUNCNAME:$LINENO]"


log 2 "Transforming ADC images" "[$BASH_SOURCE:$FUNCNAME:$LINENO]"
# prepare temporary directory
tmpdir=`mktemp -d`
for ((i = 0; i < ${#images[@]}; i++)); do
	mkdircond ${t2space}/${images[$i]}
	log 1 "Transforming ADC image ${originals}/${images[$i]}/adc_tra.${imgfiletype} with ${t2space}/${images[$i]}/dw_tra_b1000_dmean.txt transformation matrix using tmp dir ${tmpdir}"
	cmd="transformix -in ${originals}/${images[$i]}/adc_tra.${imgfiletype} -out ${tmpdir} -tp ${t2space}/${images[$i]}/dw_tra_b1000_dmean.txt"
	$cmd > /dev/null
	# copy resulting file
	cmd="cp ${tmpdir}/result.nii.gz ${t2space}/${images[$i]}/adc_tra.${imgfiletype}"
	$cmd
	cmd="cp ${t2space}/${images[$i]}/dw_tra_b1000_dmean.txt ${t2space}/${images[$i]}/adc_tra.txt"
	$cmd
	# clean up
	emptydircond ${tmpdir}
done
# remove temporary directory
rmdircond ${tmpdir}
log 2 "Done." "[$BASH_SOURCE:$FUNCNAME:$LINENO]"


log 2 "Linking all T2 sequences for easier access" "[$BASH_SOURCE:$FUNCNAME:$LINENO]"
for ((i = 0; i < ${#images[@]}; i++)); do
	mkdircond ${t2space}/${images[$i]}
	# link T2 sequences
	cwd=`pwd`
	lncond ${cwd}/${originals}/${images[$i]}/t2_sag_tse.${imgfiletype} ${t2space}/${images[$i]}/${s}.${imgfiletype}
done
log 2 "Done." "[$BASH_SOURCE:$FUNCNAME:$LINENO]"
