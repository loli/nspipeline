#!/bin/bash

#####
# Link images from the image database in a consitent manner to 00originals.
# Selects all ischemic only lesion cases that contain the required MRI sequences.
#####

## Changelog
# 2013-11-13 changed to actually copy even existing files and to correct the qform and sform codes
# 2013-10-15 changed the ADC creation script and added a conversion of non-float to float images
# 2013-10-02 created

# include shared information
source $(dirname $0)/include.sh

# Image collection HEOPKS details
c01dir="/imagedata/HEOPKS/data/"
c01indicessrc=("03" "05" "07" "09" "11" "12" "13" "15" "18")
c01indicestrg=("01" "02" "03" "04" "05" "06" "07" "08" "09")

# Image collection JGABLENTZ details
c02dir="/imagedata/JGABLENTZ/data/"
c02indicessrc=("11" "13" "14" "17" "19" "20" "29" "30" "31" "34" "47" "55" "57")
c02indicestrg=("10" "11" "12" "13" "14" "15" "16" "17" "18" "19" "20" "21" "22")

# main code
log 2 "Copying / converting images from collection ${c01dir} and correcting metadata" "[$BASH_SOURCE:$FUNCNAME:$LINENO]"
for ((i = 0; i < ${#c01indicessrc[@]}; i++)); do
	mkdircond ${originals}/${c01indicestrg[$i]}
	for s in "${sequences[@]}"; do
		# continue if target file already exists
		if [ -f "${originals}/${c01indicestrg[$i]}/${s}.${imgfiletype}" ]; then
			continue
		fi

		# catch ADC since it has to be created instead of linked when it does not exist yet
		if [ "${s}" == "adc_tra" ]; then
			if [ ! -f ${c01dir}/${c01indicessrc[$i]}/${s}.${imgfiletype} ]; then
				cmd="medpy_apparent_diffusion_coefficient.py ${c01dir}/${c01indicessrc[$i]}/dw_tra_b0_dmean.${imgfiletype} ${c01dir}/${c01indicessrc[$i]}/dw_tra_b1000_dmean.${imgfiletype} 1000 ${originals}/${c01indicestrg[$i]}/${s}.${imgfiletype} -f"
				$cmd
				continue
			fi
		fi
		# copy files otherwise
		cmd="cp ${c01dir}/${c01indicessrc[$i]}/${s}.${imgfiletype} ${originals}/${c01indicestrg[$i]}/${s}.${imgfiletype}"
		$cmd
		# correct nifit orientation metadata in-place
		cmd="${scripts}/niftimodifymetadata.py ${originals}/${c01indicestrg[$i]}/${s}.${imgfiletype} qf=aff sf=aff qfc=1 sfc=1"
		$cmd
	done
done
log 2 "Done." "[$BASH_SOURCE:$FUNCNAME:$LINENO]"

log 2 "Copying / converting images from collection ${c02dir} and correcting metadata" "[$BASH_SOURCE:$FUNCNAME:$LINENO]"
for ((i = 0; i < ${#c02indicessrc[@]}; i++)); do
	mkdircond ${originals}/${c02indicestrg[$i]}
	for s in "${sequences[@]}"; do
		# continue if target file already exists
		if [ -f "${originals}/${c02indicestrg[$i]}/${s}.${imgfiletype}" ]; then
			continue
		fi

		# catch ADC since it has to be created instead of linked when it does not exist yet
		if [ "${s}" == "adc_tra" ]; then
			if [ ! -f ${c02dir}/${c02indicessrc[$i]}/${s}.${imgfiletype} ]; then
				cmd="medpy_apparent_diffusion_coefficient.py ${c02dir}/${c02indicessrc[$i]}/dw_tra_b0_dmean.${imgfiletype} ${c02dir}/${c02indicessrc[$i]}/dw_tra_b1000_dmean.${imgfiletype} 1000 ${originals}/${c02indicestrg[$i]}/${s}.${imgfiletype} -f"
				$cmd
				continue
			fi
		fi
		# convert datatype to float64 otherwise
		cmd="${scripts}/tofloat64.py ${c02dir}/${c02indicessrc[$i]}/${s}.${imgfiletype} ${originals}/${c02indicestrg[$i]}/${s}.${imgfiletype}"
		$cmd
		# correct nifit orientation metadata in-place
		cmd="${scripts}/niftimodifymetadata.py ${originals}/${c02indicestrg[$i]}/${s}.${imgfiletype} qf=aff sf=aff qfc=1 sfc=1"
		$cmd
	done
done
log 2 "Done." "[$BASH_SOURCE:$FUNCNAME:$LINENO]"
