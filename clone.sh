#!/bin/bash

######
# Clone directory for experiments (first phase)
# call with: source <file>.sh, otherwise environement variables won't get set
# MedPy requires:
#	sudo apt-get install build-essential python-dev python-numpy python-setuptools python-scipy libatlas-dev python-pip
#	pip install -U nibabel
#	pip install -U scikit-learn
#
#	cp /share/data_humbug1/maier/Temp_Pipeline/Pipeline/clone.sh .
#
#	export PYTHONPATH=${PYTHONPATH}:/home/maier/Libraries/Python:/home/maier/Workspacepython/medpy
#	export PATH=$PATH:/home/maier/Workspacepython/medpy/bin
######

base="/share/data_humbug1/maier/Temp_Pipeline/NeuroImagePipeline/"

cp ${base}/config.sh .
cp ${base}/featureconfig.py .
ln -s ${base}/include.sh .

ln -s ${base}/logs .
#ln -s ${base}/scripts .
cp -r ${base}/scripts .

ln -s ${base}/00original
ln -s ${base}/01flairspace
ln -s ${base}/02flairskullstripped
ln -s ${base}/03biasfieldcorrected
ln -s ${base}/04flairintensitrangestandardization
ln -s ${base}/05flairfeatures
#ln -s ${base}/06samplesets
#ln -s ${base}/07forests
#ln -s ${base}/08flairlesionsegmentation

ln -s ${base}/100gtsegmentations
ln -s ${base}/102flairbrainmasks
ln -s ${base}/101flairsegmentations

#mkdir 01flairspace
#mkdir 02flairskullstripped
#mkdir 03biasfieldcorrected
#mkdir 04flairintensitrangestandardization
#mkdir 05flairfeatures
mkdir 06samplesets
mkdir 07forests
mkdir 08flairlesionsegmentation

#mkdir 102flairbrainmasks
#mkdir 101flairsegmentations

#ln -s ${base}/pop_sequencespace.sh .
#ln -s ${base}/pop_sequenceskullstripped.sh .
#ln -s ${base}/pop_sequencesegmentations.sh .
#ln -s ${base}/pop_sequencebiasfieldcorrected.sh .
#ln -s ${base}/pop_sequenceintensitrangestandardization.sh .
#ln -s ${base}/pop_sequencefeatures.sh .
ln -s ${base}/pop_sequencesamplesets.sh .
ln -s ${base}/pop_sequencetrainforests.sh .
ln -s ${base}/pop_sequencelesionsegmentation.sh .

ln -s ${base}/evaluate_original.sh .
cp ${base}/execute.sh .

export PYTHONPATH=/home/maier/Workspacepython/medpy
export PATH=${PATH}:/home/maier/Workspacepython/medpy/bin
