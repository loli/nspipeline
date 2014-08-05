#!/bin/bash

#####
# Joins a number of sample sets together.
#####

## Changelog
# 2014-08-05 created

# include shared information
source $(dirname $0)/include.sh

from1="06samplesets/GTG"
from2="06samplesets/GTL"
to="06samplesets/GTGL"

# main code
log 2 "Joining sample sets" "[$BASH_SOURCE:$FUNCNAME:$LINENO]"
for i in "${images[@]}"; do
    echo $i
    mkdircond ${to}/${i}
    scripts/joinsamplesets.py ${from1}/${i} ${from2}/${i} ${to}/${i}
done
log 2 "Done." "[$BASH_SOURCE:$FUNCNAME:$LINENO]"


