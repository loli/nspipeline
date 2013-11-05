#!/usr/bin/python

####
# Creates a Matlab script to warp the different MRI sequences to std-space.
# The method used is: SPM Normalize Write
# arg1: the sequence image to register to std-space
# arg2: the associated SPM transformation struct
# arg3: the target matlab script file
####

import sys

def main():
	imgfile = sys.argv[1]
	spmstruct = sys.argv[2]
	target = sys.argv[3]

	script = script_template.format(imgfile, spmstruct, spmstruct, imgfile)

	with open(target, 'w') as f:
		f.write(script)

script_template = """
% Script to warp the image {} to std-space using {}.

addpath '/home/maier/Applications/spm8'

matlabbatch{{1}}.spm.spatial.normalise.write.subj(1).matname = {{'{}'}};
matlabbatch{{1}}.spm.spatial.normalise.write.subj(1).resample = {{'{},1'}};

matlabbatch{{1}}.spm.spatial.normalise.write.roptions.preserve = 0;
matlabbatch{{1}}.spm.spatial.normalise.write.roptions.bb = [-78 -112 -50
                                                          78 76 85];
matlabbatch{{1}}.spm.spatial.normalise.write.roptions.vox = [1 1 1];
matlabbatch{{1}}.spm.spatial.normalise.write.roptions.interp = 1;
matlabbatch{{1}}.spm.spatial.normalise.write.roptions.wrap = [0 0 0];
matlabbatch{{1}}.spm.spatial.normalise.write.roptions.prefix = 'w';

spm('defaults', 'FMRI');
spm_jobman('initcfg');
spm_jobman('serial', matlabbatch);

exit;
"""

if __name__ == "__main__":
    main()
