from scipy.io import wavfile
import numpy as np
import matplotlib.pyplot as plt

#read sampling frequency and data from audio clip
fs, clip = wavfile.read("clip.wav")
clip = clip.astype(float); 
if clip.ndim > 1: 
    clip = clip[:,0]
clip = clip/np.max(np.abs(clip))

#Moving average filter
h_ma = np.ones(64)/64

#Difference filter
h_diff = np.array([1.0, -1.0])


#Echo filter
D = int(round(0.2 * fs))
h_echo = np.zeros(D+1)
h_echo[0] = 1.0
h_echo[D] = 0.6

#Moving average filter output
y_ma = np.convolve(clip,h_ma)
y_ma = y_ma / np.max(np.abs(y_ma)) # normalize to [-1, 1]

#Difference filter output
y_diff = np.convolve(clip,h_diff)
y_diff = y_diff / np.max(np.abs(y_diff)) # normalize to [-1, 1]

#Echo filter output
y_echo = np.convolve(clip,h_echo)
y_echo = y_echo / np.max(np.abs(y_echo)) # normalize to [-1, 1]


#write outputs to files for comparison
from scipy.io import wavfile
y_ma_i16 = np.int16(y_ma / np.max(np.abs(y_ma)) * 32767) # converts to 16 bit int for wav format
fname = "low_pass.wav"
wavfile.write(fname, round(fs), y_ma_i16) # writes the wav file to disk

y_diff_i16 = np.int16(y_diff / np.max(np.abs(y_diff)) * 32767) # converts to 16 bit int for wav format
fname = "high_pass.wav"
wavfile.write(fname, round(fs), y_diff_i16) # writes the wav file to disk

y_echo_i16 = np.int16(y_echo / np.max(np.abs(y_echo)) * 32767) # converts to 16 bit int for wav format
fname = "echo.wav"
wavfile.write(fname, round(fs), y_echo_i16) # writes the wav file to disk
