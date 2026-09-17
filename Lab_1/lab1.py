import numpy as np
import matplotlib.pyplot as plt

t = np.arange(0.0, 6.0, 1.0 / 2000)
# 0 to 6 s, step 0.5 ms
x1 = np.exp(-t)
#real exponential
x2 = np.exp((-1 + 1j * 2) * t) #complex exponential
x3 = np.zeros_like(t) #square
x4 = np.zeros_like(t) #triangular




T = 2
# generate square and triangular waves below
for i in range(len(t)):
    # rem tells us where we are in the current period
    rem = t[i] % T
    
    if rem < T/2:
        x3[i] = 1.0
        x4[i] = -1 + 4/T * rem

    else:
        x3[i] =-1.0
        x4[i] = 3 - 4/T * rem

# plot
plt.figure(figsize=(9, 8))
plt.subplot(2, 2, 1)
plt.plot(t, x1, label="exp(-t)")
plt.xlabel("t (s)"); plt.ylabel("x1")
plt.grid(True, alpha=0.4)
plt.legend()
plt.subplot(2, 2, 2)
plt.plot(t, np.imag(x2), label="imag of exp((-1+2j)t)")
plt.xlabel("t (s)"); plt.ylabel("x2")
plt.grid(True, alpha=0.4)
plt.legend()
plt.subplot(2, 2, 3)
plt.plot(t, x3, label="square")
plt.xlabel("t (s)"); plt.ylabel("x3")
plt.legend()
plt.subplot(2, 2, 4)
plt.grid(True, alpha=0.4)
plt.plot(t, x4, label="triangle")
plt.xlabel("t (s)"); plt.ylabel("x4")
plt.legend()
plt.grid(True, alpha=0.4)

plt.savefig("signals.png", dpi=150)
# saves the 2x2 fig as a png



n = np.arange(0, 6)
# index vector 0 to 5
x = np.array([1.0, 2.0, 3.0, 4.0, 5.0, 6.0])
# the ramp signal values

ny1 = n - 2
# shifted index for shift transform
y1 = x + 1
# just adds 1 to every value

ny2 = -n[::-1]
# flips and negates the index
y2 = x[::-1]
# flips the values to match

y3 = x[::2]
# keeps every other sample
ny3 = np.arange(len(y3))
# new shorter index for the compressed signal

# y4[n] = 2*x[-2n+1] - 1
x_sub = x[1::2]        # x[1], x[3], x[5] = [2, 4, 6]
y4 = 2 * x_sub[::-1] - 1   # reverse to get decreasing index-> increasing n order
ny4 = np.arange(-(len(y4) - 1), 1)  # [-2, -1, 0]


fig, ax = plt.subplots(2, 3, figsize=(15, 6), sharey=True, sharex=True)
# makes a 2x3 grid of plots
ax = ax.ravel()
# flattens the grid so we can index it 0 to 5
ax[0].stem(n, x); ax[0].set_title(r"$x[n]$")
ax[1].stem(ny1, y1); ax[1].set_title(r"$x[n+2]+1$")
ax[2].stem(ny2, y2); ax[2].set_title(r"$x[-n]$")
ax[3].stem(ny3, y3); ax[3].set_title(r"$x[2n]$")
ax[4].stem(ny4, y4); ax[4].set_title(r"$2x[-2n+1]-1$")

fig.tight_layout()
fig.savefig("part2_transforms.png", dpi=150)
# saves the stem plots as a png






f = 1406 # your birthday frequency

c = 2.00 #sampling rate multiplier, current set to nyquist rate
delta = 10

tau = 0.5

fs = round(8192) # sampling rate (Hz)
T = 4.0 # duration (s)
N = int(fs * T) # total number of samples
n = np.arange(N) # sample index vector
t = n / fs # converts sample index to actual time
x = np.sin(2 * np.pi * f * t) # the sampled sinusoid

y =  np.exp(-t/tau)*x # sampled sinusoid multiplied by decaying envelope



# plot x
x = x / np.max(np.abs(x)) # normalize to [-1, 1]
mask = t <= 1 # only keep first 1 s for the plot
plt.figure(figsize=(8, 3.5))
plt.plot(t[mask] * 1e3, x[mask])
plt.xlabel("t (ms)"); plt.ylabel("x(t)")
plt.grid(True); plt.tight_layout()
plt.savefig("part3_tone.png", dpi=150)
# saves the tone plot as a png

# plot y
y = y / np.max(np.abs(y)) # normalize to [-1, 1]
mask = t <= 1 # only keep first 1 s for the plot
plt.figure(figsize=(8, 3.5))
plt.plot(t[mask] * 1e3, y[mask])
plt.xlabel("t (ms)"); plt.ylabel("y(t)")
plt.grid(True); plt.tight_layout()
plt.savefig("part3_tone_decay.png", dpi=150)
# saves the tone plot as a png

try:
    import sounddevice as sd
    sd.play(y, round(fs)); sd.wait()
    # plays the tone out loud and waits till done
except Exception:
    print("Couldn't play audio")

from scipy.io import wavfile
x_i16 = np.int16(x / np.max(np.abs(x)) * 32767)
# converts to 16 bit int for wav format
fname = "birthday_tone.wav"
wavfile.write(fname, round(fs), x_i16)
# writes the wav file to disk