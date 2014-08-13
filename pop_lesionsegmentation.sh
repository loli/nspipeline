#!/bin/bash

#####
# APplyies the forests to a (preliminary) segmentation of the brain lesion in sequence space.
#####

## Changelog
# 2014-05-08 Adapted to the new, distributed calculation scheme.
# 2013-04-03 Added a morphological post-processing step (and removed again).
# 2013-03-25 Updated to new, variable version.
# 2013-11-25 Updated to use new script to distinguish between sequence space and std space features
# 2013-11-05 adapted to new brain mask location
# 2013-10-29 created

# include shared information
source $(dirname $0)/include.sh

# main code
log 2 "Applying random decision forests to segment lesion" "[$BASH_SOURCE:$FUNCNAME:$LINENO]"
for i in "${images[@]}"; do
	mkdircond ${sequencelesionsegmentation}/${i}
	runcond "${scripts}/apply_rdf.py ${sequenceforests}/${i}.pkl ${sequencefeatures}/${i}/ ${sequencebrainmasks}/${i}.nii.gz ${featurecnf} ${sequencelesionsegmentation}/${i}/segmentation.nii.gz ${sequencelesionsegmentation}/${i}/probabilities.nii.gz"
done

log 2 "Morphological post-processing" "[$BASH_SOURCE:$FUNCNAME:$LINENO]"
function post_processing ()
{
	i=$1
	runcond "${scripts}/remove_small_objects.py ${sequencelesionsegmentation}/${i}/segmentation.nii.gz ${sequencelesionsegmentation}/${i}/segmentation_post.nii.gz ${minimallesionsize}"
}
parallelize post_processing ${threadcount} images[@]

log 2 "Done." "[$BASH_SOURCE:$FUNCNAME:$LINENO]"


