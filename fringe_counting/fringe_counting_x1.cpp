// Automatically generated C++ file on Wed Nov 26 19:28:22 2025
//
// To build with Digital Mars C++ Compiler:
//
//    dmc -mn -WD fringe_counting_x1.cpp kernel32.lib

#include <cmath>

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

// #undef pin names lest they collide with names in any header file(s) you might include.
#undef CLK
#undef IN
#undef OUT

static bool clk_last = false;

extern "C" __declspec(dllexport) void fringe_counting_x1(void **opaque, double t, union uData *data)
{
   bool    CLK = data[0].b; // input
   double  IN  = data[1].d; // input
   double &OUT = data[2].d; // output

// Implement module evaluation code here:

   if (CLK == true && CLK != clk_last) {

      double V_spring_force = 2*IN;
      double k = 516.5;
      double lambda = 850e-9;
      double d_bias = 3.0 * lambda / 8.0;

      double x_meters = V_spring_force / k;
      double phase = (4.0 * M_PI * (d_bias + x_meters)) / lambda;
      double V_pd = cos(phase);

      V_pd = V_pd * V_pd;

      OUT = V_pd;


   }

   clk_last = CLK;


}
