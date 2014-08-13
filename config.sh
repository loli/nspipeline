#!/bin/bash

######################
# Configuration file #
######################

## changelog
# 2014-08-12 adapted to run script
# 2014-05-08 created

# image array
# INCLUSIVE (training)
#images=('03' '04' '05' '06' '07' '08' '09' '10' '11' '12' '13' '15' '17' '18' '19' '20' '21' '23' '25' '26' '28' '29' '30' '31' '32' '33' '34' '35' '36' '37' '39' '40' '41' '42' '43' '44' '45') # FLAIR
#images=('03' '05' '07' '09' '10' '11' '12' '13' '15' '17' '18' '23' '25' '26' '31' '32' '33' '34' '35' '36' '37' '39' '40' '41' '42' '43' '44' '45') # DW/ADC
#images=('03' '04' '05' '06' '07' '08' '09' '10' '11' '12' '13' '15' '17' '18' '20' '21' '23' '25' '26' '28' '29') # T1_SAG_TFE
#images=('03' '05' '07' '09' '10' '11' '12' '13' '15' '17' '18' '23' '25' '26') # DW/ADC + T1_SAG_TFE

# EXCLUSIVE (preparation & application)
#images=('03' '05' '07' '09' '10' '11' '12' '13' '15' '17' '18' '23' '25' '26') # FLAIR + DW/ADC + T1_SAG_TFE
#images=('04' '06' '08' '20' '21' '28' '29') # FLAIR + T1_SAG_TFE
#images=('19' '30' '31' '32' '33' '34' '35' '36' '37' '39' '40' '41' '42' '43' '44' '45') # FLAIR only

# ground truth sets and settings
gtsets=("GTG" "GTL")
declare -A gtsources=( ["GTG"]="segmentation_G" ["GTL"]="segmentation_L" )

# sequence combinations settings
sc_ids=("1" "2" "3")
allimages=('03' '04' '05' '06' '07' '08' '09' '10' '11' '12' '13' '15' '17' '18' '19' '20' '21' '23' '25' '26' '28' '29' '30' '31' '32' '33' '34' '35' '36' '37' '39' '40' '41' '42' '43' '44' '45')
declare -A sc_sequences=( ["1"]="flair_tra" ["2"]="flair_tra t1_sag_tfe" ["3"]="flair_tra t1_sag_tfe dw_tra_b1000_dmean" )
declare -A sc_apply_images=( ["1"]="19 30 31 32 33 34 35 36 37 39 40 41 42 43 44 45" \
                             ["2"]="04 06 08 20 21 28 29" \
                             ["3"]="03 05 07 09 10 11 12 13 15 17 18 23 25 26" )
declare -A sc_train_images=( ["1"]="03 04 05 06 07 08 09 10 11 12 13 15 17 18 19 20 21 23 25 26 28 29 30 31 32 33 34 35 36 37 39 40 41 42 43 44 45" \
                             ["2"]="03 04 05 06 07 08 09 10 11 12 13 15 17 18 20 21 23 25 26 28 29" \
                             ["3"]="03 05 07 09 10 11 12 13 15 17 18 23 25 26" )
declare -A sc_train_brainmasks=( ["1"]="flair_tra" ["2"]="t1_sag_tfe" ["3"]="t1_sag_tfe" )
sequencespacebasesequence="flair_tra"

# sequence space settings
isotropic=1 # 0/1 to disable/enable pre-registration resampling of base sequence to isotropic spacing
isotropicspacing=3 # the target isotropic spacing in mm

# config file with feature (1) to extract and (2) to create the training sample from
featurecnf="featureconfig.py"

# training sample size
samplesize=250000

# rdf parameters
maxdepth=100

# post-processing parameters
minimallesionsize=1500

##
# functions
##
# build a custom, hidden feature config file for each sequence combinations
function makecustomfeatureconfigs () {
    local scid
    for scid in "${sc_ids[@]}"; do
        local sequences=( ${sc_sequences[$scid]} )
        local sequences_sum=$(joinarr "+" ${sequences[@]})
        local string="features_to_extract = ${sequences_sum}"
        local sc_featurecnf=".${featurecnf:0: -3}_${scid}.py"
        runcond "cp ${featurecnf} ${sc_featurecnf}"
        #!NOTE: Not very nice, as runcond is omitted. But I didn't find a solution to get the piping working otherwise.
        echo "${string}" >> "${sc_featurecnf}"
    done
}

