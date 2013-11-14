#!/bin/bash

#####
# Link all segmentation images from the image database in a consitent manner.
#####

## Changelog
# 2013-10-21 created

# include shared information
source $(dirname $0)/include.sh

# Image collection HEOPKS details
c01dir="/imagedata/HEOPKS/segmentation/"
c01indicessrc=("03" "05" "07" "09" "11" "12" "13" "15" "18")
c01indicestrg=("01" "02" "03" "04" "05" "06" "07" "08" "09")

# Image collection JGABLENTZ details
c02dir="/imagedata/JGABLENTZ/segmentation/"
c02indicessrc=("11" "13" "14" "17" "19" "20" "29" "30" "31" "34" "47" "55" "57")
c02indicestrg=("10" "11" "12" "13" "14" "15" "16" "17" "18" "19" "20" "21" "22")

# main code
log 2 "Linking segmentations from collection ${c01dir}" "[$BASH_SOURCE:$FUNCNAME:$LINENO]"
for ((i = 0; i < ${#c01indicessrc[@]}; i++)); do
	lncond ${c01dir}/${c01indicessrc[$i]}.${imgfiletype} ${segmentations}/${c01indicestrg[$i]}.${imgfiletype}
done
log 2 "Done." "[$BASH_SOURCE:$FUNCNAME:$LINENO]"

log 2 "Linking / converting images from collection ${c02dir}" "[$BASH_SOURCE:$FUNCNAME:$LINENO]"
for ((i = 0; i < ${#c02indicessrc[@]}; i++)); do
	lncond ${c02dir}/${c02indicessrc[$i]}.${imgfiletype} ${segmentations}/${c02indicestrg[$i]}.${imgfiletype}
done
log 2 "Done." "[$BASH_SOURCE:$FUNCNAME:$LINENO]"
