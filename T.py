import numpy as np
import matplotlib.pyplot as plt

# 1. Створюємо сітку значень для фазової площини
x = np.linspace(-3, 3, 400)
y = np.linspace(-3, 3, 400)
X, Y = np.meshgrid(x, y)

# 2. Праві частини системи: dx/dt = -x + 2y, dy/dt = x + y
U = -X + 2*Y
V = X + Y

fig, ax = plt.subplots(figsize=(9, 8), dpi=150)

# 3. Малюємо векторне поле (фазові траєкторії)
ax.streamplot(X, Y, U, V, color='lightgray', density=1.3, linewidth=1, arrowsize=1.2)

# 4. Точні значення для сепаратрис (власних векторів)
# Вхідна сепаратриса h1: y = x / (-(1 + sqrt(3))) ≈ -0.366 * x
# Вихідна сепаратриса h2: y = x / (sqrt(3) - 1) ≈ 1.366 * x
x_lines = np.linspace(-3, 3, 200)
y_h1 = x_lines / (-(1 + np.sqrt(3)))
y_h2 = x_lines / (np.sqrt(3) - 1)

# Малюємо сепаратриси
ax.plot(x_lines, y_h1, 'r-', linewidth=2.5, label=r'Вхідна сепаратриса $h^{(1)}$ ($\lambda_1 = -\sqrt{3}$)')
ax.plot(x_lines, y_h2, 'g-', linewidth=2.5, label=r'Вихідна сепаратриса $h^{(2)}$ ($\lambda_2 = \sqrt{3}$)')

# 5. Позначення точки рівноваги (0,0)
ax.plot(0, 0, 'ko', markersize=9, zorder=5)
ax.annotate('Точка рівноваги (0,0)\n[Сідло]', xy=(0, 0), xytext=(0.15, -0.4),
            arrowprops=dict(facecolor='black', shrink=0.05, width=1, headwidth=6),
            fontweight='bold', fontsize=10, backgroundcolor='white')

# 6. Ключові опорні точки для побудови в зошиті:

# Точка А на вхідній сепаратрисі h1: (x = -2.73, y = 1)
ax.plot(-2.73, 1, 'ro', markersize=7)
ax.annotate('Точка A (-2.73, 1)\n(для вхідної лінії h1)', xy=(-2.73, 1), xytext=(-2.8, 1.5),
            arrowprops=dict(facecolor='red', shrink=0.05, width=1, headwidth=5),
            fontsize=9, color='darkred', fontweight='bold', backgroundcolor='white')

# Точка B на вихідній сепаратрисі h2: (x = 0.73, y = 1) або (x = 2.19, y = 3)
ax.plot(0.73, 1, 'go', markersize=7)
ax.annotate('Точка B (0.73, 1)\n(для вихідної лінії h2)', xy=(0.73, 1), xytext=(1.1, 0.6),
            arrowprops=dict(facecolor='green', shrink=0.05, width=1, headwidth=5),
            fontsize=9, color='darkgreen', fontweight='bold', backgroundcolor='white')

# 7. Додаємо стрілки напрямку на самих сепаратрисах
# Для h1 (вхідна - до нуля)
ax.annotate('', xy=(-1.36, 0.5), xytext=(-2.05, 0.75),
            arrowprops=dict(arrowstyle="->", color="red", lw=2.5, mutation_scale=20))
# Для h2 (вихідна - від нуля)
ax.annotate('', xy=(1.46, 2.0), xytext=(0.73, 1.0),
            arrowprops=dict(arrowstyle="->", color="green", lw=2.5, mutation_scale=20))

# Оформлення графіка
ax.axhline(0, color='black', linewidth=1, alpha=0.5)
ax.axvline(0, color='black', linewidth=1, alpha=0.5)
ax.set_xlim(-3, 3)
ax.set_ylim(-3, 3)
ax.set_xlabel('Фазова координата x', fontsize=11)
ax.set_ylabel('Фазова координата y', fontsize=11)
ax.set_title('Фазовий портрет Завдання 4 з підписаними опорними точками', fontsize=12, fontweight='bold')
ax.grid(True, linestyle=':', alpha=0.6)
ax.legend(loc='upper left', fontsize=9)

plt.tight_layout()
plt.show()