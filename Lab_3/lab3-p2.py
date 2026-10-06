import numpy as np
import matplotlib.pyplot as plt


tau = 0.01

dt = 0.0001
t = np.arange(0.0, 0.08, dt)

h = 1/tau * np.exp(-t/tau)
x = np.ones(len(t))

y = np.convolve(x,h) * dt

t_axis = np.arange(0, len(x) + len(h) - 1)

fig1, ax1 = plt.subplots(figsize=(8, 6))

ax1.plot(t_axis, y, label="y(t) = x(t) * h(t)")

ax1.set_title("Convolution output")
ax1.set_xlabel("n")
ax1.legend()
ax1.grid(True)
fig1.tight_layout()
plt.show()