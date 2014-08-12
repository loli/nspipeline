#!/bin/bash

#####
# Adaptable pipeline script for running the whole or parts of the pipeline (distributed where deemed sensible)
#####

### CHANGELOG ###
# 2014-08-12 created

### SETTINGS ###
START="original"
LOGGING=true

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

function originals () {
    log 2 "### ORIGINALS: start ###" "[$BASH_SOURCE:$FUNCNAME:$LINENO]"
    runcondlog "pop_originals.sh" "originals"
    log 2 "### ORIGINALS: done ###" "[$BASH_SOURCE:$FUNCNAME:$LINENO]"
}

# !TODO: requires sequencespacebasesequence [define and use!]
function sequencespace () {
    log 2 "### SEQUENCESPACE: start ###" "[$BASH_SOURCE:$FUNCNAME:$LINENO]"
    runcondlog "pop_sequencespace.sh" "sequencespace"
    log 2 "### SEQUENCESPACE: done ###" "[$BASH_SOURCE:$FUNCNAME:$LINENO]"
}

function sequenceskullstripped () {

}
sequencebiasfieldcorrected="03biasfieldcorrected/"
sequenceintensitrangestandardization="04intensitrangestandardization/"
sequencefeatures="05features/"
sequencesamplesets="06samplesets/${gtset}/"
sequenceforests="07forests/${gtset}/"
sequencelesionsegmentation="08lesionsegmentation/${gtset}/"

segmentations="100gtsegmentations/${gtset}/"
sequencesegmentations="101sequencesegmentations/${gtset}/"
sequencebrainmasks="102sequencebrainmasks/"



### MAIN ###

