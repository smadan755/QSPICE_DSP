# QSPICE Digital Signal Processing Project

A collection of digital signal processing (DSP) and analog filter implementations for QSPICE circuit simulator using custom C++ DLLs and Python analysis tools.

## Project Structure

```
.
├── README.md                    # This file
├── hello_filter/               # Simple IIR digital filter (starter example)
│   ├── build_qspice_dll.bat    # Build script for MSVC
│   ├── digital_filter_x1.cpp   # First-order IIR filter implementation
│   └── digital_filter.qsch     # Filter schematic
├── second_order/               # Adaptive LMS filter with second-order system
│   ├── second_order_x1.cpp     # LMS adaptive filter (50-tap FIR)
│   ├── second_order.qsch       # Adaptive filter test schematic
│   ├── lms_sim.png            # Simulation results
│   └── second_order.pfg        # Plot configuration
├── active_filter/              # Active analog filter design and analysis
│   ├── active_filter.qsch      # Op-amp based active filter schematic
│   ├── test_filter.py          # Python filter analysis script
│   └── test_filter.ipynb       # Jupyter notebook for filter design
└── op_amp_math/               # Op-amp mathematical operations
    └── op_amp.qsch            # Op-amp circuit schematic
```

**Note:** Build outputs (`.dll`, `.obj`, `.lib`, `.exp`) and simulation data (`.qraw`, `.qopraw`) are generated in their respective directories.

## Features

### 1. Hello Filter (First-Order IIR)
A simple introductory digital filter implementing a basic IIR (Infinite Impulse Response) filter:
- **Algorithm**: `OUT = (1-a) * IN + a * y_last`
- **Filter coefficient**: `a = 0.90`
- **Type**: Low-pass filter
- **Use case**: Learning basic digital filter concepts in QSPICE

### 2. Adaptive LMS Filter (Second-Order System)
Advanced adaptive filtering using the Least Mean Squares (LMS) algorithm:
- **Architecture**: 50-tap FIR filter
- **Algorithm**: LMS adaptive filtering for system identification
- **Features**:
  - Real-time weight adaptation
  - Clock division (10,000:1) for convergence stability
  - Error signal output for convergence monitoring
- **Use case**: Adaptive noise cancellation, system identification, echo cancellation

### 3. Active Analog Filters
Op-amp based active filter design with Python analysis:
- **Components**: Op-amp circuits with R, L, C components
- **Analysis Tools**: 
  - Python scripts for frequency response analysis
  - Jupyter notebooks for interactive filter design
  - Transfer function calculations
- **Use case**: Analog filter prototyping, frequency response analysis

### 4. Op-Amp Mathematical Operations
Circuit implementations of mathematical operations using operational amplifiers.

## Digital Filter Implementation

### Hello Filter (Simple IIR)

The filter implements a simple IIR (Infinite Impulse Response) digital filter with the equation:

```
OUT = (1-a) * IN + a * y_last
```

Where:
- `a = 0.90` (filter coefficient)
- `IN` is the input signal
- `OUT` is the filtered output
- The filter is clocked and updates on the rising edge of CLK

### Adaptive LMS Filter

The second-order project implements a 50-tap FIR adaptive filter using the LMS algorithm:

```cpp
// Prediction: y_est = Σ(w[i] * x[i])
// Error: e = desired - y_est
// Weight Update: w[i] = w[i] + μ * e * x[i]
```

Parameters:
- **Filter length**: 50 taps
- **Learning rate (μ)**: 0.001
- **Clock division**: 10,000:1 for stable convergence
- **Outputs**: Estimated signal and error for monitoring

## Building

### Prerequisites

- **QSPICE** - Circuit simulator ([download here](https://www.qorvo.com/products/design-tools/qspice))
- **Microsoft Visual Studio 2022** (Community Edition or higher) with C++ tools
- **Python 3.x** (optional, for active filter analysis)
  - NumPy
  - Matplotlib
  - Jupyter (for notebook analysis)

### Build in VS Code

1. Open this folder in VS Code
2. Press `Ctrl+Shift+B` or select **Terminal → Run Build Task**
3. The DLL will be compiled as `digital_filter_x1.dll`

### Build from Command Line

Navigate to the project directory (e.g., `hello_filter/` or `second_order/`) and run:
```cmd
cd hello_filter
build_qspice_dll.bat digital_filter_x1.cpp
```

Or for the adaptive filter:
```cmd
cd second_order
build_qspice_dll.bat second_order_x1.cpp
```

## Usage in QSPICE

### Digital Filters (C++ DLL)

1. Build the DLL using VS Code or the batch script
2. Open the corresponding `.qsch` file in QSPICE:
   - `hello_filter/digital_filter.qsch` for basic IIR filter
   - `second_order/second_order.qsch` for adaptive LMS filter
3. Run the simulation - QSPICE will automatically load the compiled DLL
4. The DLL must be in the same directory as the schematic file

### Active Filter Analysis (Python)

1. Navigate to `active_filter/` directory
2. Run the Python script:
   ```cmd
   python test_filter.py
   ```
3. Or open `test_filter.ipynb` in Jupyter for interactive analysis:
   ```cmd
   jupyter notebook test_filter.ipynb
   ```

## Technical Notes

### Digital Filter DLLs

- **32-bit DLL Required**: QSPICE is a 32-bit application, so the DLL must be compiled for x86 (32-bit)
- **Calling Convention**: Uses `extern "C" __declspec(dllexport)` for proper linking
- **Static Variables**: Filter state is maintained in static variables between calls
- **Clock-Triggered**: Filters update on the rising edge of the CLK signal

### LMS Adaptive Filter

- **Convergence**: Uses clock division (10,000:1) to slow down adaptation for stable convergence
- **Filter Order**: 50-tap FIR provides good balance between performance and computation
- **Learning Rate**: μ = 0.001 chosen for stable convergence
- **Error Monitoring**: Secondary output provides real-time error signal for convergence analysis

## Modifying the Filters

### Simple IIR Filter

To change filter behavior in `hello_filter/`:

1. Edit `hello_filter/digital_filter_x1.cpp`
2. Rebuild with `Ctrl+Shift+B`
3. Rerun the simulation in QSPICE

Common modifications:
- Change `a` coefficient for different filtering characteristics
- Implement different filter types (Butterworth, Chebyshev, etc.)
- Add additional states for higher-order filters

### Adaptive LMS Filter

To modify the adaptive filter in `second_order/`:

1. Edit `second_order/second_order_x1.cpp`
2. Adjust parameters:
   - `w.size()`: Change filter length (number of taps)
   - `mu`: Adjust learning rate for faster/slower convergence
   - `DIV_RATIO`: Modify clock division for convergence speed
3. Rebuild and test in QSPICE

### Active Filters

Modify Python scripts in `active_filter/` to:
- Change component values (R, L, C)
- Analyze different frequency ranges
- Plot magnitude and phase responses
- Design custom transfer functions

## Applications

- **Adaptive Noise Cancellation**: Use LMS filter to remove noise from desired signals
- **System Identification**: Model unknown systems using adaptive filtering
- **Active Filter Design**: Prototype and analyze op-amp based analog filters
- **Digital Filter Learning**: Understand DSP concepts with hands-on QSPICE simulations
- **Echo Cancellation**: Implement adaptive echo cancellation systems
- **Signal Conditioning**: Design custom filters for sensor signal processing

## License

This project is provided as-is for educational and engineering purposes.
