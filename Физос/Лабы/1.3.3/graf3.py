import matplotlib.pyplot as plt
import numpy as np

# Исходные данные по трём трубкам
# Радиусы в мм (для логарифмического масштаба можно оставить в мм)
R_mm = np.array([2.55, 1.5, 1.975])   # трубки 1, 2, 3
l_m = np.array([0.5, 0.3, 0.5])       # длины в метрах

# Экспериментальные таблицы Q(ΔP) для каждой трубки (л/мин, ΔP в делениях)
# Трубка 1
P1 = [3, 6, 9, 12, 15, 18, 20, 25, 30, 35, 40, 50, 60, 70, 80, 90, 100, 110]
Q1 = [0.60, 1.41, 2.13, 2.94, 3.63, 4.38, 4.80, 5.60, 6.00, 6.40, 7.02, 8.40, 9.00, 9.51, 10.05, 10.74, 11.49, 12.84]

# Трубка 2
P2 = [10, 15, 20, 25, 30, 35, 40, 50, 60, 70, 80, 90, 100, 110, 120, 130, 140]
Q2 = [0.38, 0.63, 0.90, 1.14, 1.32, 1.56, 1.77, 2.22, 2.55, 2.82, 3.06, 3.42, 3.68, 3.92, 4.12, 4.32, 4.50]

# Трубка 3
P3 = [10, 15, 20, 25, 30, 35, 40, 50, 60, 70, 80, 90, 100, 110]
Q3 = [0.66, 1.05, 1.47, 1.83, 2.22, 2.58, 2.97, 3.66, 4.44, 5.04, 5.61, 6.00, 6.24, 6.42]

# Функция линейной интерполяции с экстраполяцией по двум ближайшим точкам
def interp_linear(x, xp, yp):
    if x <= xp[0]:
        # Экстраполяция влево по первым двум точкам
        x1, x2 = xp[0], xp[1]
        y1, y2 = yp[0], yp[1]
    elif x >= xp[-1]:
        # Экстраполяция вправо по последним двум точкам
        x1, x2 = xp[-2], xp[-1]
        y1, y2 = yp[-2], yp[-1]
    else:
        # Интерполяция между соседними
        idx = np.searchsorted(xp, x)
        x1, x2 = xp[idx-1], xp[idx]
        y1, y2 = yp[idx-1], yp[idx]
    return y1 + (x - x1) * (y2 - y1) / (x2 - x1)

# Заданные значения градиента давления λ (дел/м)
lam_lam = 30.0   # ламинарный режим
lam_turb = 220.0 # турбулентный режим

# Расчёт ΔP для каждой трубки
dP_lam = lam_lam * l_m
dP_turb = lam_turb * l_m

print("Ламинарный режим (λ = 30 дел/м):")
for i, (dP, tube) in enumerate(zip(dP_lam, ['Трубка1','Трубка2','Трубка3'])):
    print(f"  {tube}: ΔP = {dP:.1f} дел")

print("Турбулентный режим (λ = 220 дел/м):")
for i, (dP, tube) in enumerate(zip(dP_turb, ['Трубка1','Трубка2','Трубка3'])):
    print(f"  {tube}: ΔP = {dP:.1f} дел")

# ---- Получение Q при этих ΔP с помощью интерполяции ----
Q_lam = np.zeros(3)
Q_turb = np.zeros(3)

# Трубка 1
Q_lam[0] = interp_linear(dP_lam[0], P1, Q1)
Q_turb[0] = interp_linear(dP_turb[0], P1, Q1)

# Трубка 2
Q_lam[1] = interp_linear(dP_lam[1], P2, Q2)
Q_turb[1] = interp_linear(dP_turb[1], P2, Q2)

# Трубка 3
Q_lam[2] = interp_linear(dP_lam[2], P3, Q3)
Q_turb[2] = interp_linear(dP_turb[2], P3, Q3)

print("\nРасходы в л/мин:")
print(f"Ламинарный режим: Q_lam = {Q_lam}")
print(f"Турбулентный режим: Q_turb = {Q_turb}")

# Переводим в м³/с для согласованности? Необязательно, так как логарифмы сдвинутся, но наклон не изменится.
# Оставим в л/мин.

# ---- Построение графиков в логарифмических координатах ----
ln_R = np.log(R_mm)
ln_Q_lam = np.log(Q_lam)
ln_Q_turb = np.log(Q_turb)

# Регрессия для ламинарного режима
coeffs_lam = np.polyfit(ln_R, ln_Q_lam, 1)
beta_lam = coeffs_lam[0]
print(f"\nЛаминарный режим: β = {beta_lam:.3f} (теоретически 4)")

# Регрессия для турбулентного режима
coeffs_turb = np.polyfit(ln_R, ln_Q_turb, 1)
beta_turb = coeffs_turb[0]
print(f"Турбулентный режим: β = {beta_turb:.3f} (теоретически 2.5)")

# Графики
plt.figure(figsize=(12, 5))

plt.subplot(1, 2, 1)
plt.plot(ln_R, ln_Q_lam, 'o', markersize=8, label='Эксперимент')
ln_fit = np.linspace(min(ln_R), max(ln_R), 50)
plt.plot(ln_fit, coeffs_lam[0]*ln_fit + coeffs_lam[1], '--',
         label=f'МНК: β = {beta_lam:.2f}')
plt.xlabel('ln(R) [R в мм]')
plt.ylabel('ln(Q) [Q в л/мин]')
plt.title(f'Ламинарный режим (λ = {lam_lam} дел/м)')
plt.grid(True)
plt.legend()

plt.subplot(1, 2, 2)
plt.plot(ln_R, ln_Q_turb, 's', markersize=8, label='Эксперимент')
plt.plot(ln_fit, coeffs_turb[0]*ln_fit + coeffs_turb[1], '--',
         label=f'МНК: β = {beta_turb:.2f}')
plt.xlabel('ln(R) [R в мм]')
plt.ylabel('ln(Q) [Q в л/мин]')
plt.title(f'Турбулентный режим (λ = {lam_turb} дел/м)')
plt.grid(True)
plt.legend()

plt.tight_layout()
plt.show()

# Дополнительно: вычисление β по двум трубкам с одинаковой длиной (1 и 3, l=50 см)
print("\nПо трубкам 1 и 3 (l = 50 см):")
beta_lam_13 = np.log(Q_lam[0]/Q_lam[2]) / np.log(R_mm[0]/R_mm[2])
beta_turb_13 = np.log(Q_turb[0]/Q_turb[2]) / np.log(R_mm[0]/R_mm[2])
print(f"  Ламинарный: β = {beta_lam_13:.3f}")
print(f"  Турбулентный: β = {beta_turb_13:.3f}")

# По трубкам 2 и 3 (разные длины, но λ одинаково)
print("\nПо трубкам 2 и 3:")
beta_lam_23 = np.log(Q_lam[1]/Q_lam[2]) / np.log(R_mm[1]/R_mm[2])
beta_turb_23 = np.log(Q_turb[1]/Q_turb[2]) / np.log(R_mm[1]/R_mm[2])
print(f"  Ламинарный: β = {beta_lam_23:.3f}")
