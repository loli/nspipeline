#!/bin/bash

########################################
# Include file with shared information #
########################################

## changelog
# 2014-05-08 Adapted to the new, distributed calculation scheme.
# 2014-05-08 Transfered some settings to a config file and included it here.
# 2014-05-05 Removed normalized space directories.
# 2014-05-05 Added the lnrealize() function.
# 2014-03-25 Adapted directory structure.
# 2014-03-24 Added the runcond function.
# 2013-11-14 Added new directories.
# 2013-11-11 Added new directories.
# 2013-10-31 Added new directories.
# 2013-10-22 Added new directories.
# 2013-10-21 Added new directories.
# 2013-10-15 Added new directories and made emptydircond a tick more save
# 2013-10-02 created

# include the shared config file
source $(dirname $0)/config.sh

# folders
originals="00original/"
sequencespace="01flairspace/"
sequenceskullstripped="02flairskullstripped/"
sequencebiasfieldcorrected="03biasfieldcorrected/"
sequenceintensitrangestandardization="04flairintensitrangestandardization/"
sequencefeatures="05flairfeatures/"
sequencesamplesets="06samplesets/"
sequenceforests="07forests/"
sequencelesionsegmentation="08flairlesionsegmentation/"

segmentations="100gtsegmentations/"
sequencesegmentations="101flairsegmentations/"
sequencebrainmasks="102flairbrainmasks/"

scripts="scripts/"
configs="configs/"

# other constants
imgfiletype="nii.gz"
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
## Runs the passed command if no variable "dryrun" has been initialized with a non-empty value.
## As a second parameter a redirect target of the command std output can optionaly be passed.
#####
function runcond {
	cmd=$1
	if [[ -z "$dryrun" ]]; then
		if [ $# -gt 1 ]; then
			$cmd > $2
		else
			$cmd
		fi
	else
		echo "DRYRUN: ${cmd}"
	fi
}

######
## Copy a file if target file does not exist already
######
function cpcond {
	source=$1
	target=$2

	if [ ! -f ${source} ]; then
		log 3 "Source file ${source} does not exists. Skipping." "[$BASH_SOURCE:$FUNCNAME:$LINENO]"
	elif [ -f ${target} ]; then
		log 1 "Target file ${target} already exists, skipping." [$BASH_SOURCE:$FUNCNAME:$LINENO]
	else
		log 1 "Copying ${source} to ${target}." [$BASH_SOURCE:$FUNCNAME:$LINENO]
		runcond "cp ${source} ${target}"
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
		if [ -e ${source} ]
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

###
# Takes a symbolic link and makes it "real" i.e. replaces the link with a copy of the
# actual target file.
###
lnrealize() {
	if [ -L ${1} ]
	then
		runcond "cp --remove-destination `readlink ${1}` ${1}"
	fi
}

#####
## Checks whether an element exists in an array
## Call like: isIn "element" "${array[@]}"
#####
isIn () {
  local e
  for e in "${@:2}"; do [[ "$e" == "$1" ]] && return 0; done
  return 1
}

###
# Join the elements of an array using a one-character delimiter
# Call like: joinarr $delimiter ${arr[@]}
###
function joinarr () {
	local IFS="${1}"
	shift
	echo "$*"
}

#####
# Returns a new version of an array with the passed element removed from it.
# Call like: newarray=( $(delEl element array[@]) )
# If the element could not be found, the original array is returned
# Exit codes (available from $?): 0 on success, 1 if the element could not be found
#####
function delEl {
	declare -a arr=("${!2}") # Note: decalre has scope limited to function
	local pos=$(isAt $1 arr[@])
	if [[ $pos -lt 0 ]]; then echo "${arr[@]}" && return 1; fi
	local newarr=(${arr[@]:0:$pos} ${arr[@]:$(($pos + 1))})
	echo "${newarr[@]}"
	return 0
}

#####
# Returns the position of the first occurence of an element in an array.
# Call like: pos=$(isAt element array[@])
# If the element could not be found, the return value (not! exit code) will be a negative integer
# Exit codes (available from $?): 0 on success, 1 if the element could not be found
#####
isAt () {
	declare -a arr=("${!2}")
	local e
	for e in "${!arr[@]}"; do [[ "${arr[$e]}" == "$1" ]] && echo ${e} && return 0; done
	echo -1
	return 1
}

###
# Returns the voxel spacing of supplied image as space separated string
# To catch as array, use var=( $(voxelspacing "imagelocation") )
###
function voxelspacing () {
	local image=$1
	local vss=`medpy_info.py "${image}" | grep "spacing"`
	local vse=${vss:15:-1}
	local vs=(${vse//, / })
	echo "${vs[@]}"
}
