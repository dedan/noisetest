from matplotlib.widgets import Button
from scipy import signal
import numpy as np
import pylab as plt

image_size = 100
kernel_size = 5

kernel = np.ones((kernel_size, kernel_size))
im = signal.convolve(np.random.random((image_size, image_size)), kernel)

ax = plt.subplot(121)
l = ax.imshow(im, cmap=plt.cm.gray, interpolation='nearest')
ax.set_xticks([])
ax.set_yticks([])
ax.set_xlabel('noise')

ax = plt.subplot(122)
m = ax.imshow(im, cmap=plt.cm.gray, interpolation='nearest')
ax.set_xticks([])
ax.set_yticks([])
ax.set_xlabel('average')
plt.subplots_adjust(bottom=0.2)

class Caller:

    def __init__(self, im):
        self.im = im
        self.face_list = []

    def face(self, event):
        self.face_list.append(self.im)
        self.im = signal.convolve(np.random.random((image_size, image_size)), kernel)
        l.set_data(self.im)
        m.set_data(np.mean(np.array(self.face_list), axis=0))
        plt.draw()

    def no_face(self, event):
        self.im = signal.convolve(np.random.random((image_size, image_size)), kernel)
        l.set_data(self.im)
        plt.draw()

callback = Caller(im)
axprev = plt.axes([0.7, 0.05, 0.1, 0.075])
axnext = plt.axes([0.81, 0.05, 0.1, 0.075])
bnext = Button(axnext, 'Face')
bnext.on_clicked(callback.face)
bprev = Button(axprev, 'No Face')
bprev.on_clicked(callback.no_face)

plt.show()



