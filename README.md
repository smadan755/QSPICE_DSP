# QSPICE Digital Filter Project

This project implements a digital filter C-block for QSPICE circuit simulator using custom C++ DLLs.

## Project Structure

```
.
├── digital_filter_x1.cpp        # Digital filter implementation
├── digital_filter.qsch          # Main filter schematic
├── build_qspice_dll.bat         # Build script for MSVC
├── README.md                    # This file
├── .gitignore                   # Git ignore rules
└── .vscode/
    └── tasks.json               # VS Code build tasks (Ctrl+Shift+B)
```

**Note:** Build outputs (`.dll`, `.obj`, `.lib`, `.exp`) and simulation data (`.qraw`, `.qopraw`) are automatically ignored by git.

## Digital Filter Implementation

The filter implements a simple IIR (Infinite Impulse Response) digital filter with the equation:

```
OUT = (1-a) * IN + a * y_last
```

Where:
- `a = 0.90` (filter coefficient)
- `IN` is the input signal
- `OUT` is the filtered output
- The filter is clocked and updates on the rising edge of CLK

## Building

### Prerequisites

- **QSPICE** - Circuit simulator ([download here](https://www.qorvo.com/products/design-tools/qspice))
- **Microsoft Visual Studio 2022** (Community Edition or higher) with C++ tools

### Build in VS Code

1. Open this folder in VS Code
2. Press `Ctrl+Shift+B` or select **Terminal → Run Build Task**
3. The DLL will be compiled as `digital_filter_x1.dll`

### Build from Command Line

Run the batch script:
```cmd
build_qspice_dll.bat digital_filter_x1.cpp
```

## Usage in QSPICE

1. Build the DLL using VS Code or the batch script
2. Open `digital_filter.qsch` in QSPICE
3. Run the simulation - QSPICE will automatically load the compiled DLL
4. The DLL must be in the same directory as the schematic file

## Technical Notes

- **32-bit DLL Required**: QSPICE is a 32-bit application, so the DLL must be compiled for x86 (32-bit)
- **Calling Convention**: Uses `extern "C" __declspec(dllexport)` for proper linking
- **Static Variables**: Filter state is maintained in static variables between calls
- **Clock-Triggered**: The filter only updates on the rising edge of the CLK signal

## Modifying the Filter

To change filter behavior:

1. Edit `digital_filter_x1.cpp`
2. Rebuild with `Ctrl+Shift+B`
3. Rerun the simulation in QSPICE

Common modifications:
- Change `a` coefficient for different filtering characteristics
- Implement different filter types (Butterworth, Chebyshev, etc.)
- Add additional states for higher-order filters

## License

This project is provided as-is for educational and engineering purposes.
