import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp

R1, C1 = 10e3, 1e-6; tau1 = R1*C1
R2, C2 = 4.7e3, 1e-6; tau2 = R2*C2
R4, R5 = 1e3, 4.7e3; G = 1 + R5/R4
tau_min, tau_max = min(tau1, tau2), max(tau1, tau2)

A = 1.0
T = 50e-3
t_end = T + 8*tau_max
t_eval = np.linspace(0.0, t_end, 4000)
max_step = min(T, tau_min)/20.0

vin = np.zeros(len(t_eval))
vin[(t_eval >= 0) & (t_eval <= T)] = A

def h(t): # returns impulse response, t>=0
    t = np.asarray(t, float);
    y = np.zeros_like(t);
    y = G/(tau1-tau2)*(np.exp(-t/tau1) - np.exp(-t/tau2))
    y[t<=0] = 0.0
    return y

def s(t): # returns step response, t>=0
    t = np.asarray(t, float);
    y = np.zeros_like(t);
    y = G/(tau1-tau2)*(tau1*(1-np.exp(-t/tau1)) - tau2*(1-np.exp(-t/tau2)))
    y[t<=0] = 0.0
    return y

def f_rhs(t, x): # needed for solve_ivp
    v1, v2 = x
    if (0.0 <= t < T):
        _vin = A
    else:
        _vin = 0.0
    return [(_vin - v1)/tau1, (G*v1 - v2)/tau2]

sol = solve_ivp(f_rhs, (0.0, t_end), [0.0, 0.0], t_eval=t_eval, rtol=1e-8, atol=1e-8, max_step=max_step)

v2 = sol.y[1] # pulse response
v_analytic = A*(s(t_eval) - s(t_eval - T)) # theoretical pulse response adjusted by A


fig1, ax = plt.subplots(2, 1, figsize=(8, 6))
fig2, axn = plt.subplots(figsize=(8, 4.2))
axn.plot(t_eval * 1e3, h(t_eval), "k", lw=2, label="h(t) analytic")

ax[0].plot(t_eval * 1e3, vin)
ax[1].plot(t_eval * 1e3, v2)
axn.plot(t_eval * 1e3, v2 / (A * T), "--")

ax[0].set(title="Rectangular inputs v_in(t)", ylabel="V"); ax[0].set_xlim(0, 80)
ax[1].set(title="Outputs v_c2(t)", xlabel="t (ms)", ylabel="V"); ax[1].set_xlim(0, 80)

axn.set(title="h(t) and its approximation", xlabel="t (ms)", ylabel="V"); axn.set_xlim(0, 60)
axn.grid(True, alpha=.4); axn.legend(fontsize=8)
plt.show()