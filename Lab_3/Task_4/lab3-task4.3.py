
from scipy.io import wavfile
import numpy as np
import matplotlib.pyplot as plt

fs, clip = wavfile.read("clip.wav")
clip = clip.astype(float); 
if clip.ndim > 1: 
    clip = clip[:,0]
clip = clip/np.max(np.abs(clip))

tau = 0.00155

dt = 1.0/fs
a = tau/(tau+dt)
b = dt/(tau+dt)


freq = [50, 100, 200, 500, 1000, 2000, 4000, 8000]

n = np.arange(0, 1.0, dt)

#create list of one second pure tones at each test frequency
tones = []
for f in freq:
    tones.append(np.cos(2*np.pi*f*n))


y = np.zeros_like(clip)

fig, ax = plt.subplots()
n = np.arange(len(y))


from scipy.io import wavfile
y_i16 = np.int16(y / np.max(np.abs(y)) * 32767) # converts to 16 bit int for wav format
fname = "clip_RC_filter.wav"
wavfile.write(fname, round(fs), y_i16) # writes the wav file to disk

ax.plot(n, y)


ax.set_title("Clip filtered through RC response")

ax.grid(True, alpha=0.3)
ax.set_xlabel("Sample (n)")
ax.set_ylabel("Output")


plt.tight_layout()
plt.show()