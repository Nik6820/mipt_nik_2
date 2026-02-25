import matplotlib.pyplot as plt
import numpy as np

# Данные для трубки 1 (кумулятивные длина и перепад давления)
l1 = [10.7, 40.7, 80.7, 130.7]
dp1 = [17, 32, 47, 67]

# Данные для трубки 2
l2 = [11, 31, 61]
dp2 = [72, 56 + 72, 60 + 56 + 72]  # = [72, 128, 188]

# Данные для трубки 3
l3 = [10.9, 40.9, 80.9, 130.9]
dp3 = [24, 29 + 24, 38 + 29 + 24, 45 + 38 + 29 + 24]  # = [24, 53, 91, 136]

def plot_with_regression(l, dp, title, xlabel, ylabel, color, marker_style):
    """
    Строит отдельный график: точки (без линий) и аппроксимирующую прямую по МНК.
    """
    # Расчёт коэффициентов линейной регрессии
    coeffs = np.polyfit(l, dp, 1)
    a, b = coeffs
    print(f"{title}: ΔP = {a:.4f} * l + {b:.4f}")

    # Создание нового рисунка
    plt.figure()
    # Экспериментальные точки (только маркеры, без соединительных линий)
    plt.plot(l, dp, marker_style, color=color, markersize=8, linestyle='', label='Эксперимент')
    # Линия регрессии
    l_fit = np.linspace(min(l), max(l), 100)
    dp_fit = a * l_fit + b
    plt.plot(l_fit, dp_fit, '--', color=color, linewidth=2,
             label=f'МНК: P = {a:.2f}·l + {b:.2f}')
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(title)
    plt.grid(True)

    plt.tight_layout()
    plt.show()

# Построение трёх отдельных графиков (точки без ломаных линий)
plot_with_regression(l1, dp1,
                     'Трубка 1 (d₁ = 5.1 мм), Q = 2.55 л/мин',
                     'l, см', 'P, дел', 'blue', 'o')

plot_with_regression(l2, dp2,
                     'Трубка 2 (d₂ = 3.95 мм), Q = 2.55 л/мин',
                     'l, см', 'P, дел', 'red', 's')

plot_with_regression(l3, dp3,
                     'Трубка 3 (d₃ = 3.0 мм), Q = 3.30 л/мин',
                     'l, см', 'P, дел', 'green', '^')
