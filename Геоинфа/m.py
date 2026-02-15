import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from scipy.integrate import solve_ivp

class OrbitalSimulator:
    def __init__(self, semi_major_axis, initial_velocity=None, eccentricity=None, 
                 body_name="Тело", mu=1.32712440018e20):
        """
        Инициализация орбитального симулятора
        
        Параметры:
        semi_major_axis: большая полуось (м)
        initial_velocity: начальная скорость (м/с) - тангенциальная в перигелии
        eccentricity: эксцентриситет орбиты (0-1)
        body_name: название тела
        mu: гравитационный параметр (м³/с²) для Солнца
        """
        self.semi_major_axis = semi_major_axis
        self.mu = mu
        self.body_name = body_name
        
        # Если задана начальная скорость, вычисляем эксцентриситет
        if initial_velocity is not None:
            r_peri = semi_major_axis  # Предполагаем, что начальная позиция - перигелий
            h = r_peri * initial_velocity  # Удельный угловой момент
            energy = initial_velocity**2 / 2 - mu / r_peri
            self.eccentricity = np.sqrt(1 + 2 * energy * h**2 / mu**2)
        elif eccentricity is not None:
            self.eccentricity = eccentricity
            # Вычисляем скорость в перигелии
            r_peri = semi_major_axis * (1 - eccentricity)
            v_peri = np.sqrt(mu * (2/r_peri - 1/semi_major_axis))
        else:
            self.eccentricity = 0.0  # Круговая орбита по умолчанию
        
        # Орбитальные параметры
        self.period = 2 * np.pi * np.sqrt(semi_major_axis**3 / mu)  # Период по 3-му закону Кеплера
        
        print(f"Параметры орбиты для {body_name}:")
        print(f"  Большая полуось: {semi_major_axis:.3e} м")
        print(f"  Эксцентриситет: {self.eccentricity:.6f}")
        print(f"  Орбитальный период: {self.period/86400:.2f} дней")
        if initial_velocity is not None:
            print(f"  Начальная скорость: {initial_velocity:.2f} м/с")
        
    def orbital_elements_to_state(self, true_anomaly):
        """Преобразование орбитальных элементов в вектор состояния"""
        # Параметры орбиты
        a = self.semi_major_axis
        e = self.eccentricity
        mu = self.mu
        
        # Расстояние до фокуса
        r = a * (1 - e**2) / (1 + e * np.cos(true_anomaly))
        
        # Положение в орбитальной плоскости
        x_orb = r * np.cos(true_anomaly)
        y_orb = r * np.sin(true_anomaly)
        
        # Скорость в орбитальной плоскости
        h = np.sqrt(mu * a * (1 - e**2))  # Удельный угловой момент
        v_r = (mu / h) * e * np.sin(true_anomaly)  # Радиальная скорость
        v_theta = (mu / h) * (1 + e * np.cos(true_anomaly))  # Тангенциальная скорость
        
        vx_orb = v_r * np.cos(true_anomaly) - v_theta * np.sin(true_anomaly)
        vy_orb = v_r * np.sin(true_anomaly) + v_theta * np.cos(true_anomaly)
        
        return np.array([x_orb, y_orb, 0]), np.array([vx_orb, vy_orb, 0])
    
    def equations_of_motion(self, t, y):
        """Уравнения движения для интегрирования"""
        r = y[:3]
        v = y[3:]
        r_norm = np.linalg.norm(r)
        acceleration = -self.mu * r / r_norm**3
        return np.concatenate([v, acceleration])
    
    def simulate(self, t_span, n_points=1000):
        """Моделирование движения с численным интегрированием"""
        # Начальные условия (в перигелии)
        r0, v0 = self.orbital_elements_to_state(0)
        y0 = np.concatenate([r0, v0])
        
        # Интегрирование уравнений движения
        sol = solve_ivp(
            self.equations_of_motion,
            [0, t_span],
            y0,
            method='RK45',
            t_eval=np.linspace(0, t_span, n_points),
            rtol=1e-9,
            atol=1e-12
        )
        
        self.t = sol.t
        self.r = sol.y[:3].T
        self.v = sol.y[3:].T
        
        return self.t, self.r, self.v
    
    def plot_orbit(self, t_span=None):
        """Визуализация орбиты"""
        if not hasattr(self, 'r'):
            if t_span is None:
                t_span = self.period
            self.simulate(t_span)
        
        fig, axes = plt.subplots(2, 2, figsize=(12, 10))
        
        # Орбита в плоскости XY
        ax1 = axes[0, 0]
        ax1.plot(self.r[:, 0], self.r[:, 1], 'b-', linewidth=1, alpha=0.7)
        ax1.plot(0, 0, 'yo', markersize=15, label='Солнце')
        ax1.plot(self.r[0, 0], self.r[0, 1], 'ro', label='Начало')
        ax1.set_xlabel('X (м)')
        ax1.set_ylabel('Y (м)')
        ax1.set_title(f'Орбита {self.body_name}')
        ax1.grid(True, alpha=0.3)
        ax1.axis('equal')
        ax1.legend()
        
        # Расстояние от Солнца
        ax2 = axes[0, 1]
        distances = np.linalg.norm(self.r, axis=1)
        ax2.plot(self.t/86400, distances, 'g-')
        ax2.set_xlabel('Время (дни)')
        ax2.set_ylabel('Расстояние от Солнца (м)')
        ax2.set_title('Расстояние от Солнца')
        ax2.grid(True, alpha=0.3)
        
        # Скорость
        ax3 = axes[1, 0]
        speeds = np.linalg.norm(self.v, axis=1)
        ax3.plot(self.t/86400, speeds, 'r-')
        ax3.set_xlabel('Время (дни)')
        ax3.set_ylabel('Скорость (м/с)')
        ax3.set_title('Скорость тела')
        ax3.grid(True, alpha=0.3)
        
        # Энергия (должна сохраняться)
        ax4 = axes[1, 1]
        kinetic = 0.5 * np.linalg.norm(self.v, axis=1)**2
        potential = -self.mu / np.linalg.norm(self.r, axis=1)
        total_energy = kinetic + potential
        ax4.plot(self.t/86400, total_energy, 'purple')
        ax4.set_xlabel('Время (дни)')
        ax4.set_ylabel('Удельная энергия (м²/с²)')
        ax4.set_title('Сохраняющаяся полная энергия')
        ax4.grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.show()
    
    def animate_orbit(self, t_span=None, interval=50):
        """Анимация движения по орбите"""
        if not hasattr(self, 'r'):
            if t_span is None:
                t_span = self.period
            self.simulate(t_span)
        
        fig, ax = plt.subplots(figsize=(10, 10))
        
        # Орбита
        ax.plot(self.r[:, 0], self.r[:, 1], 'b-', linewidth=0.5, alpha=0.5)
        
        # Солнце
        sun = ax.plot(0, 0, 'yo', markersize=20, label='Солнце')[0]
        
        # Тело
        body = ax.plot([], [], 'ro', markersize=8, label=self.body_name)[0]
        trail = ax.plot([], [], 'r-', linewidth=1, alpha=0.7)[0]
        
        ax.set_xlabel('X (м)')
        ax.set_ylabel('Y (м)')
        ax.set_title(f'Орбита {self.body_name}')
        ax.grid(True, alpha=0.3)
        ax.axis('equal')
        ax.legend()
        
        # Пределы графика
        max_range = np.max(np.abs(self.r)) * 1.1
        ax.set_xlim(-max_range, max_range)
        ax.set_ylim(-max_range, max_range)
        
        def init():
            body.set_data([], [])
            trail.set_data([], [])
            return body, trail
        
        def update(frame):
            # Обновление позиции тела
            body.set_data(self.r[frame, 0], self.r[frame, 1])
            
            # Обновление следа (последние 100 точек)
            start = max(0, frame - 100)
            trail.set_data(self.r[start:frame, 0], self.r[start:frame, 1])
            
            # Информация в заголовке
            speed = np.linalg.norm(self.v[frame])
            distance = np.linalg.norm(self.r[frame])
            ax.set_title(f'{self.body_name} - Время: {self.t[frame]/86400:.1f} дней, '
                        f'Скорость: {speed:.1f} м/с, '
                        f'Расстояние: {distance:.3e} м')
            
            return body, trail
        
        ani = FuncAnimation(fig, update, frames=len(self.t),
                          init_func=init, blit=True, interval=interval)
        
        plt.show()
        return ani


