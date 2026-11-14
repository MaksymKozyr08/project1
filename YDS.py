import numpy as np
import matplotlib.pyplot as plt

# 1. Розімкнена система
fig1, ax1 = plt.subplots(figsize=(7, 6))

X1, Y1 = np.meshgrid(np.linspace(-25, 25, 40), np.linspace(-25, 25, 40))
U1 = -2*X1 - 5*Y1
V1 = 2*X1 + 2*Y1

ax1.streamplot(X1, Y1, U1, V1, color='#2b5c8f', density=2.2, arrowsize=1.2)
ax1.set_xlim(-25, 25)
ax1.set_ylim(-25, 25)
ax1.set_xlabel('$x(t)$')
ax1.set_ylabel('$y(t)$')
ax1.axhline(0, color='black', linewidth=0.8)
ax1.axvline(0, color='black', linewidth=0.8)
ax1.grid(True, alpha=0.3)

# 2. Замкнена система
fig2, ax2 = plt.subplots(figsize=(7, 6))

X2, Y2 = np.meshgrid(np.linspace(-10, 10, 40), np.linspace(-10, 10, 40))
U2 = -8*X2 - 12*Y2
V2 = 2*X2 + 2*Y2

ax2.streamplot(X2, Y2, U2, V2, color='#2b5c8f', density=1.5, arrowsize=1.2)

x_line = np.linspace(-10, 10, 100)
ax2.plot(x_line, -1/3 * x_line, color='red', linewidth=2, label='Separatrix 1')
ax2.plot(x_line, -1/2 * x_line, color='green', linewidth=2, label='Separatrix 2')
ax2.plot(x_line, -1.0 * x_line, color='black', linewidth=2, linestyle='--', label='Isocline')

ax2.set_xlim(-10, 10)
ax2.set_ylim(-10, 10)
ax2.set_xlabel('$x(t)$')
ax2.set_ylabel('$y(t)$')
ax2.axhline(0, color='black', linewidth=0.8)
ax2.axvline(0, color='black', linewidth=0.8)
ax2.legend(loc='upper right')
ax2.grid(True, alpha=0.3)

plt.show()