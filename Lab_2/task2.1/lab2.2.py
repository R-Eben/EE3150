import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp

R1, C1 = 10e3, 1e-6; tau1 = R1*C1
R2, C2 = 4.7e3, 1e-6; tau2 = R2*C2
R4, R5 = 1e3, 4.7e3; G = 1 + R5/R4
tau_min, tau_max = min(tau1, tau2), max(tau1, tau2)

def h(t): 
    t = np.asarray(t, float)
    y = np.zeros_like(t)
    y = G/(tau1-tau2)*(np.exp(-t/tau1) - np.exp(-t/tau2))
    y[t<=0] = 0.0
    return y

def simulate_circuit(pulse_height, pulse_width):
    # This function simulates feeding a rectangular pulse into your circuit
    end_time = pulse_width + (8 * max(tau1, tau2))
    time_points = np.linspace(0.0, end_time, 4000)
    
    def circuit_equations(t, voltages):
        v1, v2 = voltages
        
        # If time is within the pulse width, input is pulse_height. Otherwise, it's 0.
        if 0 <= t <= pulse_width:
            current_input = pulse_height 
        else:
            current_input = 0.0
        
        #  equations for the two RC stages
        dv1_dt = (current_input - v1) / tau1
        dv2_dt = ((G * v1) - v2) / tau2
        return [dv1_dt, dv2_dt]

    # e math solver
    solution = solve_ivp(circuit_equations, (0.0, end_time), [0.0, 0.0], t_eval=time_points)
    
    # Return the time array and the output voltage array (v2)
    return time_points, solution.y[1] 


#shrinking pulses
plt.figure(figsize=(8, 5))

# Plot the perfect theoretical math line (Black line)
t_plot = np.linspace(0, 0.08, 4000)
plt.plot(t_plot * 1000, h(t_plot), "k", lw=2, label="Perfect Math h(t)")

# Test different pulse widths (from 0.1 ms to 50 ms)
pulse_widths = [0.0001, 0.001, 0.01, 0.05] 
height = 1.0

for width in pulse_widths:
    t_eval, output_voltage = simulate_circuit(height, width)
    
    #divide by (height * width) to normalize the area so we can compare them fairly
    pulse_area = height * width
    normalized_voltage = output_voltage / pulse_area
    
    plt.plot(t_eval * 1000, normalized_voltage, "--", label=f"Width = {width*1000} ms")

plt.title("Do shorter pulses act like perfect impulses?")
plt.xlabel("Time (ms)")
plt.ylabel("Voltage (V)")
plt.xlim(0, 60)
plt.legend()
plt.grid(True, alpha=0.4)
plt.show()


#lienarity
plt.figure(figsize=(8, 5))

# Simulate a 1V pulse and a 5V pulse (both 100ms long)
t1, out1 = simulate_circuit(pulse_height=1.0, pulse_width=0.1)
t5, out5 = simulate_circuit(pulse_height=5.0, pulse_width=0.1)

# Plot both (normalized by their area)
plt.plot(t1 * 1000, out1 / (1.0 * 0.1), lw=4, alpha=0.5, label="1V Pulse")
plt.plot(t5 * 1000, out5 / (5.0 * 0.1), "--", color="red", label="5V Pulse")

plt.title("Linearity Check (Does output scale perfectly with input?)")
plt.xlabel("Time (ms)")
plt.ylabel("Voltage (V)")
plt.xlim(0, 150)
plt.legend()
plt.grid(True, alpha=0.4)
plt.show()