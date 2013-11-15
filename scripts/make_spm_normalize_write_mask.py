#!/usr/bin/python

####
# Creates a Matlab script to warp the different MRI sequences to std-space.
# This version is for warping binary files with a reduced bspline order.
# The method used is: SPM Normalize Write
# arg1: the target matlab script to create
# arg2: the SPM transformation struct containing the desired transformation
# arg3+: the image to transform
####

import sys

def main():
	target = sys.argv[1]
	spmstruct = sys.argv[2]

	combined_images = ' '.join(["'{},1'".format(img) for img in sys.argv[3:]])
	script = script_template.format(combined_images, spmstruct, spmstruct, combined_images)

	with open(target, 'w') as f:
		f.write(script)

script_template = """
% Script to warp the images {} to std-space using {}.

addpath '/home/maier/Applications/spm8'

matlabbatch{{1}}.spm.spatial.normalise.write.subj(1).matname = {{'{}'}};
matlabbatch{{1}}.spm.spatial.normalise.write.subj(1).resample = {{{}}};

matlabbatch{{1}}.spm.spatial.normalise.write.roptions.preserve = 0;
matlabbatch{{1}}.spm.spatial.normalise.write.roptions.bb = [-78 -112 -50
                                                          78 76 85];
matlabbatch{{1}}.spm.spatial.normalise.write.roptions.vox = [1 1 1];
matlabbatch{{1}}.spm.spatial.normalise.write.roptions.interp = 0;
matlabbatch{{1}}.spm.spatial.normalise.write.roptions.wrap = [0 0 0];
matlabbatch{{1}}.spm.spatial.normalise.write.roptions.prefix = 'w';

spm('defaults', 'FMRI');
spm_jobman('initcfg');
spm_jobman('serial', matlabbatch);

exit;
"""

if __name__ == "__main__":
    main()
