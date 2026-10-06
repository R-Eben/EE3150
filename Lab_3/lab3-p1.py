import numpy as np
import matplotlib.pyplot as plt

x = np.array([1, 2, 3, 1])
h = np.array([1, -1, 2])


# This code for convolution only works if x and h both start at time n=0
def conv_loop(x, h):

    Ny = len(x) + len(h)- 1
    y = np.zeros(Ny)
    for n in range(Ny): # this loop computes y[n] for different n's
        for k in range(len(x)): # this loop implements the convolution sum
            m = n - k
            if 0 <= m < len(h):
                y[n] = y[n] + x[k]*h[m]
    return y


y1 = conv_loop(x, h)
y2 = np.convolve(x,h)
n1 = np.arange(len(y1))
n2 = np.arange(len(y2))

fig1, ax1 = plt.subplots(figsize=(8, 6))
fig2, ax2 = plt.subplots(figsize=(8, 6))

ax1.stem(n1, y1, label="y1[n] = x[n] * h[n]")

ax1.set_title("Convolution output")
ax1.set_xlabel("n")
ax1.legend()
ax1.grid(True)
fig1.tight_layout()

ax2.stem(n2, y2, label="y2[n] = x[n] * h[n]")
ax2.set_title("NP.convolve")
ax2.set_xlabel("n")
ax2.legend()
ax2.grid(True)
fig2.tight_layout()
plt.show()