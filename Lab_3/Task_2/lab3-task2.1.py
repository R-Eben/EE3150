import numpy as np
import matplotlib.pyplot as plt

tau = 0.01
dt = 0.0001
t = np.arange(0.0, 0.08, dt)

h = (1/tau) * np.exp(-t/tau)
x = np.ones(len(t))
y = np.convolve(x, h) * dt

# use seconds for the output time axis
t_axis = np.arange(len(y)) * dt
y_expected = 1 - np.exp(-t/tau)

fig1, ax1 = plt.subplots(figsize=(8, 5))
ax1.plot(t_axis, y, label="numerical convolution")
ax1.plot(t, y_expected, "--", label="expected response")

# show the response while the sampled step is on
ax1.set_xlim(0, 0.08)
ax1.set_ylim(0, 1.1)
ax1.set_title("First-stage RC step response")
ax1.set_xlabel("time (s)")
ax1.set_ylabel("output amplitude")
ax1.legend()
ax1.grid(True)
fig1.tight_layout()
plt.show()
