#!/usr/bin/python

####
# Creates a Matlab script to register a FLAIR image to the std-space FLAIR template using a lesion mask to mask out pathological areas.
# The method used is: SPM Normalize Estimate
# arg1: the FLAIR image to register to std-space
# arg2: the associated lesion mask (note: must contain zeros in places of pathological tissue)
# arg3: the target matlab script file
####

import sys

def main():
	flairfile = sys.argv[1]
	lmask = sys.argv[2]
	target = sys.argv[3]

	script = script_template.format(flairfile, lmask, flairfile, lmask)

	with open(target, 'w') as f:
		f.write(script)

script_template = """
% Script to register the image {} to the std-space, taking into account the lesion mask {}.

addpath '/home/maier/Applications/spm8'

matlabbatch{{1}}.spm.spatial.normalise.est.subj(1).source = {{'{},1'}};
matlabbatch{{1}}.spm.spatial.normalise.est.subj(1).wtsrc = {{'{},1'}};
matlabbatch{{1}}.spm.spatial.normalise.est.eoptions.template = {{'/home/maier/Applications/spm8/templates/GG-366-FLAIR-1.0mm.nii,1'}};
matlabbatch{{1}}.spm.spatial.normalise.est.eoptions.weight = '';
matlabbatch{{1}}.spm.spatial.normalise.est.eoptions.smosrc = 8;
matlabbatch{{1}}.spm.spatial.normalise.est.eoptions.smoref = 8;
matlabbatch{{1}}.spm.spatial.normalise.est.eoptions.regtype = 'mni';
matlabbatch{{1}}.spm.spatial.normalise.est.eoptions.cutoff = 25;
matlabbatch{{1}}.spm.spatial.normalise.est.eoptions.nits = 16;
matlabbatch{{1}}.spm.spatial.normalise.est.eoptions.reg = 1;

spm('defaults', 'FMRI');
spm_jobman('initcfg');
spm_jobman('serial', matlabbatch);

exit;
"""

if __name__ == "__main__":
    main()
