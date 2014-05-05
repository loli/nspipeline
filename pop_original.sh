#!/bin/bash

#####
# Link images from the image database in a consitent manner to 00originals.
# Links all images whose case ids are mentiones in "includes.sh".
# Flips every second case mid-saggital to have some right-sided lesions.
#####

## Changelog
# 2014-05-05 every second case now gets flipped
# 2014-03-24 changed to link sequence by availability (i.e. skip non-existing ones with only info message displayed)
# 2013-11-13 changed to actually copy even existing files and to correct the qform and sform codes
# 2013-10-15 changed the ADC creation script and added a conversion of non-float to float images
# 2013-10-02 created

# include shared information
source $(dirname $0)/include.sh

# Constants
sequencestolink=('flair_tra' 'dw_tra_b1000_dmean' 'adc_tra' 't1_tra_ffe' 't1_sag_tfe' 't2_sag_tse' 't2_tra_ffe' 't2_tra_tse') # where available / saggital dims = 0, 0, 0, 0, 2, 2, 0, 0
declare -A sequencesflipdims=(  ['flair_tra']="0" ['dw_tra_b1000_dmean']="0" ['adc_tra']="0" ['t1_tra_ffe']="0" \
				['t1_sag_tfe']="2" ['t2_sag_tse']="2" ['t2_tra_ffe']="0" ['t2_tra_tse']="0" )


# Image collection HEOPKS details
c01dir="/imagedata/HEOPKS/data/"
declare -A c01indicesmapping=(  ["01"]="01" ["02"]="02" ["03"]="03" ["04"]="04" ["05"]="05" ["06"]="06" ["07"]="07" ["08"]="08" ["09"]="09" ["10"]="10" \
				["11"]="11" ["12"]="12" ["13"]="13" ["14"]="14" ["15"]="15" ["16"]="16" ["17"]="17" ["18"]="18" ["19"]="19" ["20"]="20" \
				["21"]="21" ["22"]="22" ["23"]="23" ["24"]="24" ["25"]="25" ["26"]="26" ["27"]="27" ["28"]="28" ["29"]="29" )

# Image collection JGABLENTZ details
c02dir="/imagedata/JGABLENTZ/data/"
declare -A c02indicesmapping=(	["30"]="02" ["31"]="08" ["32"]="11" ["33"]="13" ["34"]="14" ["35"]="17" ["36"]="19" ["37"]="20" ["38"]="25" ["39"]="29" \
				["40"]="30" ["41"]="31" ["42"]="34" ["43"]="47" ["44"]="55" ["45"]="57" )


# functions
###
# Create an ADC map if required sequences are available
###
function make_adc_map () {
	srcdir=$1
	trgfile=$2

	if [ -f "${srcdir}/dw_tra_b0_dmean.${imgfiletype}" ]; then
		if [ -f "${srcdir}/dw_tra_b1000_dmean.${imgfiletype}" ]; then
			log 1 "Computing ADC map ${trgfile} with b=1000" "[$BASH_SOURCE:$FUNCNAME:$LINENO]"
			runcond "medpy_apparent_diffusion_coefficient.py ${srcdir}/dw_tra_b0_dmean.${imgfiletype} ${srcdir}/dw_tra_b1000_dmean.${imgfiletype} 1000 ${trgfile}"
		elif [ -f "${srcdir}/dw_tra_b3000_dmean.${imgfiletype}" ]; then
			log 1 "Computing ADC map ${trgfile} with b=3000" "[$BASH_SOURCE:$FUNCNAME:$LINENO]"
			runcond "medpy_apparent_diffusion_coefficient.py ${srcdir}/dw_tra_b0_dmean.${imgfiletype} ${srcdir}/dw_tra_b3000_dmean.${imgfiletype} 3000 ${trgfile}"
		fi
	fi
}

###
# Link all the sequences of a case
###
function link_case () {

	srcdir=$1
	idx=$2

	log 2 "Linking case ${idx} from ${srcdir}" "[$BASH_SOURCE:$FUNCNAME:$LINENO]"
	mkdircond "${originals}/${idx}"

	for s in "${sequencestolink[@]}"; do
		srcfile="${srcdir}/${s}.${imgfiletype}"
		trgfile="${originals}/${idx}/${s}.${imgfiletype}"

		# continue if target file already exists
		if [ -f "${trgfile}" ]; then
			log 1 "Target file ${trgfile} already exists. Skipping." "[$BASH_SOURCE:$FUNCNAME:$LINENO]"
			continue
		fi

		# if source file exists
		if [ -f "${srcfile}" ]; then		
			log 1 "Copying, to float62 and metadata correction for ${srcfile} to ${trgfile}" "[$BASH_SOURCE:$FUNCNAME:$LINENO]"
			# copy and convert datatype to float64
			runcond "${scripts}/tofloat64.py ${srcfile} ${trgfile}"
			# correct nifit orientation metadata in-place
			runcond "${scripts}/niftimodifymetadata.py ${trgfile} qf=aff sf=aff qfc=1 sfc=1"
		elif [ "${s}" == "adc_tra" ]; then # compute ADC map if possible
			make_adc_map "${srcdir}" "${trgfile}"
			if [ ! -f "${trgfile}" ]; then
				log 1 "No sequence ${s} found for this case" "[$BASH_SOURCE:$FUNCNAME:$LINENO]"
			fi	
		else
			log 1 "No sequence ${s} found for this case" "[$BASH_SOURCE:$FUNCNAME:$LINENO]"
		fi
	done
}

# main code
log 2 "Copying / converting images and correcting metadata" "[$BASH_SOURCE:$FUNCNAME:$LINENO]"
for i in "${images[@]}"; do
	if test "${c01indicesmapping[${i}]+isset}"; then
		link_case "${c01dir}/${c01indicesmapping[${i}]}" "${i}"
	elif test "${c02indicesmapping[${i}]+isset}"; then
		link_case "${c02dir}/${c02indicesmapping[${i}]}" "${i}"
	else
		log 3 "No candidate for case id ${i} found in any of the collections. Please check your 'images' array. Skipping." "[$BASH_SOURCE:$FUNCNAME:$LINENO]"
	fi
done

log 2 "Flipping images of every second case in-place along the mid-saggital plane" "[$BASH_SOURCE:$FUNCNAME:$LINENO]"
for (( i = 1 ; i < ${#images[@]} ; i+=2 )) do
	for s in "${sequencestolink[@]}"; do
		f="${originals}/${images[$i]}/${s}.${imgfiletype}"
		if [ -e ${f} ]; then
			lnrealize "${f}"
			runcond "${scripts}/flip.py ${f} ${sequencesflipdims[${s}]}"
		fi
	done
done

log 2 "Done." "[$BASH_SOURCE:$FUNCNAME:$LINENO]"

