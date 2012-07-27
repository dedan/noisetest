#!/usr/bin/env python
# encoding: utf-8
"""
    use the face detection of opencv on noise images

    the noise is white with some correlations induced by convolution with
    a rectangular kernel

    Created by stephan.gabler@gmail.com on 2012-01-27.
    Copyright (c) 2012. All rights reserved.
"""

import sys, os, pickle, json, datetime
import cv
import numpy as np
import pylab as plt
from scipy import signal

out_path = '/Users/dedan/projects/bci/noisetest/results/'
image_size = 100
iterations = 100
kernels = [3, 5, 10]
xml_files = ['haarcascade_frontalface_default.xml',
             'haarcascade_eye.xml',
             'haarcascade_frontalface_alt.xml']

for kernel_size in kernels:

    for xml_file in xml_files:

        info = {'kernel': kernel_size, 'xml_file': xml_file,
                'image_size': image_size, 'iterations': iterations,
                'noise_times': [], 'detection_times': []}
        kernel = np.ones((kernel_size, kernel_size))
        res = []
        hc = cv.Load('/usr/local/share/opencv/haarcascades/' + xml_file)

        noise_times, dect_times = [], []
        for i in range(iterations):

            t = cv.GetTickCount()
            rand_im = np.random.rand(image_size, image_size)
            im = signal.convolve(rand_im, kernel, mode='valid')
            im = ((im / np.max(im)) * 255).astype(np.uint8)
            img = cv.fromarray(im)
            noise_times.append(cv.GetTickCount() - t)

            faces = cv.HaarDetectObjects(img, hc, cv.CreateMemStorage(), 1.2, 1,
                                         cv.CV_HAAR_DO_CANNY_PRUNING)
            dect_times.append(cv.GetTickCount() - t)

            if len(faces) > 1:
                print 'more than one face in an image'
            for (x,y,w,h), _ in faces:
                res.append(im[y+1:y+h, x+1:x+w])

        info['noise_times'] = np.mean(noise_times) / (cv.GetTickFrequency()*1000.)
        info['detection_times'] = np.mean(dect_times) / (cv.GetTickFrequency()*1000.)
        timestamp = datetime.datetime.now().strftime('%d%m%y_%H%M%S')
        tmp_folder = os.path.join(out_path, timestamp)
        os.mkdir(tmp_folder)
        pickle.dump(res, open(os.path.join(tmp_folder, 'res.pckl'), 'w'))
        json.dump(info, open(os.path.join(tmp_folder, 'info.json'), 'w'))

