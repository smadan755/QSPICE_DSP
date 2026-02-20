import numpy as np
import matplotlib.pyplot as plt

# --- Simulation Parameters (Matching .tran 0 100m) ---
fs = 1e6  # 1MHz sampling rate for high-frequency carrier fidelity
t = np.linspace(0, 0.1, int(0.1 * fs))

# --- Inputs (Matching QSPICE Voltage Sources) ---
# ground_motion: sine 0 100m 100 (100mV amplitude at 100Hz)
# modulation: sine 0 20n 17K (20nV amplitude at 17kHz)
f_ground = 100
f_mod = 17000
v_ground = 100e-3 * np.sin(2 * np.pi * f_ground * t)  # 100mV
v_mod = 20e-9 * np.sin(2 * np.pi * f_mod * t)          # 20nV (tiny!)

# --- Mechanical Displacement (V(disp) node) ---
# Sum of seismic and carrier signals passing through RLC
# For simplicity in plotting the waveform effect, we treat V(disp) as the sum
v_disp = v_ground + v_mod

# --- Optical Power (B1 Behavioral Source) ---
# QSPICE B1 Equation: V = 0.5m * (1 + cos(14804071 * V(disp)))
# Note: 0.5m = 0.5e-3 (millivolts), coefficient is NOT doubled
phase_coeff = 14804071
opt_power = 0.5e-3 * (1 + np.cos(phase_coeff * v_disp))

# --- TIA Output (B2 and TIA stage) ---
# B2: I = 0.5m * V(opt_power)
# R2: 100k (Gain) -> V_tia = I * R2
i_pd = 0.5e-3 * opt_power  # 0.5mA/V responsivity
v_tia = i_pd * 100e3       # 100K transimpedance gain

# --- Plotting ---
plt.figure(figsize=(12, 6))
plt.plot(t * 1000, v_tia * 1000, color='limegreen', linewidth=1)  # Convert to mV
plt.title('Simulated V(v_tia) Waveform (Fringe Counting)')
plt.xlabel('Time [ms]')
plt.ylabel('Voltage [mV]')
plt.xlim(40, 46)  # Zoomed to match your uploaded screenshot
plt.grid(True, alpha=0.3)
plt.show()