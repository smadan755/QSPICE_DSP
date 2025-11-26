import numpy as np
import matplotlib.pyplot as plt


f = np.linspace(0.001,0.6e3,10000)
w = 2*np.pi*f
s = 1j*w


Rin = 100e3
Rf = 1e3
Cf = 0.01e-6
L = 100e-3

Zf = (1/(s*Cf)) + Rf
Zin = s*L

H = -(Zf)/(Zin)

plt.figure(figsize=(12,6))
plt.plot(f, 20*np.log10(abs(H)))
plt.xlim([0,80])
plt.show()
