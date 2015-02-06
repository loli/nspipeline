#!/bin/bash

source $(dirname $0)/config.sh


for i in "${images[@]}"; do
    itksnap -s 100gtsegmentations/${i}.nii.gz 00original/${i}/T2.nii.gz &
    itksnap -s 08lesionsegmentation/${i}/segmentation.nii.gz 00original/${i}/T2.nii.gz
done
