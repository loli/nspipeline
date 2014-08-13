#!/usr/bin/python

#####
# Simple script to check improvements in the intensity range standardization over a large amount of image
# arg1: folder with before images and a {} where the image id should go
# arg2: folder with after images and a {} where the image id should go
# arg3: folder with the brain masks and a {} where the image id should go
# arg4: folder with the lesion masks and a {} where the image id should go
#####

import sys
import os
import numpy
from medpy.io import load

images=('03', '04', '05', '06', '07', '08', '09', '10', '11', '12', '13', '15', '17', '18', '19', '20', '21', '23', '25', '26', '28', '29', '30', '31', '32', '33', '34', '35', '36', '37', '39', '40', '41', '42', '43', '44', '45')

_pre = sys.argv[1]
_post = sys.argv[2]
_msk = sys.argv[3]
_les = sys.argv[4]

pre_means = []
post_means = []
pre_std = []
post_std = []
pre_means_lesion = []
post_means_lesion = []

for i in images:
    if not os.path.exists(_pre.format(i)):
        continue
        
    ipre, _ = load(_pre.format(i))
    ipost, _ = load(_post.format(i))
    msk = load(_msk.format(i))[0].astype(numpy.bool)
    les = load(_les.format(i))[0].astype(numpy.bool)
    
    pre_means.append(ipre[msk].mean())
    post_means.append(ipost[msk].mean())
    pre_std.append(ipre[msk].std())
    post_std.append(ipost[msk].std())
    
    pre_means_lesion.append(ipre[les].mean())
    post_means_lesion.append(ipost[les].mean())
    

print '\t\tBEFORE\t\tAFTER'
print '\t\t------\t\t-----'
print 'mean-std\t{}\t{}'.format(numpy.std(pre_means), numpy.std(post_means))
print 'mean-max-diff\t{}\t{}'.format(numpy.max(pre_means) - numpy.min(pre_means), numpy.max(post_means) - numpy.min(post_means))
print
print 'std-std\t\t{}\t{}'.format(numpy.std(pre_std), numpy.std(post_std))
print
print 'les-mean-std\t{}\t{}'.format(numpy.std(pre_means_lesion), numpy.std(post_means_lesion))
print 'les-mean-mdiff\t{}\t{}'.format(numpy.max(pre_means_lesion) - numpy.min(pre_means_lesion), numpy.max(post_means_lesion) - numpy.min(post_means_lesion))



