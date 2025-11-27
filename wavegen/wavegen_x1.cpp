// Automatically generated C++ file on Thu Nov 27 12:49:45 2025
//
// To build with Digital Mars C++ Compiler:
//
//    dmc -mn -WD wavegen_x1.cpp kernel32.lib

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
#undef OUT

static bool clk_last = false;
static double omega = M_PI/8;
static double cos_val = cos(omega);
static double sin_val = sin(omega);
static double x_in = 1;
static double x_z1 = 0;
static double y_z1 = 0;
static double y_z2 = 0;
static bool not_stepped = true;

extern "C" __declspec(dllexport) void wavegen_x1(void **opaque, double t, union uData *data)
{
   bool    CLK = data[0].b; // input
   double &OUT = data[1].d; // output
// Implement module evaluation code here:

   if (CLK == true && CLK != clk_last) {
      OUT = 2*cos_val*y_z1 - y_z2 + sin_val*x_z1;
      y_z2 = y_z1;
      y_z1 = OUT;

      if (not_stepped) {
         x_z1 = x_in;
         not_stepped = false;
      } else {
         x_z1 = 0;
      }

   }

   clk_last = CLK;
}
