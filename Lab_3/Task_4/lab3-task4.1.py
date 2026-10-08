
import numpy as np
import matplotlib.pyplot as plt

tau = 0.01

fs = 16000

dt = 1.0/fs
a = tau/(tau+dt)
b = dt/(tau+dt)

x = np.ones(fs)
y = np.zeros_like(x)


for n in range(len(x)): # y[n] is the current sample of the live stream
    y[n] = a*y[n-1] + b*x[n]


fig, ax = plt.subplots()
n = np.arange(len(y))
s_analytic = 1 - np.exp(-n*dt/tau)

ax.plot(n, y, label="numeric")
ax.plot(n, s_analytic, "--", label="analytic")
ax.legend()

ax.set_title("Analytic vs. Numeric RC Step Response")

ax.grid(True, alpha=0.3)
ax.set_xlabel("Sample (n)")
ax.set_ylabel("Output")


plt.tight_layout()
fig.savefig("task4.1_step_response.png", dpi=200)
plt.show()