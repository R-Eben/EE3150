import numpy as np
import matplotlib.pyplot as plt

tau = 0.01
dt = 0.0001
t = np.arange(0.0, 0.08, dt)

#impulse response 
h = (1/tau) * np.exp(-t/tau)

#unit step input
x = np.ones(len(t))

#output convolution of impulse respones and unit step
y = np.convolve(x, h) * dt

# use seconds for the output time axis
t_axis = np.arange(len(y)) * dt

#analytic step response
y_analytic = 1 - np.exp(-t/tau)

#plot and compare analytic and numerical convolution results
fig1, ax1 = plt.subplots(figsize=(8, 5))
ax1.plot(t, y_analytic, label="hand-calculated analytic step response")
ax1.plot(t_axis, y, "--", label="numeric step response")
ax1.set_xlim(0, 0.08)
ax1.set_ylim(0, 1.1)
ax1.set_title("First-stage RC step response")
ax1.set_xlabel("time (s)")
ax1.set_ylabel("output amplitude")
ax1.legend()
ax1.grid(True)
fig1.tight_layout()
plt.show()
