import numpy as np
import matplotlib.pyplot as plt

t = np.arange(0.0, 20.0, 1.0 / 2000) # 0 to 20 s, step 0.5 ms
sigma_vals = [-2, -2, -1, -1, 0, 0, 1, 1, 2, 2]            
omega_vals = [ 0,  1,  1, 2,  2, 3, 3, 4, 4, 5]

x = [np.exp((s + 1j * o) * t) for s, o, in zip(sigma_vals, omega_vals)]  

fig1, axes1 = plt.subplots(2, 5, figsize=(12, 10), sharex=True)
for ax, s, o, x in zip(axes1.ravel(), sigma_vals, omega_vals, x):
    ax.plot(t, np.imag(x), label=fr" imag of $e^{{({s:g} + j({o:g}))t}}$")
    ax.set_xlabel("t (s)")
    ax.set_ylabel("imag of x(t)")
    ax.grid(True, alpha=0.4)
    ax.legend()

fig1.tight_layout()
fig1.savefig("complex_exponential.png", dpi=150)
