import numpy as np
import matplotlib.pyplot as plt

tau1, tau2, G = 10e-3, 4.7e-3, 5.7

t = np.linspace(0, 60e-3, 2000)
h = G / (tau1 - tau2) * (np.exp(-t / tau1) - np.exp(-t / tau2))

plt.figure(figsize=(8, 4.2))
plt.plot(t * 1e3, h, "k", lw=2)
plt.xlabel("t (ms)")
plt.ylabel("h(t)")
plt.title("Analytic impulse response h(t)")
plt.grid(True, alpha=0.4)
plt.tight_layout()
plt.savefig("h_analytic.png", dpi=300)
plt.show()