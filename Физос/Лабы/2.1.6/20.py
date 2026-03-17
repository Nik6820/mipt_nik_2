import numpy as np
import matplotlib.pyplot as plt

# Данные
P = np.array([3.9, 4.1, 3.8, 4.2, 3.5, 3.0, 2.0])
T = np.array([3.63636363636364, 3.83292383292383, 3.46437346437346,
              3.95577395577396, 3.12039312039312, 2.57985257985258,
              1.4987714987715])
err_T = np.array([0.0759437123073487, 0.0773925589650405, 0.0746759714818683,
                  0.0782980881260979, 0.0721404898309075, 0.0681561615222549,
                  0.0601875049049496])
err_P = 0.1  # погрешность давления (постоянная)

# Линейная регрессия (МНК)
coeffs = np.polyfit(P, T, 1)
slope, intercept = coeffs
print(f"Коэффициент наклона (μ) = {slope:.4f} °C/атм")
print(f"Свободный член = {intercept:.4f} °C")

# Оценка погрешности наклона
residuals = T - (slope*P + intercept)
s2 = np.sum(residuals**2) / (len(P)-2)
var_slope = s2 / np.sum((P - np.mean(P))**2)
std_slope = np.sqrt(var_slope)
print(f"Погрешность наклона: {std_slope:.4f} °C/атм")

# Построение графика
plt.figure(figsize=(8,6))
plt.errorbar(P, T, yerr=err_T, xerr=err_P, fmt='o', capsize=3, color='blue', markersize=6)
x_fit = np.linspace(1.5, 4.5, 100)
y_fit = slope * x_fit + intercept
plt.plot(x_fit, y_fit, 'r-', linewidth=2,
         label=f'МНК: ΔT = {slope:.3f}·ΔP {intercept:.3f}')
plt.xlabel('Перепад давления ΔP, атм', fontsize=20)
plt.ylabel('Изменение температуры ΔT, °C', fontsize=20)
plt.title('Зависимость эффекта Джоуля–Томсона от перепада давления T=22,06 °C', fontsize=20)
plt.grid(True, linestyle='--', alpha=0.7)
plt.legend(fontsize=18)
plt.tight_layout()
plt.show()
