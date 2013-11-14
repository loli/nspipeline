#!/usr/bin/python

####
# Creates a Matlab script to segment the tissues from a T2 or T1 image.
# The method used is: SPM Segment
# arg1: the T1/T2 image to segment
# arg2: the associated brain mask
# arg3: the target matlab script file
####

import sys

def main():
	tfile = sys.argv[1]
	mask = sys.argv[2]
	target = sys.argv[3]

	script = script_template.format(tfile, mask, tfile, mask)

	with open(target, 'w') as f:
		f.write(script)

script_template = """
% Script to segment the tissues from image {} using brain mask {}.

addpath '/home/maier/Applications/spm8'

matlabbatch{{1}}.spm.spatial.preproc.data = {{'{},1'}};
matlabbatch{{1}}.spm.spatial.preproc.output.GM = [0 0 1];
matlabbatch{{1}}.spm.spatial.preproc.output.WM = [0 0 1];
matlabbatch{{1}}.spm.spatial.preproc.output.CSF = [0 0 1];
matlabbatch{{1}}.spm.spatial.preproc.output.biascor = 0;
matlabbatch{{1}}.spm.spatial.preproc.output.cleanup = 0;
matlabbatch{{1}}.spm.spatial.preproc.opts.tpm = {{
                                               '/home/maier/Applications/spm8/tpm/grey.nii'
                                               '/home/maier/Applications/spm8/tpm/white.nii'
                                               '/home/maier/Applications/spm8/tpm/csf.nii'
                                               }};
matlabbatch{{1}}.spm.spatial.preproc.opts.ngaus = [2
                                                 2
                                                 2
                                                 4];
matlabbatch{{1}}.spm.spatial.preproc.opts.regtype = '';
matlabbatch{{1}}.spm.spatial.preproc.opts.warpreg = 1;
matlabbatch{{1}}.spm.spatial.preproc.opts.warpco = 25;
matlabbatch{{1}}.spm.spatial.preproc.opts.biasreg = 0;
matlabbatch{{1}}.spm.spatial.preproc.opts.biasfwhm = 60;
matlabbatch{{1}}.spm.spatial.preproc.opts.samp = 3;
matlabbatch{{1}}.spm.spatial.preproc.opts.msk = {{'{},1'}};

spm('defaults', 'FMRI');
spm_jobman('initcfg');
spm_jobman('serial', matlabbatch);

exit;
"""

if __name__ == "__main__":
    main()
