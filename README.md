# QSPICE Digital Signal Processing Project

A collection of DSP, nonlinear dynamics, and analog filter implementations for the QSPICE circuit simulator using custom C++ DLLs, behavioral sources, and Python analysis tools.

## Project Structure

```
.
├── README.md
├── hello_filter/                # Simple IIR digital filter (starter example)
│   ├── digital_filter_x1.cpp   # First-order IIR low-pass filter
│   ├── digital_filter.qsch     # Filter schematic
│   └── build_qspice_dll.bat    # Build script for MSVC
├── second_order/                # Adaptive LMS filter
│   ├── second_order_x1.cpp     # 50-tap FIR LMS adaptive filter
│   ├── second_order.qsch       # Adaptive filter test schematic
│   └── second_order.pfg        # Plot configuration
├── active_filter/               # Active analog filter design
│   ├── active_filter.qsch      # Op-amp based active filter schematic
│   └── test_filter.py          # Python frequency response analysis
├── butter/                      # Butterworth filter
│   └── butter.qsch             # Butterworth filter schematic
├── op_amp_math/                 # Op-amp mathematical operations
│   └── op_amp.qsch             # Op-amp circuit schematic
├── wavegen/                     # Digital waveform generator
│   ├── wavegen_x1.cpp          # Recursive sine oscillator (Goertzel)
│   └── wavegen.qsch            # Waveform generator schematic
├── fringe_counting/             # Optical interferometric sensor simulation
│   ├── fringe_counting_x1.cpp  # Fabry-Perot fringe counting model
│   ├── fringe_counting.qsch    # Fringe counting schematic
│   ├── sia_sensor.qsch         # SIA sensor schematic
│   └── debug.py                # Python verification/plotting script
└── duffing/                     # Duffing oscillator & nonlinear transmission line
    ├── duffing_base.qsch       # Single Duffing oscillator (sharkfin response)
    ├── duffing.qsch            # 8-section NLTL frequency comb generator
    ├── plot_comb.py            # PyQSPICE-based FFT analysis with comb quality metrics
    └── analyze_comb.ipynb      # Jupyter notebook for comb analysis
```

## Modules

### 1. Hello Filter (First-Order IIR)

A simple introductory digital filter implementing a basic IIR low-pass filter:
- **Algorithm**: `OUT = (1-a) * IN + a * y_last`
- **Filter coefficient**: `a = 0.90`
- **Use case**: Learning basic digital filter concepts in QSPICE

### 2. Adaptive LMS Filter

Advanced adaptive filtering using the Least Mean Squares algorithm:
- **Architecture**: 50-tap FIR filter
- **Learning rate**: mu = 0.001
- **Clock division**: 10,000:1 for convergence stability
- **Outputs**: Estimated signal and real-time error for convergence monitoring
- **Use case**: System identification, adaptive noise cancellation

### 3. Active Analog Filter

Op-amp based active filter with Python frequency response analysis:
- Inverting amplifier topology with impedance feedback (L input, RC feedback)
- Python script computes and plots the transfer function H(s) = -Z_f / Z_in

### 4. Butterworth Filter

Butterworth filter schematic for maximally-flat magnitude response design.

### 5. Op-Amp Mathematical Operations

Circuit implementations of mathematical operations using operational amplifiers.

### 6. Waveform Generator (Goertzel Oscillator)

A digital sine wave generator using a recursive second-order IIR structure:
- **Algorithm**: `y[n] = 2*cos(w)*y[n-1] - y[n-2] + sin(w)*x[n-1]`
- **Frequency**: omega = pi/8 (fixed)
- Generates a pure sine wave from a single impulse input using only multiplies and adds

### 7. Fringe Counting (Optical Interferometric Sensor)

Simulates a Fabry-Perot interferometric displacement sensor:
- Models optical phase from mechanical displacement: `phase = 4*pi*(d_bias + x) / lambda`
- Photodetector output: `V_pd = cos^2(phase)`
- Spring constant k = 516.5 N/m, wavelength lambda = 850 nm
- Includes TIA (transimpedance amplifier) readout stage
- Python debug script for independent waveform verification

### 8. Duffing Oscillator & NLTL Frequency Comb

Nonlinear dynamics simulations based on the Duffing equation:

**Single Oscillator** (`duffing_base.qsch`):
- Series RLC loop: V1 -> L1 -> R1 -> B1 -> C1 -> GND
- B1 implements hardening spring: `V = V(x) + V(x)**3`
- Produces the classic sharkfin frequency response with hysteresis
- Node `x` (between B1 and C1) represents displacement
- Equation: `x'' + delta*x' + x + beta*x^3 = gamma*sin(wt)`

**NLTL Frequency Comb** (`duffing.qsch`):
- 8-section nonlinear transmission line (LC ladder with Duffing shunt capacitors)
- Each section: inductor in series, B+C pair shunting to ground
- B sources: `V = -0.1*V(xN)**2 - 0.05*V(xN)**3` (quadratic + cubic nonlinearity)
- Generates frequency combs at harmonics of the drive frequency
- Source and load impedance matched to Z0 = sqrt(L/C)

**Python Analysis** (`plot_comb.py`):
- Reads simulation data via PyQSPICE
- FFT with Hanning window and steady-state extraction
- Comb quality metrics: tooth count, amplitude flatness, per-tooth SNR, spacing accuracy (ppm)

## Building

### Prerequisites

- [QSPICE](https://www.qorvo.com/products/design-tools/qspice) circuit simulator
- Microsoft Visual Studio 2022 (Community Edition or higher) with C++ tools
- Python 3.x with NumPy, Matplotlib (for analysis scripts)
- [PyQSPICE](https://pypi.org/project/PyQSPICE/) (for duffing/plot_comb.py)

### Build DLLs

From VS Code: `Ctrl+Shift+B` runs the build task.

From command line:
```cmd
cd hello_filter
build_qspice_dll.bat digital_filter_x1.cpp
```

### Run in QSPICE

1. Build the DLL (must be in same directory as `.qsch`)
2. Open the `.qsch` file in QSPICE
3. Run the simulation

### Python Analysis

```cmd
cd duffing
python plot_comb.py
```

## Technical Notes

- **32-bit DLLs**: QSPICE requires x86 (32-bit) DLLs
- **Calling convention**: `extern "C" __declspec(dllexport)`
- **Clock-triggered**: All digital filters update on the rising edge of CLK
- **Behavioral sources**: Duffing circuits use QSPICE behavioral voltage sources (B) for nonlinear elements
- **PyQSPICE**: Uses QUX.exe to export .qraw data into uniform-sampled pandas DataFrames (better for FFT than raw adaptive-step data)

## License

This project is provided as-is for educational and engineering purposes.
