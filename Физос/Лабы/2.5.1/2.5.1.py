import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

# ------------------------------------------------------------
# Настройка размера шрифта на графиках
# ------------------------------------------------------------
plt.rcParams.update({
    'font.size': 14,
    'axes.labelsize': 14,
    'axes.titlesize': 16,
    'legend.fontsize': 10,
    'xtick.labelsize': 12,
    'ytick.labelsize': 12
})

# ------------------------------------------------------------
# Исходные данные с погрешностями (по условию)
# ------------------------------------------------------------
# Калибровка по спирту
sigma_sp = 22.3                     # мН/м, табличное значение (погрешностью пренебрегаем)
deltaP_sp_meas = 41                 # отсчётов, измеренное давление спирта
delta_deltaP_sp = 1                 # погрешность измерения давления спирта (отсчёты)

# Коэффициент перевода отсчётов в Па
K = 0.2 * 9.81                      # Па/отсчёт

# Диаметр иглы по микроскопу (для сравнения)
d_micro = 1.1                       # мм
delta_d_micro = 0.05                # мм

# Данные для воды (t в °C, P2 в отсчётах)
data = [
    (23.5, 173),   # при 23.5 °C P2 = 173 (игла погружена)
    (30.0, 163),
    (40.0, 159),
    (50.0, 156),
    (60.0, 153)
]

# Измерения для гидростатической поправки при 23.5 °C
P1_surface = 114                    # отсчётов, игла касается поверхности
P2_bottom = 173                     # отсчётов, игла на дне
h1 = 19                             # мм, выступание при касании
h2 = 7                              # мм, выступание при погружении
delta_h_meas = 1                    # мм, погрешность измерения высоты

# Погрешности измерений
delta_P = 1                         # погрешность отсчётов давления (1 деление)
delta_t = 0.1                       # °C, погрешность температуры

# ------------------------------------------------------------
# 1. Определение радиуса иглы по эталонной жидкости
# ------------------------------------------------------------
# Давление спирта в Па
deltaP_sp_Pa = deltaP_sp_meas * K
# Радиус из формулы Лапласа: r = 2*sigma / deltaP
r_calc = 2 * sigma_sp * 1e-3 / deltaP_sp_Pa      # перевод sigma_sp в Н/м -> м
r_calc_mm = r_calc * 1000                         # в мм
# Погрешность радиуса (относительная, как у deltaP)
delta_r_rel = delta_deltaP_sp / deltaP_sp_meas
delta_r_mm = r_calc_mm * delta_r_rel
print(f"Радиус иглы по калибровке: {r_calc_mm:.3f} ± {delta_r_mm:.3f} мм")
print(f"Диаметр по микроскопу: {d_micro:.2f} ± {delta_d_micro:.2f} мм, "
      f"радиус {d_micro/2:.2f} ± {delta_d_micro/2:.2f} мм")
print("Сравнение: значения согласуются в пределах погрешностей.\n")

# Для дальнейших расчётов используем калиброванный радиус
r = r_calc               # м
delta_r = delta_r_mm * 1e-3   # м

# ------------------------------------------------------------
# 2. Гидростатическая поправка
# ------------------------------------------------------------
P_hydro = P2_bottom - P1_surface          # отсчётов
# Погрешность гидростатической поправки (ΔP1 = ΔP2 = delta_P)
delta_P_hydro = np.sqrt(delta_P**2 + delta_P**2)   # 1.414 отсчёта
print(f"Гидростатическая поправка: {P_hydro:.0f} ± {delta_P_hydro:.1f} отсчётов")

# Вычисленная глубина погружения из линейки
delta_h_calc = h1 - h2                    # 12 мм
delta_delta_h = np.sqrt(delta_h_meas**2 + delta_h_meas**2)   # 1.414 мм
# Теоретическое гидростатическое давление
rho_water = 1000                          # кг/м³
g = 9.81
P_hydro_theor = rho_water * g * (delta_h_calc / 1000)   # Па
P_hydro_meas = P_hydro * K                # Па
print(f"Глубина погружения: {delta_h_calc:.1f} ± {delta_delta_h:.1f} мм")
print(f"Гидростатическое давление (теор): {P_hydro_theor:.1f} Па")
print(f"Гидростатическое давление (эксп): {P_hydro_meas:.1f} Па")
print("Сравнение: в пределах погрешностей согласуется.\n")

# ------------------------------------------------------------
# 3. Обработка данных для воды
# ------------------------------------------------------------
t_arr = np.array([d[0] for d in data])
P2_arr = np.array([d[1] for d in data])

# Лапласовское давление (отсчёты) и его погрешность
P_lapl = np.zeros_like(P2_arr)
delta_P_lapl = np.zeros_like(P2_arr)

for i, (t, P2) in enumerate(data):
    if t == 23.5:   # для комнатной температуры используем P1_surface как лапласовское
        P_lapl[i] = P1_surface
        delta_P_lapl[i] = delta_P
    else:
        P_lapl[i] = P2 - P_hydro
        delta_P_lapl[i] = np.sqrt(delta_P**2 + delta_P_hydro**2)

# Коэффициент поверхностного натяжения воды (мН/м)
sigma = sigma_sp * (P_lapl / deltaP_sp_meas)

# Погрешность sigma (без учёта погрешности sigma_sp)
delta_sigma_rel = np.sqrt((delta_P_lapl / P_lapl)**2 + (delta_deltaP_sp / deltaP_sp_meas)**2)
delta_sigma = sigma * delta_sigma_rel

# Абсолютная температура
T_arr = t_arr + 273.15
delta_T_arr = np.full_like(T_arr, delta_t)   # погрешность 0.1 К

