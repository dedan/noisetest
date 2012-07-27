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

for i, idx in enumerate(indeces[:n_images]):

    patches = [r for r in res if r.shape[0] == int(bins[idx])]
    patches_mean = np.mean(np.array(patches), axis=0)

    plt.figure()
    plt.imshow(patches_mean, cmap=plt.cm.gray, interpolation='nearest')
    plt.savefig(os.path.join(res_folder, 'patches_mean_%d.png' % i))

