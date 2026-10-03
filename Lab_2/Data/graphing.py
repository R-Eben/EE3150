import glob, os
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

FOLDER = os.path.dirname(os.path.abspath(__file__))   # put this script in the CSV folder
OUT = os.path.join(FOLDER, "graphs")   # separate folder so scope .png files never get overwritten
os.makedirs(OUT, exist_ok=True)

for path in sorted(glob.glob(os.path.join(FOLDER, "*.csv"))):
    name = os.path.splitext(os.path.basename(path))[0]

    # skip the scope header, data starts at the Sample Number line
    with open(path, encoding="utf-8-sig") as f:
        skip = next(i for i, line in enumerate(f) if line.startswith("Sample Number"))
    df = pd.read_csv(path, skiprows=skip, encoding="utf-8-sig").dropna(axis=1, how="all")

    t = df["Time (s)"] * 1e3      # ms
    ch2_label = r"$v_{c1}$" if "vc1" in name else r"$v_{c2}$"

    fig, ax = plt.subplots(2, 1, figsize=(8, 6), sharex=True)

    ax[0].plot(t, df.iloc[:, 2], color="tab:orange", label=r"$v_{in}$ (Ch1)")
    ax[0].set_ylabel("Voltage (V)")
    ax[0].set_title(name)
    ax[0].grid(True, alpha=0.3)
    ax[0].legend(loc="upper right")

    ax[1].plot(t, df.iloc[:, 3], color="tab:green", label=f"{ch2_label} (Ch2)")
    ax[1].set_xlabel("Time (ms)")
    ax[1].set_ylabel("Voltage (V)")
    ax[1].grid(True, alpha=0.3)
    ax[1].legend(loc="upper right")

    fig.tight_layout()
    fig.savefig(os.path.join(OUT, name + ".png"), dpi=200)
    plt.close(fig)
    print("saved", name)


# Task 3.4 frequency response plot
frequency = [5, 15, 30, 60, 120]
vc1 = [0.94, 0.71, 0.47, 0.25, 0.13]
vc2 = [5.37, 3.80, 2.01, 0.71, 0.20]

fig, ax = plt.subplots(figsize=(8, 4.5))

ax.plot(frequency, vc1, marker="o", linewidth=2, label=r"$v_{c1}$")
ax.plot(frequency, vc2, marker="o", linewidth=2, label=r"$v_{c2}$")

ax.set_xlabel("Frequency (Hz)")
ax.set_ylabel("Voltage (Vpp)")
ax.set_title("Measured Magnitude of $v_{c1}$ and $v_{c2}$ vs. Frequency")
ax.grid(True, alpha=0.3)
ax.legend()

fig.tight_layout()
fig.savefig(os.path.join(OUT, "task3_4_frequency_response.png"), dpi=200)
plt.close(fig)