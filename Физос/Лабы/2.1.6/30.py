import numpy as np
import matplotlib.pyplot as plt

# Данные
P = np.array([4.0, 3.7, 3.4, 3.1, 2.8, 2.5])          # перепад давления, атм
T = np.array([3.37349397590361, 3.06024096385542,
              2.72289156626506, 2.43373493975904,
              2.04819277108434, 1.80722891566265])    # изменение температуры, °C
err_T = np.array([0.0725794745246045, 0.0703149949194368,
                  0.0678763245754101, 0.0657860357091015,
                  0.0629989838873567, 0.0612570764987662])  # погрешности T
err_P = 0.1  # погрешность давления (постоянная для всех точек)

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
x_fit = np.linspace(2.5, 4, 100)
y_fit = slope * x_fit + intercept
plt.plot(x_fit, y_fit, 'r-', linewidth=2,
         label=f'МНК: ΔT = {slope:.3f}·ΔP {intercept:.3f}')
plt.xlabel('Перепад давления ΔP, атм', fontsize=20)
plt.ylabel('Изменение температуры ΔT, °C', fontsize=20)
plt.title('Зависимость эффекта Джоуля–Томсона от перепада давления\n T=30,07 °C', fontsize=20)
plt.grid(True, linestyle='--', alpha=0.7)
plt.legend(fontsize=18)
plt.tight_layout()
plt.show()
