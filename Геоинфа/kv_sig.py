import numpy as np
import matplotlib.pyplot as plt

# Параметры сигнала
f = 1.0                 # частота 1 Гц
T_period = 1.0          # период
A = 1.0                 # амплитуда
n_periods = 5           # сколько периодов отображаем

# Временные параметры дискретизации
N_per_period = 256      # точек на один период (для высокого разрешения)
N_total = n_periods * N_per_period
T_total = n_periods * T_period
t = np.linspace(0, T_total, N_total, endpoint=False)
dt = t[1] - t[0]

# Генерируем меандр: +1 на первой половине каждого периода, -1 на второй
signal = A * ( (t % T_period) < (T_period/2) ) * 2 - 1  # приводит к значениям +1 и -1

# Вычисляем ДПФ
fft_vals = np.fft.fft(signal)
fft_abs = np.abs(fft_vals) / N_total * 2  # нормировка для амплитуд гармоник

# Частоты для графика (односторонний спектр)
freqs = np.fft.fftfreq(N_total, d=dt)[:N_total//2]

# Построение
plt.figure(figsize=(14, 12))

# 1. Сигнал
plt.subplot(3, 2, 1)
plt.plot(t, signal, 'b-', linewidth=1)
plt.title(f'Периодический прямоугольный сигнал (меандр) {n_periods} периодов')
plt.xlabel('Время, с')
plt.ylabel('Амплитуда')
plt.grid(True)
plt.xlim(0, T_total)
plt.ylim(-1.2, 1.2)

# 2. Спектр
plt.subplot(3, 2, 2)
plt.stem(freqs[:50], fft_abs[:50], basefmt=" ", linefmt='r-', markerfmt='ro')
plt.title('Амплитудный спектр (первые 50 гармоник)')
plt.xlabel('Частота, Гц')
plt.ylabel('Амплитуда')
plt.grid(True)
plt.xlim(0, 20)

# Восстановление по первым гармоникам
K_list = [1, 3, 5, 15]  # количество сохраняемых положительных гармоник
for idx, K in enumerate(K_list):
    fft_trunc = fft_vals.copy()
    # Оставляем только первые K положительных частот и соответствующие отрицательные
    fft_trunc[K:N_total-K] = 0
    recon = np.fft.ifft(fft_trunc).real
    
    plt.subplot(3, 2, 3 + idx)
    plt.plot(t, signal, 'k--', linewidth=1, alpha=0.5, label='Исходный')
    plt.plot(t, recon, 'r', linewidth=1.5, label=f'{K} гармоник')
    plt.title(f'Восстановление по первым {K} гармоникам')
    plt.xlabel('Время, с')
    plt.ylabel('Амплитуда')
    plt.grid(True)
    plt.xlim(0, T_total)
    plt.ylim(-1.5, 1.5)
    plt.legend()

plt.tight_layout()
plt.show()