# Пример использования
if __name__ == "__main__":
    # Пример 1: Земля (круговая орбита)
    earth_sim = OrbitalSimulator(
        semi_major_axis=1.496e11,  # 1 а.е.
        initial_velocity=29780,    # Орбитальная скорость Земли
        body_name="Земля"
    )
    
    # Моделирование на 2 года
    earth_sim.simulate(earth_sim.period * 2)
    
    # Построение графиков
    earth_sim.plot_orbit()
    
    # Пример 2: Комета с высоким эксцентриситетом
    comet_sim = OrbitalSimulator(
        semi_major_axis=3.0e12,     # ~20 а.е.
        eccentricity=0.9,           # Высокий эксцентриситет
        body_name="Комета"
    )
    
    # Анимация движения кометы
    comet_sim.animate_orbit(comet_sim.period, interval=30)
    
    # Пример 3: Пользовательское тело
    print("\n" + "="*50)
    print("Расчет для пользовательских параметров:")
    print("="*50)
    
    # Ввод пользовательских параметров
    try:
        a = float(input("Введите большую полуось (м): ") or "1.496e11")
        v0 = float(input("Введите начальную скорость (м/с): ") or "30000")
        name = input("Введите название тела: ") or "Пользовательское тело"
        
        custom_sim = OrbitalSimulator(
            semi_major_axis=a,
            initial_velocity=v0,
            body_name=name
        )
        
        # Моделирование на один период
        custom_sim.simulate(custom_sim.period)
        custom_sim.plot_orbit()
        
    except ValueError:
        print("Ошибка ввода. Используются значения по умолчанию.")