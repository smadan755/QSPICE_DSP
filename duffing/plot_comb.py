import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.signal import find_peaks
from pathlib import Path

from PyQSPICE import clsQSPICE as pqs


def analyze_odd_comb(file_name_base, node='V(x13)', f0=10.0, max_harmonic=21):
    """
    Analyzes a QSPICE transient raw file for an odd-harmonic frequency comb.
    """
    
    work_dir = Path(r"c:\Users\madan\Documents\QSPICE\QSPICE_DSP\duffing")
    qsch_file = work_dir / "duffing.qsch"
    print(f"Loading {file_name_base}.qraw via QUX.exe...")
    
    # 1. Load data using Qorvo's PyQSPICE
    run = pqs(file_name_base)
    df = run.LoadQRAW([node])
    
    # Extract time and voltage arrays from the DataFrame
    t = df['Time'].values
    v = df[node].values
    
    # 2. Ensure uniform sampling for accurate FFT
    dt = np.median(np.diff(t))
    fs = 1.0 / dt
    
    # Optional: Isolate steady-state (e.g., last 50% of the simulation)
    half_idx = len(v) // 2
    t_ss = t[half_idx:]
    v_ss = v[half_idx:]
    
    # 3. Apply Window and Compute FFT
    window = np.hanning(len(v_ss))
    v_windowed = v_ss * window
    
    fft_vals = np.fft.rfft(v_windowed)
    fft_freqs = np.fft.rfftfreq(len(v_windowed), d=dt)
    
    # Convert to dB (normalized to 1V reference)
    fft_mag = np.abs(fft_vals) * (2.0 / len(v_ss))
    fft_db = 20 * np.log10(fft_mag + 1e-12) # Add small epsilon to avoid log(0)
    
    # 4. Analyze Comb Quality (Odd Harmonics Only)
    print("\n--- Comb Quality Metrics (Odd Harmonics) ---")
    expected_odd_harmonics = [f0 * i for i in range(1, max_harmonic + 1, 2)]
    
    # Calculate Noise Floor (median of the entire spectrum)
    noise_floor_db = np.median(fft_db)
    print(f"Calculated Baseline Noise Floor: {noise_floor_db:.2f} dB")
    
    measured_freqs = []
    
    for i, target_f in enumerate(expected_odd_harmonics):
        harmonic_num = (i * 2) + 1
        
        # Search for the highest peak near the target frequency (+/- 2 Hz)
        search_mask = (fft_freqs > target_f - 2) & (fft_freqs < target_f + 2)
        if not np.any(search_mask):
            continue
            
        local_freqs = fft_freqs[search_mask]
        local_db = fft_db[search_mask]
        
        peak_idx = np.argmax(local_db)
        peak_f = local_freqs[peak_idx]
        peak_amp = local_db[peak_idx]
        
        # Calculate SNR and Spacing Error
        snr = peak_amp - noise_floor_db
        spacing_error_ppm = abs(peak_f - target_f) / target_f * 1e6
        measured_freqs.append(peak_f)
        
        print(f"Harmonic {harmonic_num}f0 ({target_f} Hz):")
        print(f"  -> Measured Freq: {peak_f:.4f} Hz (Error: {spacing_error_ppm:.2f} ppm)")
        print(f"  -> Amplitude:     {peak_amp:.2f} dB")
        print(f"  -> Peak SNR:      {snr:.2f} dB\n")

    # Calculate global comb spacing metric
    if len(measured_freqs) > 1:
        spacings = np.diff(measured_freqs)
        avg_spacing = np.mean(spacings)
        print(f"Average Comb Spacing (Target = {f0*2} Hz): {avg_spacing:.4f} Hz")
        print(f"Comb Spacing Standard Deviation: {np.std(spacings):.6f} Hz")

    # 5. Plot the Results
    plt.figure(figsize=(12, 6))
    plt.plot(fft_freqs, fft_db, color='limegreen', linewidth=1)
    
    # Highlight the odd harmonic peaks
    for f in measured_freqs:
        plt.axvline(x=f, color='white', linestyle='--', alpha=0.3)
        
    plt.title("Cascaded Duffing NLTL: Odd-Harmonic Frequency Comb (13 Stages)")
    plt.xlabel("Frequency (Hz)")
    plt.ylabel("Magnitude (dB)")
    plt.xlim(0, max(expected_odd_harmonics) + 20)
    plt.ylim(-160, 20)
    plt.grid(True, alpha=0.2)
    
    # Use dark background to match your QSPICE screenshot aesthetic
    plt.style.use('dark_background') 
    plt.show()
    
    
if __name__ == "__main__":
    # Just pass the base name of your QSPICE file

    analyze_odd_comb('duffing', node='V(x13)', f0=10.0)