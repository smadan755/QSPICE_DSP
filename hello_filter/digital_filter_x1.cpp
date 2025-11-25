// Automatically generated C++ file on Mon Nov 24 22:40:10 2025
//
// To build with Digital Mars C++ Compiler:
//
//    dmc -mn -WD digital_filter_x1.cpp kernel32.lib


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
#undef IN
#undef OUT
#undef CLK

static double a = 0.90;
static bool clk_last = false;
static double y_last = 0.0;
static double x_last = 0.0;


extern "C" __declspec(dllexport) void digital_filter_x1(void **opaque, double t, union uData *data)
{
   double  IN  = data[0].d; // input
   bool    CLK = data[1].b; // input
   double &OUT = data[2].d; // output

// Implement module evaluation code here:
   if (CLK == false || CLK == clk_last) {
      clk_last = CLK;
   } else {
//      if (x_last == 0) {
//         OUT = 0;
//         y_last = 0;
//         clk_last = CLK;
//         x_last = IN;
//      } else {
         OUT = (1-a)*IN + a*y_last;
         clk_last = CLK;
         y_last = OUT;
         x_last = IN;
//      }

   }
}
