from scipy.io import wavfile
import numpy as np
import matplotlib.pyplot as plt
from scipy.io import wavfile

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

y1_i16 = np.int16(y1 / np.max(np.abs(y1)) * 32767) # converts to 16 bit int for wav format
fname = "y1.wav"
wavfile.write(fname, round(fs), y1_i16) # writes the wav file to disk

y2_i16 = np.int16(y2 / np.max(np.abs(y2)) * 32767) # converts to 16 bit int for wav format
fname = "y2.wav"
wavfile.write(fname, round(fs), y2_i16) # writes the wav file to disk

y3_i16 = np.int16(y3 / np.max(np.abs(y3)) * 32767) # converts to 16 bit int for wav format
fname = "y3.wav"
wavfile.write(fname, round(fs), y3_i16) # writes the wav file to disk



# code for plotting highpass, low pass, and echo, if interested
# def t_axis(x):
#     return np.arange(len(x)) / fs  # seconds

# fig, axes = plt.subplots(4, 1, figsize=(10, 9), sharex=True)

# axes[0].plot(t_axis(clip), clip, linewidth=0.5)
# axes[0].set_title("Original clip")

# axes[1].plot(t_axis(y_ma), y_ma, linewidth=0.5, color="tab:green")
# axes[1].set_title("Low pass (64-pt moving average)")

# axes[2].plot(t_axis(y_diff), y_diff, linewidth=0.5, color="tab:red")
# axes[2].set_title("High pass (first difference)")

# axes[3].plot(t_axis(y_echo), y_echo, linewidth=0.5, color="tab:purple")
# axes[3].set_title(f"Echo (D = {D} samples, {D/fs:.2f} s, gain 0.6)")

# for ax in axes:
#     ax.set_ylabel("Amplitude")
#     ax.set_ylim(-1.05, 1.05)
#     ax.grid(True, alpha=0.3)
# axes[-1].set_xlabel("Time (s)")
# axes[-1].set_xlim(1, 2)  # e.g., a 50 ms window

# plt.tight_layout()
# plt.show()