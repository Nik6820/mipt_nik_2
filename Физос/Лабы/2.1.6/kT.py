import numpy as np
import matplotlib.pyplot as plt

# Данные: коэффициент Джоуля-Томсона и обратная температура
mu = np.array([1.12, 1.06, 0.89])              # коэффициент μ, K   /атм
err_mu = np.array([0.02, 0.02, 0.05])           # погрешности μ

invT = np.array([0.00338741912536838, 0.00329793549238177,	0.00309453814018258])  # 1/T, 1/K
err_invT = np.array([1.14746083309115E-06,	1.08763785119114E-06,	9.57616630104465E-07])  # погрешности 1/T

# Линейная регрессия (МНК) для μ = A * (1/T) + B
coeffs = np.polyfit(invT, mu, 1)
A, B = coeffs  # A - наклон, B - свободный член
print(f"Наклон (A) = {A:.4f} °C·К/атм")
print(f"Свободный член (B) = {B:.4f} °C/атм")

# Оценка погрешностей наклона и свободного члена
n = len(invT)
residuals = mu - (A * invT + B)
s2 = np.sum(residuals**2) / (n - 2)  # несмещённая оценка дисперсии остатков

# Средние значения
x_mean = np.mean(invT)
x_var = np.sum((invT - x_mean)**2)

# Погрешность наклона
var_A = s2 / x_var
std_A = np.sqrt(var_A)

# Погрешность свободного члена
var_B = s2 * (1/n + x_mean**2 / x_var)
std_B = np.sqrt(var_B)

print(f"Погрешность наклона: {std_A:.4f} °C·К/атм")
print(f"Погрешность свободного члена: {std_B:.4f} °C/атм")

# Построение графика с учётом погрешностей
plt.figure(figsize=(8, 6))
plt.errorbar(invT, mu, yerr=err_mu, xerr=err_invT, fmt='o', capsize=3,
             label='Экспериментальные точки', color='blue', markersize=8,
             ecolor='black', elinewidth=1, markeredgewidth=1)

# Аппроксимирующая прямая
x_fit = np.linspace(0.003, 0.0034, 100)
y_fit = A * x_fit + B
plt.plot(x_fit, y_fit, 'r-', linewidth=2,
         label=f'МНК: μ = ({A:.3f} ± {std_A:.3f})·(1/T) + ({B:.3f} ± {std_B:.3f})')

plt.xlabel('Обратная температура 1/T, 1/K', fontsize=20)
plt.ylabel('Коэффициент Джоуля–Томсона μ, K/атм', fontsize=20)
plt.title('Зависимость коэффициента Джоуля–Томсона от обратной температуры', fontsize=20)
plt.grid(True, linestyle='--', alpha=0.7)
plt.legend(fontsize=18)
plt.tight_layout()
plt.show()

# Доверительные интервалы для предсказания (опционально)
from scipy import stats

# Доверительный интервал для коэффициентов (95%)
t_val = stats.t.ppf(0.975, n-2)  # квантиль распределения Стьюдента
print(f"\n95% доверительные интервалы:")
print(f"Наклон A: [{A - t_val*std_A:.4f}, {A + t_val*std_A:.4f}] °C·К/атм")
print(f"Свободный член B: [{B - t_val*std_B:.4f}, {B + t_val*std_B:.4f}] °C/атм")

# Построение доверительной полосы для регрессии
x_conf = np.linspace(0.003, 0.0034, 100)
y_conf = A * x_conf + B

# Стандартная ошибка предсказания
se_pred = np.sqrt(s2 * (1/n + (x_conf - x_mean)**2 / x_var))
ci = t_val * se_pred  # полуширина доверительного интервала

plt.figure(figsize=(8, 6))
plt.errorbar(invT, mu, yerr=err_mu, xerr=err_invT, fmt='o', capsize=3,
             label='Экспериментальные точки', color='blue', markersize=8,
             ecolor='black', elinewidth=1)
plt.plot(x_conf, y_conf, 'r-', linewidth=2, label='Регрессионная прямая')
plt.fill_between(x_conf, y_conf - ci, y_conf + ci, alpha=0.2, color='red',
                 label='95% доверительная полоса')
plt.xlabel('Обратная температура 1/T, 1/°C', fontsize=20)
plt.ylabel('Коэффициент Джоуля–Томсона μ, °C/атм', fontsize=20)
plt.title('Зависимость μ от 1/T с доверительной полосой', fontsize=20)
plt.grid(True, linestyle='--', alpha=0.7)
plt.legend(fontsize=18)
plt.tight_layout()
#plt.show()
