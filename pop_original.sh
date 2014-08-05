#!/bin/bash

#####
# Link images and segmentations from the image database in a consitent manner to their respective base folders.
#####

## Changelog
# 2014-08-05 created

# include shared information
source $(dirname $0)/include.sh

# Image collection MSUKE details
datadir="/imagedata/MSUKE/data/"
segmdir="/imagedata/MSUKE/segmentation/"
declare -A indicesmapping=( ['865272935_20121016']="01"  ['974747069_20110812']="02"  ['975736566_20130121']="03"  ['976092126_20120330']="04"  ['976199806_20120823']="05"  ['976260087_20120119']="06"
['974558839_20120702']="07"  ['975379342_20111108']="08"  ['976061931_20120301']="09"  ['976124069_20111118']="10"  ['976248793_20120925']="11" )

# main code
log 2 "Linking the image folders and ground truth" "[$BASH_SOURCE:$FUNCNAME:$LINENO]"
for i in "${!indicesmapping[@]}"; do
    if [ ! -d "${datadir}/${i}" ]; then
        log 3 "No source folder ${datadir}/${i} found. Please check your 'indicesmapping' array. Skipping." "[$BASH_SOURCE:$FUNCNAME:$LINENO]"
        continue
    elif [ ! -f "${segmdir}/${i}.${imgfiletype}" ]; then
        log 3 "No source segmentation ${segmdir}/${i}.${imgfiletype} found. Please check your 'indicesmapping' array. Skipping." "[$BASH_SOURCE:$FUNCNAME:$LINENO]"
    fi
    lncond "${datadir}/${i}" "${originals}/${indicesmapping[${i}]}"
    lncond "${segmdir}/${i}.${imgfiletype}" "${segmentations}/${indicesmapping[${i}]}.${imgfiletype}"
done
log 2 "Done." "[$BASH_SOURCE:$FUNCNAME:$LINENO]"

