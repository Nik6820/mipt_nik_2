import matplotlib.pyplot as plt
import numpy as np

# Данные
Q1 = [0.60, 1.41, 2.13, 2.94, 3.63, 4.38, 4.80, 5.60, 6.00, 6.40, 7.02, 8.40, 9.00, 9.51, 10.05, 10.74, 11.49, 12.84]
P1 = [3, 6, 9, 12, 15, 18, 20, 25, 30, 35, 40, 50, 60, 70, 80, 90, 100, 110]

Q2 = [0.38, 0.63, 0.90, 1.14, 1.32, 1.56, 1.77, 2.22, 2.55, 2.82, 3.06, 3.42, 3.68, 3.92, 4.12, 4.32, 4.50]
P2 = [10, 15, 20, 25, 30, 35, 40, 50, 60, 70, 80, 90, 100, 110, 120, 130, 140]

Q3 = [0.66, 1.05, 1.47, 1.83, 2.22, 2.58, 2.97, 3.66, 4.44, 5.04, 5.61, 6.00, 6.24, 6.42]
P3 = [10, 15, 20, 25, 30, 35, 40, 50, 60, 70, 80, 90, 100, 110]

# Погрешности
sigma_Q = 0.03  # л/мин
sigma_P = 1     # деление

# Цвета и маркеры
colors = ['blue', 'red', 'green']
markers = ['o', 's', '^']
labels = ['Трубка 1 (d=5.1 мм)', 'Трубка 2 (d=3.95 мм)', 'Трубка 3 (d=3.0 мм)']

datasets = [(P1, Q1), (P2, Q2), (P3, Q3)]

plt.figure(figsize=(12, 8))

for i, (P, Q) in enumerate(datasets):
    # Берём первые 8 точек для ламинарного участка
    P_lam = P[:8]
    Q_lam = Q[:8]
    
    # Линейная регрессия (МНК) по первым 8 точкам
    coeffs = np.polyfit(P_lam, Q_lam, 1)
    a, b = coeffs
    print(f"{labels[i]} (ламинарный участок, 8 точек): Q = {a:.4f} * P + {b:.4f}")
    
    # Построение всех точек с погрешностями
    plt.errorbar(P, Q, xerr=sigma_P, yerr=sigma_Q,
                 fmt=markers[i], color=colors[i], capsize=3,
                 label=labels[i], markersize=5, alpha=0.7)
    
    # Построение прямой регрессии только для ламинарного участка (продлеваем на весь диапазон для наглядности)
    P_fit = np.linspace(min(P)-2, max(P)+2, 50)
    Q_fit = a * P_fit + b
    plt.plot(P_fit, Q_fit, '--', color=colors[i], linewidth=1.5, label=f'{labels[i]}')

plt.xlabel('ΔP, деления микроманометра', fontsize=16)
plt.ylabel('Q, л/мин', fontsize=16)
plt.title('Зависимость объёмного расхода от перепада давления', fontsize=16)
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.show()
