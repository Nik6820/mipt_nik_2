

import matplotlib.pyplot as plt
import numpy as np
from skyfield.api import load, wgs84, EarthSatellite

ts = load.timescale()

t_start = ts.utc(2026, 1, 1)
t_end = ts.utc(2026, 3, 1)


line1 = '1 33591U 09005A   26055.21485026  .00000032  00000-0  40752-4 0  9998'
line2 = '2 33591  98.9636 125.9615 0013475 354.3600   5.7419 14.13453966878522'

satellite = EarthSatellite(line1, line2, 'NOAA19', ts)

dolgoprudny = wgs84.latlon(+55.9496, +37.5018)

t, events = satellite.find_events(dolgoprudny, t_start, t_end, altitude_degrees=0)
event_names = 'above ', 'culminate', 'below '
for ti, event in zip(t, events):
    if event == 0:
        ans = event_names[event] + ti.utc_strftime('%Y %b %d %H:%M:%S')

    if event == 2:
        ans = ans +" "+ event_names[event] + ti.utc_strftime('%Y %b %d %H:%M:%S')
        print(ans)

difference = satellite - dolgoprudny

t_start = ts.utc(2026, 1, 1)
t_end = ts.utc(2026, 1, 3)


times = ts.linspace(t_start, t_end, 10000)

azimuts = []
altitudes = []

for t in times:
    topocentric = difference.at(t)
    alt, az, distance = topocentric.altaz()
    if alt.degrees > 0:
        azimuts.append(az.degrees)
        altitudes.append(alt.degrees)

fig, ax = plt.subplots(subplot_kw={'projection': 'polar'})
ax.set_theta_zero_location('N')
ax.set_theta_direction(-1)
ax.set_ylim(90, 0)
ax.set_yticks(range(0, 91, 30))

ax.plot(np.radians(azimuts), altitudes, linewidth=1)
plt.show()