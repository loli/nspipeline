#!/bin/bash

######################
# Configuration file #
######################

## changelog
# 2014-05-08 created

# image array
#images=('03' '04' '05' '06' '07' '08' '09' '10' '11' '12' '13' '15' '17' '18' '19' '20' '21' '22' '23' '25' '26' '28' '29' '30' '31' '32' '33' '34' '35' '36' '37' '39' '40' '41' '42' '43' '44' '45') # FLAIR
#images=('03' '05' '07' '09' '10' '11' '12' '13' '15' '17' '18' '22' '23' '25' '26' '31' '32' '33' '34' '35' '36' '37' '39' '40' '41' '42' '43' '44' '45') # DW/ADC
images=('03' '04' '05' '06' '07' '08' '09' '10' '11' '12' '13' '15' '17' '18' '20' '21' '22' '23' '25' '26' '28' '29') # T1_SAG_TFE
#images=('03' '05' '06' '07' '09' '10' '11' '12' '13' '15' '17' '18' '19' '20' '21' '22' '23' '25' '26' '29' '30' '32' '33' '34' '35' '36' '37' '39' '40' '41' '42' '43' '44' '45') # T2_SAG_TSE

# sequences to use and base sequence
sequences=("flair_tra") # "adc_tra" "dw_tra_b1000_dmean" "t1_tra_ffe" "t2_sag_tse" "t2_tra_ffe" "t2_tra_tse" "t1_sag_tfe") # sequences to use
basesequence="flair_tra" # base sequence for all operation sin sequence space

# sequence space settings
isotropic=1 # 0/1 to disable/enable pre-registration resampling of base sequence to isotropic spacing
isotropicspacing=3 # the target isotropic spacing in mm

# config file with feature (1) to extract and (2) to create the training sample from
featurecnf="featureconfig.py"

# training sample size
samplesize=250000

# rdf parameters
maxdepth=500

# post-processing paramters
minimallesionsize=1500

