// Automatically generated C++ file on Wed Nov 26 13:32:38 2025
//
// To build with Digital Mars C++ Compiler:
//
//    dmc -mn -WD second_order_x1.cpp kernel32.lib

#include <vector>


union uData
{
   bool b;
   char c;
   unsigned char uc;
   short s;
   unsigned short us;
   int i;
   unsigned int ui;
   float f;
   double d;
   long long int i64;
   unsigned long long int ui64;
   char *str;
   unsigned char *bytes;
};

// int DllMain() must exist and return 1 for a process to load the .DLL
// See https://docs.microsoft.com/en-us/windows/win32/dlls/dllmain for more information.
int __stdcall DllMain(void *module, unsigned int reason, void *reserved) { return 1; }


#undef IN
#undef OUT
#undef CLK
#undef FN_IN
#undef FN_OUT

static bool clk_last = false;
static std::vector<double> w(50, 0.0);
static std::vector<double> x(50, 0.0);
static double mu = 0.001;
static int div_counter = 0;
const int DIV_RATIO = 10000;


extern "C" __declspec(dllexport) void second_order_x1(void **opaque, double t, union uData *data)
{
    double  IN     = data[0].d; // Desired Signal (Output from MEMS)
    bool    CLK    = data[1].b; // Clock
    double  FN_IN  = data[2].d; // Reference Input (source)
    double &OUT    = data[3].d; // Algorithm Output
    double &FN_OUT = data[4].d; // Debug: output error



    // 1. Rising Edge Detection
    if (CLK == true && clk_last == false) {

        // --- PRE-PROCESSING ---

        div_counter++;

        if (div_counter >= DIV_RATIO) {

        div_counter = 0;

        double desired = 2 * IN;
        double input   = 2 * FN_IN;

        // --- STEP 1: SHIFT REGISTER (Update History) ---
        // Move everything to the right
        for (int i = x.size() - 1; i > 0; i--) {
            x[i] = x[i - 1];
        }
        // Insert new sample at front
        x[0] = input;

        // --- STEP 2: PREDICT (FIR Filter) ---
        double y_est = 0.0;
        for (size_t i = 0; i < w.size(); i++) {
            y_est += w[i] * x[i];
        }

        // --- STEP 3: CALCULATE ERROR ---
        // Error = Desired (Real Plant) - Estimated (Filter)
        double error = desired - y_est;

        // --- STEP 4: UPDATE WEIGHTS (LMS) ---
        // w[n+1] = w[n] + mu * error * x[n]
        for (size_t i = 0; i < w.size(); i++) {
             w[i] = w[i] + (mu * error * x[i]);
        }

        // output the estimated signal to see convergence
        OUT = y_est;
        FN_OUT = error; // output the error to plot convergence

        }

    }

    // 2. Save Clock State for next call
    clk_last = CLK;
}
