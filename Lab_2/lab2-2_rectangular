import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp

R1, C1 = 10e3, 1e-6; tau1 = R1*C1
R2, C2 = 4.7e3, 1e-6; tau2 = R2*C2
R4, R5 = 1e3, 4.7e3; G = 1 + R5/R4
tau_min, tau_max = min(tau1, tau2), max(tau1, tau2)
A = 1.0

def h(t):
    t = np.asarray(t, float)
    y = G/(tau1-tau2)*(np.exp(-t/tau1) - np.exp(-t/tau2))
    y[t <= 0] = 0.0
    return y

def f_rhs(t, x, T):
    v1, v2 = x
    _vin = A if 0.0 <= t < T else 0.0
    return [(_vin - v1)/tau1, (G*v1 - v2)/tau2]

def simulate(T):
    t_end = T + 8*tau_max
    t_eval = np.linspace(0.0, t_end, 4000)
    max_step = min(T, tau_min)/20.0
    sol = solve_ivp(f_rhs, (0.0, t_end), [0.0, 0.0], t_eval=t_eval,
                    rtol=1e-8, atol=1e-8, max_step=max_step, args=(T,))
    vin = np.zeros(len(t_eval))
    vin[(t_eval >= 0) & (t_eval <= T)] = A
    return t_eval, vin, sol.y[1]

fig1, ax = plt.subplots(2, 1, figsize=(8, 6))
fig2, axn = plt.subplots(figsize=(8, 4.2))

t_ref = np.linspace(0.0, 60e-3, 4000)
axn.plot(t_ref*1e3, h(t_ref), "k", lw=2, label="h(t) analytic")

for T in [100e-6, 1e-3, 10e-3, 50e-3]:
    t, vin, v2 = simulate(T)
    label = f"T = {T*1e3:g} ms"
    ax[0].plot(t*1e3, vin, label=label)
    ax[1].plot(t*1e3, v2, label=label)
    axn.plot(t*1e3, v2/(A*T), "--", label=label)

ax[0].set(title="Rectangular inputs v_in(t)", ylabel="V", xlim=(0, 80))
ax[1].set(title="Outputs v_c2(t)", xlabel="t (ms)", ylabel="V", xlim=(0, 80))
axn.set(title="Do shorter pulses act like perfect impulses?", xlabel="t (ms)", ylabel="h(t) (1/s)", xlim=(0, 60))
axn.grid(True, alpha=.4); axn.legend(fontsize=8)
ax[0].legend(fontsize=8); ax[1].legend(fontsize=8)
plt.show()