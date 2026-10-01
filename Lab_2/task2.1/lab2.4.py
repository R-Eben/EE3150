import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp

R1, C1 = 10e3, 1e-6; tau1 = R1*C1
R2, C2 = 4.7e3, 1e-6; tau2 = R2*C2
R4, R5 = 1e3, 4.7e3; G = 1 + R5/R4
tau_min, tau_max = min(tau1, tau2), max(tau1, tau2)

A = 1.0
t_end = 8 * tau_max 
t_eval = np.linspace(0.0, t_end, 4000)
max_step = tau_min / 20.0

#step input is constantly A for all t >= 0 
vin = np.ones(len(t_eval)) * A

def h(t): 
    t = np.asarray(t, float)
    y = np.zeros_like(t)
    y = G/(tau1-tau2)*(np.exp(-t/tau1) - np.exp(-t/tau2))
    y[t<=0] = 0.0
    return y

def s(t): 
    t = np.asarray(t, float)
    y = np.zeros_like(t)
    y = G/(tau1-tau2)*(tau1*(1-np.exp(-t/tau1)) - tau2*(1-np.exp(-t/tau2)))
    y[t<=0] = 0.0
    return y

#f_rhs to feed a continuous step into the solver
def f_rhs(t, x): 
    v1, v2 = x
    _vin = A  # The input is always A, no matter the time
    return [(_vin - v1)/tau1, (G*v1 - v2)/tau2]

sol = solve_ivp(f_rhs, (0.0, t_end), [0.0, 0.0], t_eval=t_eval, rtol=1e-8, atol=1e-8, max_step=max_step)
v2_step = sol.y[1] 

#differentiate the step response using np.gradient
ds_dt = np.gradient(v2_step, t_eval)

#plot
fig, ax = plt.subplots(2, 1, figsize=(8, 8))

# Top Plot: Step Response
ax[0].plot(t_eval * 1e3, s(t_eval), "k", lw=4, alpha=0.3, label="s(t) analytic")
ax[0].plot(t_eval * 1e3, v2_step, "--", color="blue", label="Simulated Step Response")
ax[0].set_title("Step Response: Simulated vs Analytic")
ax[0].set_xlabel("t (ms)")
ax[0].set_ylabel("Voltage (V)")
ax[0].grid(True, alpha=0.4)
ax[0].legend()

# Bottom Plot: Impulse Response via Differentiation
ax[1].plot(t_eval * 1e3, h(t_eval), "k", lw=4, alpha=0.3, label="h(t) analytic")
ax[1].plot(t_eval * 1e3, ds_dt, "--", color="red", label="ds(t)/dt (Numerical Derivative)")
ax[1].set_title("Impulse Response: Analytic h(t) vs Differentiated ds(t)/dt")
ax[1].set_xlabel("t (ms)")
ax[1].set_ylabel("Voltage (V)")
ax[1].grid(True, alpha=0.4)
ax[1].legend()

plt.tight_layout()
plt.show()