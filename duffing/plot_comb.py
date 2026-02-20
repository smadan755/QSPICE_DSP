"""Plot frequency comb from NLTL simulation using PyQSPICE.

Includes comb quality metrics: tooth amplitudes, flatness, SNR, spacing error.
"""
import numpy as np
import matplotlib.pyplot as plt
from PyQSPICE import clsQSPICE as pqs
from pathlib import Path

# Setup PyQSPICE
work_dir = Path(__file__).parent
run = pqs(str(work_dir / "dauffing"))

probes = ["V(x1)", "V(x2)", "V(x3)", "V(x4)", "V(x5)", "V(x6)", "V(x7)", "V(x8)"]
df = run.LoadQRAW(probes)

print(f"Loaded DataFrame: {df.shape}")
time = df['Time'].values
vx8 = df['V(x8)'].values
print(f"Time: {time[0]:.1f} to {time[-1]:.1f} s ({len(time)} points)")

# Use steady-state portion (last 50%)
t_start = time[-1] * 0.5
mask = time >= t_start
t_ss = time[mask]
v_ss = vx8[mask]
T_obs = t_ss[-1] - t_ss[0]
print(f"Steady-state: {t_ss[0]:.0f}s to {t_ss[-1]:.0f}s ({len(t_ss)} pts, T_obs={T_obs:.0f}s)")

# Resample to uniform grid for FFT
N_resample = 65536
t_uniform = np.linspace(t_ss[0], t_ss[-1], N_resample)
v_uniform = np.interp(t_uniform, t_ss, v_ss)
dt = t_uniform[1] - t_uniform[0]
fs = 1.0 / dt
df_bin = fs / N_resample  # frequency resolution
print(f"Resampled: {N_resample} pts, dt={dt:.4f}s, fs={fs:.2f} Hz, df={df_bin:.6f} Hz")

# Window and FFT
window = np.hanning(N_resample)
v_windowed = (v_uniform - np.mean(v_uniform)) * window
fft_vals = np.fft.rfft(v_windowed)
freqs = np.fft.rfftfreq(N_resample, d=dt)
mag_linear = np.abs(fft_vals) / N_resample
magnitude_dB = 20 * np.log10(mag_linear + 1e-15)

# --- Comb tooth detection ---
f_drive = 0.03  # Hz
f_cutoff = 1 / (np.pi * np.sqrt(1))  # ~0.318 Hz for L=1, C=1
f_max = min(f_cutoff * 1.5, freqs[-1])

# Find actual peak near each expected harmonic
tooth_freqs = []
tooth_dBs = []
tooth_snrs = []
search_width = f_drive * 0.3  # search +/- 30% of spacing around expected

for n in range(1, int(f_max / f_drive) + 1):
    f_expected = n * f_drive
    if f_expected > f_max:
        break
    # Find peak within search window
    search_mask = (freqs >= f_expected - search_width) & (freqs <= f_expected + search_width)
    if not np.any(search_mask):
        continue
    idx_in_window = np.where(search_mask)[0]
    peak_idx = idx_in_window[np.argmax(magnitude_dB[idx_in_window])]
    peak_f = freqs[peak_idx]
    peak_dB = magnitude_dB[peak_idx]

    # SNR: peak power vs median noise in surrounding region
    noise_mask = search_mask & (np.abs(freqs - peak_f) > df_bin * 3)
    if np.any(noise_mask):
        noise_floor_dB = np.median(magnitude_dB[noise_mask])
        snr = peak_dB - noise_floor_dB
    else:
        snr = 0.0

    tooth_freqs.append(peak_f)
    tooth_dBs.append(peak_dB)
    tooth_snrs.append(snr)

tooth_freqs = np.array(tooth_freqs)
tooth_dBs = np.array(tooth_dBs)
tooth_snrs = np.array(tooth_snrs)

# --- Comb quality metrics ---
# Only consider teeth with SNR > 10 dB as "real"
valid = tooth_snrs > 10
n_teeth = np.sum(valid)
if n_teeth > 1:
    valid_dBs = tooth_dBs[valid]
    flatness_dB = np.max(valid_dBs) - np.min(valid_dBs)
    mean_snr = np.mean(tooth_snrs[valid])
    # Spacing error: deviation of actual tooth freq from expected n*f_drive
    valid_freqs = tooth_freqs[valid]
    valid_ns = np.round(valid_freqs / f_drive).astype(int)
    spacing_errors_ppm = np.abs(valid_freqs - valid_ns * f_drive) / f_drive * 1e6
    mean_spacing_err = np.mean(spacing_errors_ppm)
