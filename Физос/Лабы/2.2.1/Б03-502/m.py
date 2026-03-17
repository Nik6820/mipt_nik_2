import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
import os

# Устанавливаем размер шрифта для всех элементов графиков
plt.rcParams.update({'font.size': 20})

# Геометрические параметры установки (из задания)
V = 775          # см³
dV = 10          # погрешность объёма, см³
L_over_S = 5.3   # 1/см
dL_over_S = 0.1  # погрешность отношения L/S, 1/см

# Константы для расчёта длины свободного пробега и сечения
k_B = 1.380649e-23      # Дж/К
R = 8.314462618         # Дж/(моль·К)
mu_He = 0.0040026       # кг/моль (молярная масса гелия)
torr_to_Pa = 133.322    # 1 торр = 133.322 Па

def process_file(filename, T):
    """
    Чтение CSV-файла с двумя столбцами: время (с), напряжение (мВ).
    Возвращает:
        time, voltage (массивы),
        tau, dtau (характерное время и его погрешность, с),
        D, dD (коэффициент диффузии и его погрешность, см²/с),
        результаты регрессии (slope, intercept, r_value)
    """
    try:
        data = pd.read_csv(filename)
    except Exception as e:
        print(f"Ошибка чтения файла {filename}: {e}")
        return None

    # Предполагаем, что первый столбец - время, второй - напряжение
    time_col = data.columns[0]
    volt_col = data.columns[1]
    time = data[time_col].values.astype(float)
    voltage = data[volt_col].values.astype(float)

    # Удаляем пропуски
    mask = ~(np.isnan(time) | np.isnan(voltage))
    time = time[mask]
    voltage = voltage[mask]

    # Для логарифмирования нужны положительные напряжения
    pos_mask = voltage > 0
    time_pos = time[pos_mask]
    voltage_pos = voltage[pos_mask]

    if len(time_pos) < 3:
        print("Недостаточно положительных значений напряжения.")
        return None

    # Полулогарифмическое преобразование
    lnV = np.log(voltage_pos)

    # Линейная регрессия: lnV = a + b*t, где b = -1/tau
    slope, intercept, r_value, p_value, std_err = stats.linregress(time_pos, lnV)

    tau = -1.0 / slope          # характеристическое время, с
    # Погрешность tau: dt/t = |ds/s|, где s = slope
    dtau = tau * (std_err / abs(slope))

    # Коэффициент диффузии: D = V * (L/S) / (2 * tau)
    D = V * L_over_S / (2 * tau)        # см²/с
    # Относительная погрешность D
    rel_err_D = np.sqrt((dV/V)**2 + (dL_over_S/L_over_S)**2 + (dtau/tau)**2)
    dD = D * rel_err_D

    # Построение графиков
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
    fig.suptitle(f'Файл: {os.path.basename(filename)}', fontsize=20)

    # График U(t)
    ax1.plot(time, voltage, 'o', markersize=5, label='Данные')
    ax1.set_xlabel('Время, с', fontsize=20)
    ax1.set_ylabel('Напряжение, мВ', fontsize=20)
    ax1.set_title('U(t)', fontsize=20)
    ax1.grid(True)
    ax1.legend(fontsize=18)
    ax1.tick_params(labelsize=18)

    # Полулогарифмический график с аппроксимацией
    ax2.semilogy(time_pos, voltage_pos, 'o', markersize=5, label='Данные (ln)')
    t_fit = np.linspace(time_pos.min(), time_pos.max(), 100)
    v_fit = np.exp(intercept) * np.exp(-t_fit / tau)
    ax2.semilogy(t_fit, v_fit, 'r-', linewidth=2, label=f'Аппроксимация: τ = {tau:.1f} с')
    ax2.set_xlabel('Время, с', fontsize=20)
    ax2.set_ylabel('Напряжение, мВ', fontsize=20)
    ax2.set_title('Полулогарифмический график', fontsize=20)
    ax2.grid(True)
    ax2.legend(fontsize=16)
    ax2.tick_params(labelsize=18)

    plt.tight_layout()
    plt.show()

    # Вывод результатов
    print(f"\nРезультаты для файла {filename}:")
    print(f"  Наклон (lnU/t) = {slope:.6f} ± {std_err:.6f} 1/с")
    print(f"  R² = {r_value**2:.4f}")
    print(f"  τ = {tau:.2f} ± {dtau:.2f} с")
    print(f"  D = {D:.4f} ± {dD:.4f} см²/с")

    return time, voltage, tau, dtau, D, dD, slope, intercept, r_value

