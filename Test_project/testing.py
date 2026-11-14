import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint

colors = ['red', 'blue', 'green', 'magenta']

# ==========================================
# Завдання 1
# ==========================================
plt.figure(figsize=(7, 6))
X, Y = np.meshgrid(np.linspace(-4, 4, 25), np.linspace(-4, 4, 25))
X_safe = np.where(np.abs(X) < 1e-3, np.nan, X)
DY = (Y**2 - Y) / X_safe
DX = np.ones_like(DY)
N = np.hypot(DX, DY)
plt.quiver(X, Y, DX/N, DY/N, angles='xy', color='black', alpha=0.35, width=0.003)

pts1 = [[1, 2], [-1, 2], [-1, -1], [1, -1]]
labels1 = ["(1, 2)", "(-1, 2)", "(-1, -1)", "(1, -1)"]

for i, (x0, y0) in enumerate(pts1):
    c = (1 - 1/y0) / x0
    if x0 > 0:
        x_grid = np.linspace(0.01, 4, 1000)
    else:
        x_grid = np.linspace(-4, -0.01, 1000)
    
    y_sol = 1 / (1 - c * x_grid)
    
    denom = 1 - c * x_grid
    y_sol[np.abs(denom) < 0.02] = np.nan
    
    plt.plot(x_grid, y_sol, color=colors[i], linewidth=2, label=labels1[i])
    plt.plot(x0, y0, 'o', color=colors[i])

plt.xlim(-4, 4)
plt.ylim(-4, 4)
plt.xlabel('x')
plt.ylabel('y(x)')
plt.title('Завдання 1')
plt.axhline(0, color='gray', linewidth=0.8)
plt.axvline(0, color='gray', linewidth=0.8)
plt.grid(True, linestyle='--', alpha=0.5)
plt.legend(loc='upper right')
plt.tight_layout()
plt.show()

# ==========================================
# Завдання 2
# ==========================================
plt.figure(figsize=(7, 6))
X, Y = np.meshgrid(np.linspace(-6, 6, 30), np.linspace(-6, 6, 30))
Denom = X + 4*Y
Denom_safe = np.where(np.abs(Denom) < 1e-3, np.nan, Denom)
DY = (2*X + 3*Y - 5) / Denom_safe
DX = np.ones_like(DY)
N = np.hypot(DX, DY)
plt.quiver(X, Y, DX/N, DY/N, angles='xy', color='black', alpha=0.35, width=0.003)

pts2 = [[1, 1], [-1, 1], [-1, -2], [2, -2]]
labels2 = ["(1, 1)", "(-1, 1)", "(-1, -2)", "(2, -2)"]

X_fine, Y_fine = np.meshgrid(np.linspace(-6, 6, 500), np.linspace(-6, 6, 500))
# Точний загальний інтеграл рівняння: (x + y - 1)^2 * |2x + y - 3| = C
F = ((X_fine + Y_fine - 1)**2) * np.abs(2*X_fine + Y_fine - 3)

for i, (x0, y0) in enumerate(pts2):
    C_val = ((x0 + y0 - 1)**2) * np.abs(2*x0 + y0 - 3)
    plt.contour(X_fine, Y_fine, F, levels=[C_val], colors=[colors[i]], linewidths=2)
    plt.plot(x0, y0, 'o', color=colors[i], label=labels2[i])

plt.xlim(-6, 6)
plt.ylim(-6, 6)
plt.xlabel('x')
plt.ylabel('y(x)')
plt.title('Завдання 2')
plt.axhline(0, color='gray', linewidth=0.8)
plt.axvline(0, color='gray', linewidth=0.8)
plt.grid(True, linestyle='--', alpha=0.5)
plt.legend(loc='lower right')
plt.tight_layout()
plt.show()

# ==========================================
# Завдання 3
# ==========================================
plt.figure(figsize=(7, 6))
X, Y = np.meshgrid(np.linspace(-6, 6, 25), np.linspace(-6, 6, 25))
X_safe = np.where(np.abs(X) < 1e-3, np.nan, X)
DY = Y / X_safe + X_safe * np.cos(X_safe)
DX = np.ones_like(DY)
N = np.hypot(DX, DY)
plt.quiver(X, Y, DX/N, DY/N, angles='xy', color='black', alpha=0.35, width=0.003)

