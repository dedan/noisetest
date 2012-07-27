#!/usr/bin/python

# face_detect.py

# Face Detection using OpenCV. Based on sample code from:
# http://python.pastebin.com/m76db1d6b

# Usage: python face_detect.py <image_file>

import sys, os
import cv
import numpy as np
import pylab as plt
from scipy import signal

image_size = 100
kernel_size = 5
iterations = 1000

kernel = np.ones((kernel_size, kernel_size))

noise_creation_times = []
detection_times = []
img = cv.LoadImage('lena.jpeg', 0)

for i in range(iterations):

    t = cv.GetTickCount()
    rand_im = np.random.rand(image_size, image_size)
    im = signal.convolve(rand_im, kernel, mode='valid')

    im = ((im / np.max(im)) * 255).astype(np.uint8)
    img = cv.fromarray(im)

    noise_creation_times.append(cv.GetTickCount() - t)

    xml_file = 'haarcascade_frontalface_default.xml'
    # xml_file = 'haarcascade_eye.xml'
    # xml_file = 'haarcascade_frontalface_alt.xml'
    hc = cv.Load('/usr/local/share/opencv/haarcascades/' + xml_file)
    faces = cv.HaarDetectObjects(img, hc, cv.CreateMemStorage(), 1.2, 1,
                                 cv.CV_HAAR_DO_CANNY_PRUNING, (30, 30))
    detection_times.append(cv.GetTickCount() - t)

    for (x,y,w,h),n in faces:
        cv.Rectangle(img, (x,y), (x+w,y+h), 255)
    if faces:
        cv.SaveImage("faces_detected_%d.jpg" % i, img)

avg_noise_time = np.mean(noise_creation_times)
print "avg, noise creation time = %gms" % (avg_noise_time/(cv.GetTickFrequency()*1000.))
avg_detection_time = np.mean(detection_times)
print "avg, detection_times time = %gms" % (avg_detection_time/(cv.GetTickFrequency()*1000.))
