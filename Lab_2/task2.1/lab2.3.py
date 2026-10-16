import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp

R1, C1 = 10e3, 1e-6; tau1 = R1*C1
R2, C2 = 4.7e3, 1e-6; tau2 = R2*C2
R4, R5 = 1e3, 4.7e3; G = 1 + R5/R4
tau_min, tau_max = min(tau1, tau2), max(tau1, tau2)

# A and T for triangular
A = 2.0
T = 100e-6
t_end = T + 8*tau_max
t_eval = np.linspace(0.0, t_end, 4000)
max_step = min(T, tau_min)/20.0

# vin array for plotting the triangle
vin = np.zeros(len(t_eval))
for i, t in enumerate(t_eval):
    if 0 <= t <= T/2:
        vin[i] = (2 * A / T) * t
    elif T/2 < t <= T:
        vin[i] = (2 * A / T) * (T - t)

def h(t): 
    t = np.asarray(t, float)
    y = np.zeros_like(t)
    y = G/(tau1-tau2)*(np.exp(-t/tau1) - np.exp(-t/tau2))
    y[t<=0] = 0.0
    return y

#f_rhs to feed a triangle into the solver ---
def f_rhs(t, x): 
    v1, v2 = x
    if 0 <= t <= T/2:
        _vin = (2 * A / T) * t
    elif T/2 < t <= T:
        _vin = (2 * A / T) * (T - t)
    else:
        _vin = 0.0
    return [(_vin - v1)/tau1, (G*v1 - v2)/tau2]

sol = solve_ivp(f_rhs, (0.0, t_end), [0.0, 0.0], t_eval=t_eval, rtol=1e-8, atol=1e-8, max_step=max_step)
v2 = sol.y[1] 

# Plotting code normalizes by triangle area (0.5 * A * T)
area = 0.5 * A * T

fig1, ax = plt.subplots(2, 1, figsize=(8, 6))
fig2, axn = plt.subplots(figsize=(8, 4.2))

axn.plot(t_eval * 1e3, h(t_eval), "k", lw=2, label="h(t) analytic")

ax[0].plot(t_eval * 1e3, vin)
ax[1].plot(t_eval * 1e3, v2)

# normalized against the area
axn.plot(t_eval * 1e3, v2 / area, "--", color="orange", label="Normalized Triangle")

ax[0].set(title="Triangular input v_in(t)", ylabel="V")
ax[0].set_xlim(-0.02, 0.2) 
ax[1].set(title="Outputs v_c2(t)", xlabel="t (ms)", ylabel="V"); ax[1].set_xlim(0, 80)

axn.set(title="h(t) and its approximation (Triangle)", xlabel="t (ms)", ylabel="V"); axn.set_xlim(0, 60)
axn.grid(True, alpha=.4); axn.legend(fontsize=10)
plt.tight_layout()
plt.show()