pts3 = [[np.pi/2, np.pi], [-np.pi/2, np.pi], [-np.pi/2, -np.pi], [np.pi/2, -np.pi]]
labels3 = [r"$(\pi/2, \pi)$", r"$(-\pi/2, \pi)$", r"$(-\pi/2, -\pi)$", r"$(\pi/2, -\pi)$"]

for i, (x0, y0) in enumerate(pts3):
    c = y0 / x0 - np.sin(x0)
    if x0 > 0:
        x_vals = np.linspace(0.01, 6, 400)
    else:
        x_vals = np.linspace(-6, -0.01, 400)
        
    y_sol = x_vals * np.sin(x_vals) + c * x_vals
    plt.plot(x_vals, y_sol, color=colors[i], linewidth=2, label=labels3[i])
    plt.plot(x0, y0, 'o', color=colors[i])

plt.xlim(-6, 6)
plt.ylim(-6, 6)
plt.xlabel('x')
plt.ylabel('y(x)')
plt.title('Завдання 3')
plt.axhline(0, color='gray', linewidth=0.8)
plt.axvline(0, color='gray', linewidth=0.8)
plt.grid(True, linestyle='--', alpha=0.5)
plt.legend(loc='lower left')
plt.tight_layout()
plt.show()

# ==========================================
# Завдання 4 (Графік розв'язків)
# ==========================================
plt.figure(figsize=(7, 6))
ics4 = [[1.0, 1.0], [-1.0, 1.0], [-1.0, -1.0], [1.0, -1.0]]
labels4 = ["(y=1, y'=1)", "(y=-1, y'=1)", "(y=-1, y'=-1)", "(y=1, y'=-1)"]

def odes_task4(state, x):
    y, v = state
    return [v, 9*y + np.exp(-3*x)*(x**2 + np.sin(3*x))]

for i, (y0, v0) in enumerate(ics4):
    x_pos = np.linspace(0, 1.0, 200)
    sol_pos = odeint(odes_task4, [y0, v0], x_pos)
    x_neg = np.linspace(0, -1.0, 200)
    sol_neg = odeint(odes_task4, [y0, v0], x_neg)
    
    x_full = np.concatenate([x_neg[::-1], x_pos])
    y_full = np.concatenate([sol_neg[::-1, 0], sol_pos[:, 0]])
    
    plt.plot(x_full, y_full, color=colors[i], linewidth=2, label=labels4[i])
    plt.plot(0, y0, 'o', color=colors[i])

plt.xlim(-1, 1)
plt.ylim(-4, 4)
plt.xlabel('x')
plt.ylabel('y(x)')
plt.title('Завдання 4: Інтегральні криві y(x)')
plt.axhline(0, color='gray', linewidth=0.8)
plt.axvline(0, color='gray', linewidth=0.8)
plt.grid(True, linestyle='--', alpha=0.5)
plt.legend(loc='lower right')
plt.tight_layout()
plt.show()

# ==========================================
# Завдання 5 (Графіки для всіх компонент x1, x2, x3)
# ==========================================
plt.figure(figsize=(8, 6))
pts5 = [[1, 1, 1], [-1, 1, 0], [-1, -1, -2], [2, -1, 1]]
labels5 = ["(1, 1, 1)", "(-1, 1, 0)", "(-1, -1, -2)", "(2, -1, 1)"]
t = np.linspace(0, 1.5, 300)

for i, (x0, y0, z0) in enumerate(pts5):
    c2 = x0 - y0
    c3 = z0 - x0
    c1 = y0 - c3
    
    x1_t = c1 + c2*np.exp(t) + c3*np.exp(-t)
    x2_t = c1 + c3*np.exp(-t)
    x3_t = c1 - c2*np.exp(t) + c3*np.exp(-t)
    
    plt.plot(t, x1_t, color=colors[i], linestyle='-', linewidth=2, label=f'{labels5[i]} - x1(t)')
    plt.plot(t, x2_t, color=colors[i], linestyle='--', linewidth=1.5, label=f'{labels5[i]} - x2(t)')
    plt.plot(t, x3_t, color=colors[i], linestyle=':', linewidth=1.5, label=f'{labels5[i]} - x3(t)')

plt.xlim(0, 1.5)
plt.xlabel('t')
plt.ylabel('x(t)')
plt.title('Завдання 5: Динаміка компонент системи')
plt.axhline(0, color='gray', linewidth=0.8)
plt.grid(True, linestyle='--', alpha=0.5)
plt.legend(loc='upper left', bbox_to_anchor=(1, 1), fontsize=8)
plt.tight_layout()
plt.show()