from scipy.io import wavfile
import numpy as np
import matplotlib.pyplot as plt

fs = 16000
freq = [50, 100, 200, 500, 1000, 2000, 4000, 8000]

t = np.arange(0, 1.0, 1.0/fs)



#create list of one second pure tones at each test frequency
tones = []
for f in freq:
    tones.append(np.cos(2*np.pi*f*t))


h_ma = np.ones(64)/64 #length-64 moving average filter      

#convolve each tone with length-64 moving average filter
y = []
for t in tones:
    y.append(np.convolve(t, h_ma))

#measure steady state amplitude of output at each frequency
steady_state_amp = []
for out in y:
    steady_state_amp.append(np.max(np.abs(out[len(out)//2:])))

amp_low_freq = steady_state_amp[0]



# code for plotting freq vs amplitude
fig, ax = plt.subplots()

ax.plot(freq, steady_state_amp)

ax.set_title("Amplitude vs Frequency (64-pt moving average filter output)")

ax.grid(True, alpha=0.3)
ax.set_xlabel("Time (s)")
ax.set_ylabel("Amplitude")
ax.set_xscale('log')

ax.axhline(y=amp_low_freq, color="tab:red", linestyle="--", linewidth=1, label="Low frequncy amplitude")
ax.axhline(y=amp_low_freq/2, color="tab:green", linestyle="--", linewidth=1, label="Half of low frequency amplitude")
ax.legend() 


plt.tight_layout()
fig.savefig("task3.3_amplitude_vs_freq.png", dpi=200)
plt.show()
