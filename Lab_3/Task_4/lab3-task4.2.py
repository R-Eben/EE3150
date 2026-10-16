
from scipy.io import wavfile
import numpy as np
import matplotlib.pyplot as plt

#read sampling frequency and data from audio clip
fs, clip = wavfile.read("clip.wav")
clip = clip.astype(float); 
if clip.ndim > 1: 
    clip = clip[:,0]
clip = clip/np.max(np.abs(clip))

#RC time constant
tau = 0.00155

dt = 1.0/fs
a = tau/(tau+dt)
b = dt/(tau+dt)

y = np.zeros_like(clip)

#numeric step result convolution via DE approximation
for n in range(len(clip)): # y[n] is the current sample of the live stream
    y[n] = a*y[n-1] + b*clip[n]

#write output to files for comparison
from scipy.io import wavfile
y_i16 = np.int16(y / np.max(np.abs(y)) * 32767) # converts to 16 bit int for wav format
fname = "clip_RC_filter.wav"
wavfile.write(fname, round(fs), y_i16) # writes the wav file to disk


fig, ax = plt.subplots()
n = np.arange(len(y))

ax.plot(n, y)

ax.set_title("Clip filtered through RC response")

ax.grid(True, alpha=0.3)
ax.set_xlabel("Sample (n)")
ax.set_ylabel("Output")


plt.tight_layout()
plt.show()