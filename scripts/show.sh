#!/bin/bash

######
# Displays the .nii.gz images in the supplied location with amide.
######

# changelog
# 2013-11-11 created

echo "Displaying images from ${i} with amide:"

tmpdir=`mktemp -d`
echo "Using temporary directory ${tmpdir}..."

echo "Unpacking images..."
for f in "${1}"/*.nii.gz; do
	fn=`basename $f .nii.gz`
	medpy_convert.py "${f}" "${tmpdir}/${fn}.nii"
done

echo "Displaying images..."
amide ${tmpdir}/t2_sag_tse.nii ${tmpdir}/*.nii ${tmpdir}/*.nii

echo "Cleaning up..."
rm ${tmpdir}/*
rmdir ${tmpdir}
echo "done."

