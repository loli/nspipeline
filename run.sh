#!/bin/bash

#####
# Adaptable pipeline script for running the whole or parts of the pipeline (distributed where deemed sensible)
#####

### CHANGELOG ###
# 2014-08-12 created

### SETTINGS ###
START="original"
LOGGING=true
#!TODO: Add usage of different sample sets
#!TODO: Add array of machines

### INCLUDES ###
source $(dirname $0)/include.sh

### CONSTANTS ###
LOGDIR='logs/'

### FUNCTIONS ###
# Executes runcond, but also with a logging if enabled
function runcondlog () {
    local cmd=$1
    local logfile=$2
    if [ "$LOGGING" = true ] ; then
        runcond "${cmd}" "${LOGDIR}/${logfile}.log"
    else
        runcond "${cmd}"
    fi
}

function originals () {
    log 2 "### ORIGINALS: start ###" "[$BASH_SOURCE:$FUNCNAME:$LINENO]"
    runcondlog "pop_originals.sh" "originals"
    log 2 "### ORIGINALS: done ###" "[$BASH_SOURCE:$FUNCNAME:$LINENO]"
}

function sequencespace () {
    log 2 "### SEQUENCESPACE: start ###" "[$BASH_SOURCE:$FUNCNAME:$LINENO]"
    runcondlog "pop_sequencespace.sh" "sequencespace"
    log 2 "### SEQUENCESPACE: done ###" "[$BASH_SOURCE:$FUNCNAME:$LINENO]"
}

function sequenceskullstripped () {
    log 2 "### SEQUENCESKULLSTRIP: start ###" "[$BASH_SOURCE:$FUNCNAME:$LINENO]"
    runcondlog "pop_sequenceskullstripped.sh" "sequenceskullstrip"
    log 2 "### SEQUENCESKULLSTRIP: done ###" "[$BASH_SOURCE:$FUNCNAME:$LINENO]"
}

function sequencebiasfieldcorrected () {
    log 2 "### SEQUENCEBIASFIELD: start ###" "[$BASH_SOURCE:$FUNCNAME:$LINENO]"
    runcondlog "pop_sequencebiasfieldcorrected.sh" "sequencebiasfield"
    log 2 "### SEQUENCEBIASFIELD: done ###" "[$BASH_SOURCE:$FUNCNAME:$LINENO]"
}

#!TODO: Check that this works
function sequenceintensitrangestandardization () {
    log 2 "### SEQUENCEINTENSITYRANGESTD: start ###" "[$BASH_SOURCE:$FUNCNAME:$LINENO]"
    runcondlog "pop_sequenceintensitrangestandardization.sh" "sequenceintensityrangestd"
    log 2 "### SEQUENCEINTENSITYRANGESTD: done ###" "[$BASH_SOURCE:$FUNCNAME:$LINENO]"
}

#!TODO: Check that this works
function sequencefeatures () {
    log 2 "### SEQUENCEFEATURES: start ###" "[$BASH_SOURCE:$FUNCNAME:$LINENO]"
    runcondlog "pop_sequencefeatures.sh" "sequencefeatures"
    log 2 "### SEQUENCEFEATURES: done ###" "[$BASH_SOURCE:$FUNCNAME:$LINENO]"
}

function sequencesamplesets () {
    log 2 "### SEQUENCESAMPLESETS: start ###" "[$BASH_SOURCE:$FUNCNAME:$LINENO]"
    runcondlog "pop_sequencesamplesets.sh" "sequencesamplesets"
    log 2 "### SEQUENCESAMPLESETS: done ###" "[$BASH_SOURCE:$FUNCNAME:$LINENO]"
}

function sequenceforests () {
    log 2 "### SEQUENCEFORESTS: start ###" "[$BASH_SOURCE:$FUNCNAME:$LINENO]"
    runcondlog "pop_sequencetrainforests.sh" "sequencetrainforests"
    log 2 "### SEQUENCEFORESTS: done ###" "[$BASH_SOURCE:$FUNCNAME:$LINENO]"
}

function sequencelesionsegmentation () {
    log 2 "### SEQUENCELESIONSEGMENTATION: start ###" "[$BASH_SOURCE:$FUNCNAME:$LINENO]"
    runcondlog "pop_sequencelesionsegmentation.sh" "sequencelesionsegmentation"
    log 2 "### SEQUENCELESIONSEGMENTATION: done ###" "[$BASH_SOURCE:$FUNCNAME:$LINENO]"
}

function segmentations () {
    log 2 "### SEGMENTATIONS: start ###" "[$BASH_SOURCE:$FUNCNAME:$LINENO]"
    runcondlog "pop_segmentations.sh" "segmentations.sh "
    log 2 "### SEGMENTATIONS: done ###" "[$BASH_SOURCE:$FUNCNAME:$LINENO]"
}

function sequencesegmentations () {
    log 2 "### SEQUENCESEGMENTATIONS: start ###" "[$BASH_SOURCE:$FUNCNAME:$LINENO]"
    runcondlog "pop_sequencesegmentations.sh" "sequencesegmentations.sh "
    log 2 "### SEQUENCESEGMENTATIONS: done ###" "[$BASH_SOURCE:$FUNCNAME:$LINENO]"
}

function createfolderstructure () {
    for folder in "${folders[@]}"; do
        mkdircond ${folder}
    done
}

### MAIN ###
#!TODO: Create directory structure if not existant!

