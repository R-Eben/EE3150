import numpy as np
import matplotlib.pyplot as plt

# experimental values from lab 2
freq = np.array([5, 15, 30, 60, 120])
experimental = np.array([5.37, 3.80, 2.01, 0.71, 0.20])

# circuit values
tau1 = 0.01
tau2 = 0.0047
G = 5.7

# calculate a smooth analytical curve
f = np.linspace(0, 120, 500)
omega = 2 * np.pi * f

analytical = G / (
    np.sqrt(1 + (omega * tau1)**2)
    * np.sqrt(1 + (omega * tau2)**2)
)

# plot the analytical curve and measured points
fig, ax = plt.subplots(figsize=(8, 5))

ax.plot(f, analytical, label="Analytical", color="tab:blue")
ax.scatter(freq, experimental, label="Experimental",
           color="tab:red", zorder=3)

ax.set_title("Two-stage RC magnitude response")
ax.set_xlabel("Frequency (Hz)")
ax.set_ylabel("Magnitude (V/V)")
ax.set_xlim(0, 125)
ax.set_ylim(0, 6)
ax.grid(True, alpha=0.3)
ax.legend()

fig.tight_layout()
fig.savefig("p2_two_stage_mag.png", dpi=200)
plt.show()