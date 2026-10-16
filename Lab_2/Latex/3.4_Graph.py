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