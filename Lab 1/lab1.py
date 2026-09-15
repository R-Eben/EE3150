import numpy as np
import matplotlib.pyplot as plt

t = np.arange(0.0, 6.0, 1.0 / 2000)
# 0 to 6 s, step 0.5 ms
x1 = np.exp(-t)
#real exponential
x2 = np.exp((-1 + 1j * 2) * t) #complex exponential
x3 = np.zeros_like(t) #square
x4 = np.zeros_like(t) #triangular

T = 2
# generate square and triangular waves below
for i in range(len(t)):
    rem = t[i] % T
    
    if rem < T/2:
        x3[i] = 1.0
        x4[i] = 1-2 * rem

    else:
        x3[i] =-1.0
        x4[i] = 2 * rem - 3

# plot
plt.figure(figsize=(9, 8))
plt.subplot(2, 2, 1)
plt.plot(t, x1, label="exp(-t)")
plt.xlabel("t (s)"); plt.ylabel("x1")
plt.grid(True, alpha=0.4)
plt.legend()
plt.subplot(2, 2, 2)
plt.plot(t, np.imag(x2), label="imag of exp((-1+2j)t)")
plt.xlabel("t (s)"); plt.ylabel("x2")
plt.grid(True, alpha=0.4)
plt.legend()
plt.subplot(2, 2, 3)
plt.plot(t, x3, label="square")
plt.xlabel("t (s)"); plt.ylabel("x3")
plt.legend()
plt.subplot(2, 2, 4)
plt.grid(True, alpha=0.4)
plt.plot(t, x4, label="triangle")
plt.xlabel("t (s)"); plt.ylabel("x4")
plt.legend()
plt.grid(True, alpha=0.4)

plt.savefig("signals.png", dpi=150)