else:
    flatness_dB = 0
    mean_snr = 0
    mean_spacing_err = 0

print(f"\n--- Comb Quality ---")
print(f"Teeth detected (SNR>10dB): {n_teeth} / {len(tooth_freqs)}")
print(f"Amplitude flatness: {flatness_dB:.1f} dB (lower is better)")
print(f"Mean SNR: {mean_snr:.1f} dB")
print(f"Mean spacing error: {mean_spacing_err:.0f} ppm")
for i, (f, db, snr) in enumerate(zip(tooth_freqs, tooth_dBs, tooth_snrs)):
    marker = "*" if tooth_snrs[i] > 10 else " "
    print(f"  {marker} {i+1}f0 = {f:.6f} Hz  {db:.1f} dB  SNR={snr:.1f} dB")

# --- Plot ---
fig, axes = plt.subplots(3, 1, figsize=(14, 12), gridspec_kw={'height_ratios': [2, 3, 2]})
fig.suptitle('NLTL Frequency Comb — Quality Analysis', fontsize=16, fontweight='bold')

# Time domain
ax1 = axes[0]
ax1.plot(t_ss, v_ss, 'b-', linewidth=0.3, alpha=0.7)
ax1.set_xlabel('Time (s)')
ax1.set_ylabel('V(x8) (V)')
ax1.set_title(f'Output Waveform (Steady State, T_obs={T_obs:.0f}s)')
ax1.grid(True, alpha=0.3)

# FFT with comb markers
ax2 = axes[1]
freq_mask = (freqs > 0.005) & (freqs <= f_max)
ax2.plot(freqs[freq_mask], magnitude_dB[freq_mask], 'k-', linewidth=0.5, alpha=0.6)

# Plot detected teeth as stems
for i, (f, db, snr) in enumerate(zip(tooth_freqs, tooth_dBs, tooth_snrs)):
    color = 'green' if snr > 10 else 'red'
    ax2.plot(f, db, 'o', color=color, markersize=6, zorder=5)
    ax2.vlines(f, db - 40, db, color=color, linewidth=1.5, alpha=0.7)
    label = f'{i+1}f\u2080'
    if snr > 10:
        label += f'\n{snr:.0f}dB'
    ax2.text(f, db + 3, label, ha='center', va='bottom', fontsize=7,
             color=color, fontweight='bold')

ax2.set_xlabel('Frequency (Hz)')
ax2.set_ylabel('Magnitude (dB)')
peak_dB_all = np.max(magnitude_dB[freq_mask])
ax2.set_ylim(peak_dB_all - 80, peak_dB_all + 20)
ax2.set_xlim(0, f_max)
ax2.set_title('Frequency Comb (green = SNR>10dB, red = weak/buried)')
ax2.grid(True, alpha=0.3)

comb_ticks = np.arange(0, f_max + f_drive, f_drive)
ax2.set_xticks(comb_ticks)
ax2.set_xticklabels([f'{f:.2f}' for f in comb_ticks], fontsize=7, rotation=45)

# Comb quality summary bar chart
ax3 = axes[2]
if n_teeth > 0:
    bar_colors = ['green' if s > 10 else 'red' for s in tooth_snrs]
    x_pos = np.arange(len(tooth_freqs))
    ax3.bar(x_pos, tooth_snrs, color=bar_colors, alpha=0.8, edgecolor='black', linewidth=0.5)
    ax3.axhline(y=10, color='orange', linewidth=1.5, linestyle='--', label='SNR threshold (10 dB)')
    ax3.set_xticks(x_pos)
    ax3.set_xticklabels([f'{i+1}f\u2080' for i in range(len(tooth_freqs))], fontsize=9)
    ax3.set_ylabel('SNR (dB)')
    ax3.set_title(f'Comb Quality: {n_teeth} teeth, flatness={flatness_dB:.1f}dB, '
                  f'mean SNR={mean_snr:.1f}dB, spacing err={mean_spacing_err:.0f}ppm')
    ax3.legend(fontsize=9)
    ax3.grid(True, alpha=0.3, axis='y')
else:
    ax3.text(0.5, 0.5, 'No comb teeth detected (SNR > 10 dB)', transform=ax3.transAxes,
             ha='center', va='center', fontsize=14, color='red')

plt.tight_layout()
out_path = work_dir / "frequency_comb.png"
plt.savefig(out_path, dpi=150, bbox_inches='tight')
print(f"\nSaved {out_path}")
plt.show()
