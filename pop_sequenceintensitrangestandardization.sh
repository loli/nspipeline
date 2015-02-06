#!/bin/bash

#####
# Standarizes the intensity profiles of all images by simply adapting mean and std.
#####

## Changelog
# 2014-08-11 Simple intensity normalization

# include shared information
source $(dirname $0)/include.sh

# main code
log 2 "Normalizing intensities" "[$BASH_SOURCE:$FUNCNAME:$LINENO]"
for i in "${images[@]}"; do
    mkdircond ${sequenceintensitrangestandardization}/${i}
    for s in "${sequences[@]}"; do
        if [[ $s =~ .*PM.* ]]; then
            runcond "cp ${sequencebiasfieldcorrected}/${i}/${s}.${imgfiletype} ${sequenceintensitrangestandardization}/${i}/${s}.${imgfiletype}"
        else
            runcond "${scripts}/naive_intensity_std.py ${sequencebiasfieldcorrected}/${i}/${s}.${imgfiletype} ${sequencebrainmasks}/${i}.${imgfiletype} ${sequenceintensitrangestandardization}/${i}/${s}.${imgfiletype}"
        fi
    done
done
log 2 "Done." "[$BASH_SOURCE:$FUNCNAME:$LINENO]"


