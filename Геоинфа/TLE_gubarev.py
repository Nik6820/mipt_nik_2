import matplotlib.pyplot as plt
import numpy as np
from skyfield.api import EarthSatellite, load, wgs84

# Шкала времени
ts = load.timescale()

# TLE спутника NOAA 19
l1 = '1 33591U 09005A   26055.21485026  .00000032  00000-0  40752-4 0  9998'
l2 = '2 33591  98.9636 125.9615 0013475 354.3600   5.7419 14.13453966878522'
sat = EarthSatellite(l1, l2, 'NOAA19', ts)

# Наблюдатель в Долгопрудном
loc = wgs84.latlon(55.93021167610939, 37.51823395650721)

# Поиск восходов и заходов с 1 января по 1 марта (включительно) 2026
t1 = ts.utc(2026, 1, 1)
t2 = ts.utc(2026, 3, 2)
t_ev, ev = sat.find_events(loc, t1, t2, 0)

# Вывод происходит временным массивом и целочисленными кодами:
ev_names = ('above ', 'culminate', 'below ')
fmt = '%Y %b %d %H:%M:%S'
for ti, code in zip(t_ev, ev):
    if code == 0:
        line = ev_names[code] + ti.utc_strftime(fmt)
    if code == 2:
        line += " " + ev_names[code] + ti.utc_strftime(fmt)
        print(line)

#Построение трассы над горизонтом 1–3 января (включительно) 2026
diff = sat - loc
t3 = ts.utc(2026, 1, 1)
t4 = ts.utc(2026, 1, 4)
times = ts.linspace(t3, t4, 10000)

az, alt = [], []
for ti in times:
    topo = diff.at(ti)
    el, a, mess = topo.altaz()
    if el.degrees > 0:
        az.append(a.degrees)
        alt.append(el.degrees)

# Полярный график
fig, ax = plt.subplots(subplot_kw={'projection': 'polar'})
ax.set_theta_zero_location('N')
ax.set_theta_direction(-1)
ax.set_ylim(90, 0)
ax.set_yticks(range(0, 91, 30))
ax.plot(np.radians(az), alt, lw=1, color='black')
ax.set_title('Полярный график пролета спутника над Долгопрудным', fontsize=10)
plt.show()