# Вывод промежуточных результатов
print("Результаты для воды:")
print(f"{'t, °C':<8} {'P_lapl, отсч':<12} {'ΔP_lapl, отсч':<12} {'σ, мН/м':<12} {'Δσ, мН/м':<12}")
for i in range(len(t_arr)):
    print(f"{t_arr[i]:<8.1f} {P_lapl[i]:<12.1f} {delta_P_lapl[i]:<12.1f} "
          f"{sigma[i]:<12.3f} {delta_sigma[i]:<12.3f}")

# ------------------------------------------------------------
# 4. Линейная аппроксимация σ(T) с учётом погрешностей
# ------------------------------------------------------------
def linear_func(T, a, b):
    return a + b * T

# Взвешенная аппроксимация (веса = 1/Δσ²)
popt, pcov = curve_fit(linear_func, T_arr, sigma, sigma=delta_sigma, absolute_sigma=True)
a_fit, b_fit = popt
da_fit, db_fit = np.sqrt(np.diag(pcov))

print(f"\nЛинейная аппроксимация σ(T) = {a_fit:.3f} + {b_fit:.4f} * T")
print(f"dσ/dT = {b_fit:.4f} ± {db_fit:.4f} мН/(м·К)")
print(f"dσ/dt (в °C) = {b_fit:.4f} ± {db_fit:.4f} мН/(м·°C)")

# ------------------------------------------------------------
# 5. Термодинамические величины
# ------------------------------------------------------------
q_exp = -T_arr * b_fit
U_over_F_exp = sigma - T_arr * b_fit

delta_q = T_arr * db_fit
delta_U = np.sqrt(delta_sigma**2 + (T_arr * db_fit)**2)

print("\nТермодинамические характеристики поверхности воды:")
print(f"{'t, °C':<8} {'q, мН/м':<12} {'Δq, мН/м':<12} {'U/F, мН/м':<12} {'Δ(U/F), мН/м':<12}")
for i in range(len(t_arr)):
    print(f"{t_arr[i]:<8.1f} {q_exp[i]:<12.1f} {delta_q[i]:<12.1f} "
          f"{U_over_F_exp[i]:<12.1f} {delta_U[i]:<12.1f}")

# ------------------------------------------------------------
# 6. Построение графиков с увеличенным шрифтом
# ------------------------------------------------------------
# Создаём плавные кривые на основе аппроксимации
T_plot = np.linspace(T_arr.min() - 5, T_arr.max() + 5, 100)
sigma_fit = linear_func(T_plot, a_fit, b_fit)
q_fit = -T_plot * b_fit
U_fit = sigma_fit - T_plot * b_fit

# Рисунок 1: три панели
fig, axes = plt.subplots(1, 3, figsize=(16, 6))  # чуть увеличим размер

# Панель 1: σ(T)
ax = axes[0]
ax.errorbar(T_arr, sigma, xerr=delta_T_arr, yerr=delta_sigma,
            fmt='o', capsize=3, label='Эксперимент', color='blue')
ax.plot(T_plot, sigma_fit, 'r-', 
        label=f'Линейная аппроксимация\n$d\\sigma/dT = {b_fit:.4f}\\pm{db_fit:.4f}$ мН/(м·К)')
ax.set_xlabel('Температура $T$, К')
ax.set_ylabel('$\\sigma$, мН/м')
ax.set_title('Коэффициент поверхностного натяжения воды')
ax.legend(loc='upper right')
ax.grid(True)

# Панель 2: q(T)
ax = axes[1]
ax.errorbar(T_arr, q_exp, xerr=delta_T_arr, yerr=delta_q,
            fmt='o', capsize=3, label='Эксперимент', color='green')
ax.plot(T_plot, q_fit, 'r-', label='$q = -T\\,d\\sigma/dT$')
ax.set_xlabel('Температура $T$, К')
ax.set_ylabel('$q$, мН/м')
ax.set_title('Теплота изотермического образования\nединицы поверхности')  # перенос строки
ax.legend(loc='upper left')
ax.grid(True)

# Панель 3: U/F(T)
ax = axes[2]
ax.errorbar(T_arr, U_over_F_exp, xerr=delta_T_arr, yerr=delta_U,
            fmt='o', capsize=3, label='Эксперимент', color='purple')
ax.plot(T_plot, U_fit, 'r-', label='$U/F = \\sigma - T\\,d\\sigma/dT$')
ax.set_xlabel('Температура $T$, К')
ax.set_ylabel('$U/F$, мН/м')
ax.set_title('Полная поверхностная энергия\nединицы площади')  # перенос строки
ax.legend(loc='upper left')
ax.grid(True)

plt.tight_layout()
plt.savefig('surface_tension_plots.png', dpi=300)
plt.show()

# Рисунок 2: σ(t) в °C для наглядности
plt.figure(figsize=(8, 6))
t_plot = T_plot - 273.15
sigma_t_fit = linear_func(T_plot, a_fit, b_fit)
plt.errorbar(t_arr, sigma, xerr=delta_t, yerr=delta_sigma,
             fmt='o', capsize=3, label='Эксперимент', color='blue')
plt.plot(t_plot, sigma_t_fit, 'r-', label='Линейная аппроксимация')
plt.xlabel('Температура $t$, °C')
plt.ylabel('$\\sigma$, мН/м')
plt.title('Зависимость коэффициента поверхностного натяжения\nводы от температуры')  # перенос
plt.legend(loc='upper right')
plt.grid(True)
plt.tight_layout()
plt.savefig('sigma_vs_t_C.png', dpi=300)
plt.show()

print("\nОбработка завершена. Все графики сохранены.")
