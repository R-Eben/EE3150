import numpy as np, pandas as pd, matplotlib.pyplot as plt

tau1, tau2, G = 10e-3, 4.7e-3, 5.7
t = np.linspace(0, 0.06, 600)
h = G/(tau1-tau2) * (np.exp(-t/tau1) - np.exp(-t/tau2))
plt.plot(t*1e3, h, "k", lw=2, label="h(t) analytic")

# (file, amplitude, width)
runs = [("3_2_p1_slow.csv", 5, 100e-6), ("3_2_1ms_slow.csv", 5, 1e-3),
        ("3_2_10ms_slow.csv", 2, 10e-3), ("3_2_50ms_slow.csv", 2, 50e-3)]

for f, A, T in runs:
    df = pd.read_csv(f, skiprows=7, encoding="utf-8-sig")   # data starts after the header
    time, vin, vout = df.iloc[:, 1], df.iloc[:, 2], df.iloc[:, 3]
    t0 = time[vin > A/2].iloc[0]                            # rising edge of pulse
    m = (time >= t0) & (time <= t0 + 0.06)
    plt.plot((time[m] - t0)*1e3, vout[m]/(A*T), label=f)

plt.xlabel("t (ms)"); plt.ylabel("v_c2/(A·T)"); plt.legend(); plt.grid(alpha=.3)
plt.savefig("3.2_normalized.png", dpi=200)