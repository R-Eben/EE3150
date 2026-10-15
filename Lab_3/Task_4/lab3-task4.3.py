
from scipy.io import wavfile
import numpy as np
import matplotlib.pyplot as plt

fs = 16000

tau = 0.00155

dt = 1.0/fs
a = tau/(tau+dt)
b = dt/(tau+dt)


freq = [50, 100, 200, 500, 1000, 2000, 4000, 8000]

n = np.arange(0, 1.0, dt)

h_ma = np.ones(64)/64 #length-64 moving average filter      


#create list of one second pure tones at each test frequency
tones = []
for f in freq:
    tones.append(np.cos(2*np.pi*f*n))

y_iir = []
for t in tones:
    out = np.zeros(len(t))
    for k in range(len(t)):  # k is the current sample of the live stream
        if k == 0:
            out[k] = b*t[k]
        else:
            out[k] = a*out[k-1] + b*t[k]
    y_iir.append(out)

y_fir = []
for t in tones:
    y_fir.append(np.convolve(t, h_ma))

#y_analytic
f_dense = np.logspace(np.log10(freq[0]), np.log10(freq[-1]), 500)
H_analytic = 1/np.sqrt(1 + (2*np.pi*f_dense*tau)**2)

#measure steady state amplitude of output at each frequency
steady_state_amp_iir = []
for out in y_iir:
    steady_state_amp_iir.append(np.max(np.abs(out[len(out)//2:])))

steady_state_amp_fir = []
for out in y_fir:
    steady_state_amp_fir.append(np.max(np.abs(out[len(out)//2:])))

# code for plotting freq vs amplitude
fig, ax = plt.subplots()

ax.plot(freq, steady_state_amp_iir, 'o-', label='IIR Output Steady-State Amplitude (RC circuit)')
ax.plot(freq, steady_state_amp_fir, 'o-', label='FIR Output Steady-State Amplitude (Moving average)')
ax.plot(f_dense, H_analytic, label='Analytic Steady-State Amplitude (RC circuit)')
ax.legend()

ax.set_title("Amplitude vs Frequency for different filter outputs")

ax.grid(True, alpha=0.3)
ax.set_xlabel("Frequency (Hz)")
ax.set_ylabel("Amplitude")
ax.set_xscale('log')


plt.tight_layout()
fig.savefig("task4.3_amplitude_vs_freq.png", dpi=200)
plt.show()
