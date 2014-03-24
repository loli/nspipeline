#!/bin/bash

########################################
# Include file with shared information #
########################################

## changelog
# 2014-03-24 Added the runcond function.
# 2013-11-14 Added new directories.
# 2013-11-11 Added new directories.
# 2013-10-31 Added new directories.
# 2013-10-22 Added new directories.
# 2013-10-21 Added new directories.
# 2013-10-15 Added new directories and made emptydircond a tick more save
# 2013-10-02 created

# folders
originals="00original/"
t2space="01t2space/"
t2skullstripped="02t2skullstripped/"
t2biasfieldcorrected="03t2biasfieldcorrected/"
t2intensitrangestandardization="04t2intensitrangestandardization/"
t2lesionsegmentation="05t2lesionsegmentation/"
stdspace="06stdspace"
stdskullstripped="07stdskullstripped/"
stdbiasfieldcorrected="08stdbiasfieldcorrected/"
stdintensitrangestandardization="09stdintensitrangestandardization/"
stdfeatureimages="10stdfeatureimages/"
stdlesionsegmentation="11stdlesionsegmentation/"


segmentations="100gtsegmentations/"
t2segmentations="101t2segmentations/"
t2brainmasks="102t2brainmasks/"
stdsegmentations="103stdsegmentations/"
stdbrainmasks="104stdbrainmasks/"

scripts="scripts/"
configs="configs/"

# image arrays
images=('03' '04' '05' '06' '07' '08' '09' '10' '11' '12' '13' '15' '17' '18' '19' '20' '21' '22' '23' '25' '26' '28' '29' '30' '31' '32' '33' '34' '35' '36' '37' '39' '40' '41' '42' '43' '44' '45')
sequences=("flair_tra") # sequences to use

# other constants
imgfiletype="nii.gz"
#stdspace=('0.44921875' '0.44921875' '0.99999148') # the minimal common space of all spectra

threadcount=6

# logging
loglevel=2 # 1=debug, 2=info, 3=warning, 4=err, 5+=silent
logprefixes=('DEBUG' 'INFO' 'WARNING' 'ERROR')
logprintlocation=false # true | false to print the location from where the log was triggered


# shared functions

######
## Signal a log message of a determined level
######
function log {
	level=${1}
	msg=${2}
	location=${3} # optional, should be [$SOURCE:$FUNCNAME:$LINENO], [$SOURCE::$LINENO] or similar

	loglevels=${#logprefixes[@]}	
	
	# check if current logging level is lower than the messages logging level
	if [ "$loglevel" -le "$level" ]
	then
		# determine the log type
		if [ "$level" -le "0" ]
		then
			prefix="UNKNOWN"
		elif [ "$level" -gt "$loglevels" ]
		then
			prefix="UNKNOWN"
		else
			prefix=${logprefixes[$level-1]}
		fi

		# print, according to logprintlocation, with or without location information
		if $logprintlocation
		then
			echo -e "${prefix}: ${msg} ${location}"
		else
			echo -e "${prefix}: ${msg}"
		fi
	fi
}

######
# Parallelizes a function-call by calling different subprocesses
######
# Note that the different calles are processed in chunks, each of which this functions waits for to terminate before executing the next one.
# Takes as first parameter the function, as second the number of process to spawn and as third the array of parameters to pass to the function.
# !The third argument is supposed to be an array and therefore has to be passes in the form "parameter[@]"
# Call like "parallelize fun 4 indices[@]"
function parallelize ()
{
	# Grab parameters
	fun=$1
	processes=$2
	declare -a parameters=("${!3}")
	
	# split $parameters into $processes sized chunks
	for i in $(seq 0 ${processes} ${#parameters[@]}); do # seq: from stepsize to
		declare -a parameterchunk="(${parameters[@]:$i:$processes})"
		# execute function in background for each parameter in the current chunk and then wait for their termination
		for parameter in "${parameterchunk[@]}"; do
			${fun} $parameter &
		done
		wait
	done
}

######
## Create the supplied directory if it does not yet exists
######
function mkdircond {
	directory=${1}

	if [ ! -d "$directory" ]
	then
		log 1 "Creating directory ${directory}." "[$BASH_SOURCE:$FUNCNAME:$LINENO]"
		mkdir ${directory}
	fi
}

######
## Remove all files (but not directories or write-protected files) from the supplied directory if it is not empty
######
function emptydircond {
	directory=${1}

	if [ -z "$directory" ]; then
		log 3 "Supplied an empty string to emptydircond function. This might be dangerous and is therefore ignored." "[$BASH_SOURCE:$FUNCNAME:$LINENO]"
	else
		filecount=`ls -al ${directory} | wc -l`
		if [ "$filecount" -gt "3" ]
		then
			rm ${directory}/*
		fi
	fi
}

#####
## Remove a dirctory if it exists
#####
function rmdircond {
	directory=${1}

	if [ -d "$directory" ]
	then
		rmdir ${directory}
	fi
}

#####
## Empties and removes a directory if it exists
#####
function removedircond {
	directory=${1}
	emptydircond ${directory}
	rmdircond ${directory}
}

#####
## Runs the passed command if no variable "dryrun" has been initialized with a non-empty value
#####
function runcond {
	cmd=$1
	if [[ -z "$dryrun" ]]; then
		$cmd
	else
		echo "DRYRUN: ${cmd}"
	fi
}

######
## Create a symlink if non existant or dead
######
function lncond {
	source=$1
	target=$2

	# Check if link does not exists or is a dead symlink
	if [ ! -e ${target} ]
	then
		# remove if a dead symlink
		if [ -L ${target} ]
		then
			log 1 "Removing dead symlink ${target}." [$BASH_SOURCE:$FUNCNAME:$LINENO]
			`rm ${target}`
		fi

		# create sym link if source file exists
		if [ -f ${source} ]
		then
			log 1 "Linking ${source} to ${target}." "[$BASH_SOURCE:$FUNCNAME:$LINENO]"
			ln -s ${source} ${target}
		else
			log 3 "${source} does not exists." "[$BASH_SOURCE:$FUNCNAME:$LINENO]"
		fi
	else
		log 1 "Target file ${target} already exists, skipping." [$BASH_SOURCE:$FUNCNAME:$LINENO]
	fi
}
