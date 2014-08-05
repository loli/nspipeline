#!/bin/bash

######################
# Configuration file #
######################

## changelog
# 2014-05-08 created

# image array
images=('01' '02' '03' '04' '05' '06' '07' '08' '09' '10' '11')

# sequences to use and base sequence
sequences=("FLAIR" "PD" "T1mprageCE" "T1mprage" "T2") # sequences to use
basesequence="T1mprage" # base sequence for all operation sin sequence space

# sequence space settings
isotropic=0 # 0/1 to disable/enable pre-registration resampling of base sequence to isotropic spacing
isotropicspacing=1 # the target isotropic spacing in mm

# config file with feature (1) to extract and (2) to create the training sample from
featurecnf="featureconfig.py"

# training sample size
samplesize=500000

# rdf parameters
maxdepth=100

# post-processing parameters
minimallesionsize=0

