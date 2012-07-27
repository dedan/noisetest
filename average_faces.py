#!/usr/bin/env python
# encoding: utf-8
"""
    anaylysis of the pickle created with face_detect.py
"""

import sys, os, pickle
import numpy as np
import pylab as plt

res_folder = '/Users/dedan/projects/bci/noisetest/res2'

n_images = 15
max_size = 50

# compute histogram
res = pickle.load(open(os.path.join(res_folder, 'res.pckl')))
widths = [p.shape[0] for p in res]
minw, maxw = np.min(widths), np.max(widths)
counts, bins = np.histogram(widths, range=(minw, maxw), bins=(maxw-minw))

indeces = list(reversed(np.argsort(counts.tolist()).tolist()))

# for i, idx in enumerate(indeces[:n_images]):

#     patches = [r for r in res if r.shape[0] == int(bins[idx])]
#     patches_mean = np.mean(np.array(patches), axis=0)

#     plt.figure()
#     plt.imshow(patches_mean, cmap=plt.cm.gray, interpolation='nearest')
#     plt.savefig(os.path.join(res_folder, 'patches_mean_%d.png' % i))

# take mean over all images up to a certain size. Needs interpolation to fit sizes
patches = [r for r in res if r.shape[0] <= max_size]
x_y_range = range(max_size)
patches_interpolated = []
for patch in patches:

    back = np.ones((max_size, max_size)) * 127
    patch_size = patch.shape[0]

    for i in range(patch_size):
        for j in range(patch_size):

            i_trans = np.floor((float(i) / patch_size) * max_size)
            j_trans = np.floor((float(j) / patch_size) * max_size)
            back[i_trans, j_trans] = patch[i, j]
    patches_interpolated.append(back)
    patches_inter_mean = np.mean(np.array(patches_interpolated), axis=0)

plt.figure()
plt.imshow(patches_inter_mean, cmap=plt.cm.gray, interpolation='nearest')
plt.savefig(os.path.join(res_folder, 'patches_inter.png'))




# take mean over all images up to a certain size. 'reverse interpolation'
patches = [r for r in res if r.shape[0] <= max_size]
min_size = np.min([p.shape[0] for p in patches])
patches_interpolated = []
for patch in patches:

    back = np.ones((min_size, min_size)) * 127
    patch_size = patch.shape[0]

    for i in range(patch_size):
        for j in range(patch_size):

            i_trans = np.floor((float(i) / patch_size) * min_size)
            j_trans = np.floor((float(j) / patch_size) * min_size)
            back[i_trans, j_trans] = patch[i, j]
    patches_interpolated.append(back)
    patches_inter_mean = np.mean(np.array(patches_interpolated), axis=0)

plt.figure()
plt.imshow(patches_inter_mean, cmap=plt.cm.gray, interpolation='nearest')
plt.savefig(os.path.join(res_folder, 'patches_inter_inv.png'))




