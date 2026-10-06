from scipy.io import wavfile
import numpy as np

fs, clip = wavfile.read("clip.wav")
clip = clip.astype(float); 
if clip.ndim > 1: 
    clip = clip[:,0]
clip = clip/np.max(np.abs(clip))

h_ma = np.ones(64)/64

h_diff = np.array([1.0, -1.0])

#D = 8192 * 0.2
D = int(round(0.2 * fs))
h_echo = np.zeros(D+1)
h_echo[0] = 1.0
h_echo[D] = 0.6

y_ma = np.convolve(clip,h_ma)
y_ma = y_ma / np.max(np.abs(y_ma)) # normalize to [-1, 1]

y_diff = np.convolve(clip,h_diff)
y_diff = y_diff / np.max(np.abs(y_diff)) # normalize to [-1, 1]

y_echo = np.convolve(clip,h_echo)
y_echo = y_echo / np.max(np.abs(y_echo)) # normalize to [-1, 1]

y1 = np.convolve(np.convolve(clip, h_ma), h_echo) # average, then echo
y2 = np.convolve(np.convolve(clip, h_echo), h_ma) # echo, then average
y3 = np.convolve(clip, np.convolve(h_ma, h_echo)) # one combined filter

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

y1_i16 = np.int16(y1 / np.max(np.abs(y1)) * 32767) # converts to 16 bit int for wav format
fname = "y1.wav"
wavfile.write(fname, round(fs), y1_i16) # writes the wav file to disk

y2_i16 = np.int16(y2 / np.max(np.abs(y2)) * 32767) # converts to 16 bit int for wav format
fname = "y2.wav"
wavfile.write(fname, round(fs), y2_i16) # writes the wav file to disk

y3_i16 = np.int16(y3 / np.max(np.abs(y3)) * 32767) # converts to 16 bit int for wav format
fname = "y3.wav"
wavfile.write(fname, round(fs), y3_i16) # writes the wav file to disk