#!/usr/bin/env python
# encoding: utf-8
"""
    anaylysis of the pickle created with face_detect.py
"""

import sys, os, pickle, json
import numpy as np
import pylab as plt

n_images = 10
max_size = 50

res_folder = '/Users/dedan/projects/bci/noisetest/results'
folders = [f for f in os.listdir(res_folder) if not f[0] == '.']

for folder in folders:

    res = pickle.load(open(os.path.join(res_folder, folder, 'res.pckl')))
    info = json.load(open(os.path.join(res_folder, folder, 'info.json')))

    print('workin on new data from folder: %s' % folder)
    print('\t%d faces detected in %d iterations -> fraction: %f' %
            (len(res), info['iterations'], float(len(res)) / info['iterations']))
    print('\tkernel_width: %d\n\txml_file: %s' % (info['kernel'], info['xml_file']))
    print('\taverage noise time: %0.2f\n\taverage detection time: %0.2f' %
            (info['noise_times'], info['detection_times']))

    if not len(res) > 1:
        print 'no faces detected'
        continue

    # size histogram plot
    plt.figure()
    plt.hist([r.shape[0] for r in res])
    plt.savefig(os.path.join(res_folder, folder, 'sizes_hist.png'))

    # compute histogram
    widths = [p.shape[0] for p in res]
    minw, maxw = np.min(widths), np.max(widths)
    counts, bins = np.histogram(widths, range=(minw, maxw), bins=(maxw-minw))
    indeces = list(reversed(np.argsort(counts.tolist()).tolist()))

    for i, idx in enumerate(indeces[:n_images]):

        patches = [r for r in res if r.shape[0] == int(bins[idx])]
        patches_mean = np.mean(np.array(patches), axis=0)

        if not np.any(np.isnan(patches_mean)):
            plt.figure()
            plt.imshow(patches_mean, cmap=plt.cm.gray, interpolation='nearest')
            plt.savefig(os.path.join(res_folder, folder, 'patches_mean_%d.png' % i))

    # take mean over all images up to a certain size. Needs interpolation to fit sizes
    patches = [r for r in res if r.shape[0] <= max_size]
    min_size = np.min([p.shape[0] for p in patches])
    patches_interpolated = []
    patches_rev_interpolated = []
    for patch in patches:

        back_inter = np.ones((max_size, max_size)) * 127
        back_rev_inter = np.ones((min_size, min_size)) * 127

        patch_size = patch.shape[0]

        for i in range(patch_size):
            for j in range(patch_size):

                i_trans = np.floor((float(i) / patch_size) * max_size)
                j_trans = np.floor((float(j) / patch_size) * max_size)
                back_inter[i_trans, j_trans] = patch[i, j]

                i_trans = np.floor((float(i) / patch_size) * min_size)
                j_trans = np.floor((float(j) / patch_size) * min_size)
                back_rev_inter[i_trans, j_trans] = patch[i, j]

        patches_interpolated.append(back_inter)
        patches_rev_interpolated.append(back_rev_inter)

    plt.figure()
    patches_inter_mean = np.mean(np.array(patches_interpolated), axis=0)
    plt.imshow(patches_inter_mean, cmap=plt.cm.gray, interpolation='nearest')
    plt.savefig(os.path.join(res_folder, folder, 'patches_inter.png'))
    plt.figure()
    patches_rev_inter_mean = np.mean(np.array(patches_rev_interpolated), axis=0)
    plt.imshow(patches_rev_inter_mean, cmap=plt.cm.gray, interpolation='nearest')
    plt.savefig(os.path.join(res_folder, folder, 'patches_rev_inter.png'))