def calculate_lambda_sigma(D, dD, P, T, dT=1.0):
    """
    Расчёт длины свободного пробега λ (мкм) и сечения σ (Å²) по D и P.
    D - в см²/с, P - в торр, T - в К.
    Возвращает λ, dλ, σ, dσ.
    """
    # Перевод D в м²/с
    D_m2 = D * 1e-4
    dD_m2 = dD * 1e-4

    # Средняя тепловая скорость атомов He
    v_mean = np.sqrt(8 * R * T / (np.pi * mu_He))   # м/с

    # Длина свободного пробега (м)
    lambda_m = 3 * D_m2 / v_mean
    # Погрешность λ (относительная погрешность D)
    dlambda_m = lambda_m * (dD_m2 / D_m2)

    # Перевод в микрометры
    lambda_um = lambda_m * 1e6
    dlambda_um = dlambda_m * 1e6

    # Концентрация фона (м⁻³)
    P_Pa = P * torr_to_Pa
    n0 = P_Pa / (k_B * T)                # м⁻³
    # Погрешность n0 (учитываем погрешность P и T)
    dP = 0.5  # предположим погрешность давления 0.5 торр (можно уточнить)
    dT_abs = dT
    dn0 = n0 * np.sqrt((dP/P)**2 + (dT_abs/T)**2)

    # Эффективное сечение (м²)
    sigma_m2 = 1 / (n0 * lambda_m)
    # Погрешность сечения (сложение погрешностей n0 и λ)
    dsigma_m2 = sigma_m2 * np.sqrt((dn0/n0)**2 + (dlambda_m/lambda_m)**2)

    # Перевод в ангстремы²
    sigma_A2 = sigma_m2 * 1e20
    dsigma_A2 = dsigma_m2 * 1e20

    return lambda_um, dlambda_um, sigma_A2, dsigma_A2

def main():
    print("Обработка данных для лабораторной работы 2.2.1")
    print("Геометрические параметры:")
    print(f"  V = {V} ± {dV} см³")
    print(f"  L/S = {L_over_S} ± {dL_over_S} 1/см\n")

    # Ввод температуры
    T_c = float(input("Введите температуру в лаборатории (°C): "))
    T = T_c + 273.15  # Кельвины

    results = []  # список кортежей (P, D, dD)

    while True:
        filename = input("Введите имя CSV-файла (или 'exit' для выхода): ").strip()
        if filename.lower() == 'exit':
            break
        if not os.path.isfile(filename):
            print("Файл не найден. Попробуйте снова.")
            continue

        res = process_file(filename, T)
        if res is None:
            continue

        # Спрашиваем, хочет ли пользователь ввести давление для этого измерения
        ans = input("Введите рабочее давление P (торр) для этого эксперимента (или пропустите, нажав Enter): ").strip()
        if ans:
            try:
                P = float(ans)
                results.append((P, res[4], res[5]))  # D, dD
            except:
                print("Некорректное значение давления, пропускаем.")

        cont = input("Обработать ещё один файл? (y/n): ").lower()
        if cont != 'y':
            break

    # Если есть данные для разных давлений, строим график D(1/P)
    if len(results) >= 2:
        results.sort()  # по возрастанию давления
        pressures = np.array([r[0] for r in results])
        D_vals = np.array([r[1] for r in results])
        D_errs = np.array([r[2] for r in results])
        invP = 1.0 / pressures

        plt.figure(figsize=(10, 8))
        plt.errorbar(invP, D_vals, yerr=D_errs, fmt='o', capsize=5, markersize=8, label='Измерения')
        plt.xlabel('1/P, 1/торр', fontsize=20)
        plt.ylabel('D, см²/с', fontsize=20)
        plt.title('Зависимость коэффициента диффузии от обратного давления', fontsize=20)
        plt.grid(True)
        plt.tick_params(labelsize=18)

        # Линейная аппроксимация (ожидается D ~ const/P)
        slope_fit, intercept_fit, r_fit, p_fit, err_fit = stats.linregress(invP, D_vals)
        fit_line = slope_fit * invP + intercept_fit
        plt.plot(invP, fit_line, 'r-', linewidth=2, label=f'Линейный fit: D = {slope_fit:.2f}/P + {intercept_fit:.2f}')
        plt.legend(fontsize=18)
        plt.show()

        # Оценка D при атмосферном давлении (760 торр)
        P_atm = 760
        D_atm = slope_fit / P_atm + intercept_fit
        print(f"\nЭкстраполяция к атмосферному давлению (P = {P_atm} торр):")
        print(f"  D(атм) ≈ {D_atm:.4f} см²/с")

    # Расчёт длины свободного пробега и сечения для всех введённых измерений
    if results:
        print("\n" + "="*60)
        print("Оценка длины свободного пробега и эффективного сечения")
        print("="*60)
        for i, (P, D, dD) in enumerate(results):
            lambda_um, dlambda_um, sigma_A2, dsigma_A2 = calculate_lambda_sigma(D, dD, P, T)
            print(f"\nИзмерение {i+1}: P = {P:.1f} торр, D = {D:.4f} ± {dD:.4f} см²/с")
            print(f"  Длина свободного пробега λ = {lambda_um:.2f} ± {dlambda_um:.2f} мкм")
            print(f"  Эффективное сечение σ = {sigma_A2:.2f} ± {dsigma_A2:.2f} Å²")

    print("\nРабота завершена.")

if __name__ == "__main__":
    main()
