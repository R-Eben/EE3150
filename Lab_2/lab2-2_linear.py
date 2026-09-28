import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp

R1, C1 = 10e3, 1e-6; tau1 = R1*C1
R2, C2 = 4.7e3, 1e-6; tau2 = R2*C2
R4, R5 = 1e3, 4.7e3; G = 1 + R5/R4
tau_min, tau_max = min(tau1, tau2), max(tau1, tau2)

def h(t):
    t = np.asarray(t, float)
    y = G/(tau1-tau2)*(np.exp(-t/tau1) - np.exp(-t/tau2))
    y[t <= 0] = 0.0
    return y

def f_rhs(t, x, T, A): # needed for solve_ivp
    v1, v2 = x
    if (0.0 <= t < T):
        _vin = A
    else:
        _vin = 0.0
    return [(_vin - v1)/tau1, (G*v1 - v2)/tau2]

def simulate(T,A, lw=1.5, ls='-'):
    t_end = T + 8*tau_max
    t_eval = np.linspace(0.0, t_end, 4000)
    max_step = min(T, tau_min)/20.0
    sol = solve_ivp(f_rhs, (0.0, t_end), [0.0, 0.0], t_eval=t_eval,
                    rtol=1e-8, atol=1e-8, max_step=max_step, args=(T,A,))
    vin = np.zeros(len(t_eval))
    vin[(t_eval >= 0) & (t_eval <= T)] = A
    v2 = sol.y[1]
    label = f"T = {T*1e3:g} ms, A = {A} V"
    axn.plot(t_eval*1e3, v2/(A*T), lw=lw, ls=ls, label=label)

fig2, axn = plt.subplots(figsize=(8, 4.2))

t_ref = np.linspace(0.0, 60e-3, 4000)

simulate(100e-3, 1, lw=4, ls = "-")
simulate(100e-3, 5, lw = 1.5, ls = '--')

axn.set(title="Linearity Check (Does output scale perfectly with input?)", xlabel="t (ms)", ylabel="h(t) (1/s)", xlim=(0, 150))
axn.grid(True, alpha=.4); axn.legend(fontsize=8)
plt.show()