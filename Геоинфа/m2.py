import numpy as np
import matplotlib.pyplot as plt

class OrbitalSimulator:
    def __init__(self, semi_major_axis, initial_velocity, body_name="Тело", mu=1.32712440018e20):
        """
        Упрощенный орбитальный симулятор
        
        Параметры:
        semi_major_axis: большая полуось (м)
        initial_velocity: начальная скорость (м/с)
        body_name: название тела
        mu: гравитационный параметр Солнца (м³/с²)
        """
        self.a = semi_major_axis
        self.v0 = initial_velocity
        self.mu = mu
        self.body_name = body_name
        
        # Начальное положение (перигелий)
        self.r0 = self.a  # начальное расстояние от Солнца
        
        # Расчет параметров орбиты
        self.calculate_orbital_parameters()
        
        # Вывод информации
        print(f"Параметры орбиты для {body_name}:")
        print(f"  Большая полуось: {self.a:.3e} м")
        print(f"  Начальная скорость: {self.v0:.2f} м/с")
        print(f"  Эксцентриситет: {self.e:.6f}")
        print(f"  Орбитальный период: {self.T/86400:.2f} дней")
        print(f"  Минимальное расстояние: {self.r_min:.3e} м")
        print(f"  Максимальное расстояние: {self.r_max:.3e} м")
    
    def calculate_orbital_parameters(self):
        """Вычисление орбитальных параметров"""
        # Энергия и угловой момент
        E = self.v0**2/2 - self.mu/self.r0
        h = self.r0 * self.v0
        
        # Большая полуось и эксцентриситет
        self.a = -self.mu/(2*E)
        self.e = np.sqrt(1 + 2*E*h**2/self.mu**2)
        
        # Период по третьему закону Кеплера
        self.T = 2*np.pi*np.sqrt(self.a**3/self.mu)
        
        # Минимальное и максимальное расстояние
        self.r_min = self.a*(1 - self.e)
        self.r_max = self.a*(1 + self.e)
    
    def calculate_orbit(self, time_points=1000, num_periods=1):
        """Вычисление орбиты для заданного времени"""
        self.time = np.linspace(0, num_periods*self.T, time_points)
        
        # Инициализация массивов
        self.r_values = np.zeros(len(self.time))  # расстояния
        self.v_values = np.zeros(len(self.time))  # скорости
        self.a_values = np.zeros(len(self.time))  # ускорения
        self.x_values = np.zeros(len(self.time))  # координата x
        self.y_values = np.zeros(len(self.time))  # координата y
        
        # Для каждого момента времени решаем уравнение Кеплера
        for i, t in enumerate(self.time):
            # Средняя аномалия
            M = 2*np.pi*t/self.T
            
            # Решение уравнения Кеплера M = E - e*sin(E) методом Ньютона
            E = M  # начальное приближение
            for _ in range(20):  # итерации Ньютона
                delta = (E - self.e*np.sin(E) - M)/(1 - self.e*np.cos(E))
                E -= delta
                if abs(delta) < 1e-12:
                    break
            
            # Истинная аномалия
            nu = 2*np.arctan(np.sqrt((1+self.e)/(1-self.e))*np.tan(E/2))
            
            # Расстояние
            r = self.a*(1 - self.e**2)/(1 + self.e*np.cos(nu))
            self.r_values[i] = r
            
            # Координаты (в плоскости орбиты)
            self.x_values[i] = r*np.cos(nu)
            self.y_values[i] = r*np.sin(nu)
            
            # Скорость (из закона сохранения энергии)
            v = np.sqrt(2*(self.mu/r + self.v0**2/2 - self.mu/self.r0))
            self.v_values[i] = v
            
            # Ускорение (из закона всемирного тяготения)
            self.a_values[i] = self.mu/r**2
    
    def plot_results(self):
        """Построение графиков результатов"""
        if not hasattr(self, 'time'):
            self.calculate_orbit()
        
        fig, axes = plt.subplots(2, 2, figsize=(12, 10))
        
        # 1. Орбита в плоскости XY
        ax1 = axes[0, 0]
        ax1.plot(self.x_values, self.y_values, 'b-', linewidth=1)
        ax1.plot(0, 0, 'yo', markersize=15, label='Солнце')
        ax1.plot(self.x_values[0], self.y_values[0], 'ro', label='Начало')
        ax1.set_xlabel('X (м)')
        ax1.set_ylabel('Y (м)')
        ax1.set_title(f'Орбита {self.body_name}')
        ax1.grid(True, alpha=0.3)
        ax1.legend()
        ax1.axis('equal')
        
        # 2. Расстояние от Солнца от времени
        ax2 = axes[0, 1]
        ax2.plot(self.time/86400, self.r_values, 'g-', linewidth=1)
        ax2.set_xlabel('Время (дни)')
        ax2.set_ylabel('Расстояние от Солнца (м)')
        ax2.set_title('Расстояние от времени')
        ax2.grid(True, alpha=0.3)
        
        # 3. Скорость от времени
        ax3 = axes[1, 0]
        ax3.plot(self.time/86400, self.v_values, 'r-', linewidth=1)
        ax3.set_xlabel('Время (дни)')
        ax3.set_ylabel('Скорость (м/с)')
        ax3.set_title('Скорость от времени')
        ax3.grid(True, alpha=0.3)
        
        # 4. Ускорение от времени
        ax4 = axes[1, 1]
        ax4.plot(self.time/86400, self.a_values, 'purple', linewidth=1)
        ax4.set_xlabel('Время (дни)')
        ax4.set_ylabel('Ускорение (м/с²)')
        ax4.set_title('Ускорение от времени')
        ax4.grid(True, alpha=0.3)
        
        plt.suptitle(f'Движение тела "{self.body_name}" вокруг Солнца', fontsize=14)
        plt.tight_layout()
        plt.show()
    
    def create_animation(self, num_periods=1, interval=50):
        """Простая анимация движения по орбите"""
        if not hasattr(self, 'time'):
            self.calculate_orbit(num_periods=num_periods)
        
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
        
        # Левая панель: орбита
        ax1.plot(self.x_values, self.y_values, 'b-', linewidth=0.5, alpha=0.5)
        ax1.plot(0, 0, 'yo', markersize=20, label='Солнце')
        body_orbit = ax1.plot([], [], 'ro', markersize=8)[0]
        trail = ax1.plot([], [], 'r-', linewidth=1, alpha=0.7)[0]
        ax1.set_xlabel('X (м)')
        ax1.set_ylabel('Y (м)')
        ax1.set_title('Орбита')
        ax1.grid(True, alpha=0.3)
        ax1.axis('equal')
        ax1.legend()
        
        # Правая панель: графики
        ax2_velocity, = ax2.plot([], [], 'r-', label='Скорость')
        ax2_distance, = ax2.plot([], [], 'g-', label='Расстояние')
        ax2.set_xlabel('Время (дни)')
        ax2.set_ylabel('Величина')
        ax2.set_title('Параметры движения')
        ax2.grid(True, alpha=0.3)
        ax2.legend()
        ax2.set_xlim(0, num_periods*self.T/86400)
        ax2.set_ylim(0, max(np.max(self.v_values), np.max(self.r_values))*1.1)
        
        def init():
            body_orbit.set_data([], [])
            trail.set_data([], [])
            ax2_velocity.set_data([], [])
            ax2_distance.set_data([], [])
            return body_orbit, trail, ax2_velocity, ax2_distance
        
        def update(frame):
            # Обновление позиции на орбите
            body_orbit.set_data(self.x_values[frame], self.y_values[frame])
            
            # Обновление следа
            start = max(0, frame - 50)
            trail.set_data(self.x_values[start:frame], self.y_values[start:frame])
            
            # Обновление графиков
            current_time = self.time[:frame+1]/86400
            ax2_velocity.set_data(current_time, self.v_values[:frame+1])
            ax2_distance.set_data(current_time, self.r_values[:frame+1])
            
            return body_orbit, trail, ax2_velocity, ax2_distance
        
        from matplotlib.animation import FuncAnimation
        ani = FuncAnimation(fig, update, frames=len(self.time), 
                          init_func=init, blit=True, interval=interval)
        
        plt.tight_layout()
        plt.show()
        return ani


# Пример использования
if __name__ == "__main__":
    # Пример 1: Земля
    print("Пример 1: Орбита Земли")
    earth = OrbitalSimulator(
        semi_major_axis=1.496e11,  # 1 астрономическая единица
        initial_velocity=29780,    # Орбитальная скорость Земли
        body_name="Земля"
    )
    earth.calculate_orbit(num_periods=2)  # 2 орбитальных периода
    earth.plot_results()
    
    # Пример 2: Произвольное тело с пользовательскими параметрами
    print("\n" + "="*50)
    print("Расчет для пользовательских параметров:")
    print("="*50)
    
    try:
        a_input = input("Введите большую полуось в метрах (по умолчанию 1.496e11): ")
        v_input = input("Введите начальную скорость в м/с (по умолчанию 30000): ")
        name_input = input("Введите название тела (по умолчанию 'Тело'): ")
        
        a = float(a_input) if a_input else 1.496e11
        v0 = float(v_input) if v_input else 30000
        name = name_input if name_input else "Тело"
        
        custom_body = OrbitalSimulator(
            semi_major_axis=a,
            initial_velocity=v0,
            body_name=name
        )
        
        custom_body.calculate_orbit(num_periods=1)
        custom_body.plot_results()
        
        # Вопрос об анимации
        animate = input("Показать анимацию движения? (да/нет): ").lower()
        if animate in ['да', 'д', 'y', 'yes']:
            custom_body.create_animation(num_periods=1, interval=30)
            
    except ValueError:
        print("Ошибка ввода. Используются значения по умолчанию.")
        
        # Тело со значениями по умолчанию
        default_body = OrbitalSimulator(
            semi_major_axis=1.496e11,
            initial_velocity=30000,
            body_name="Тело по умолчанию"
        )
        default_body.calculate_orbit()
        default_body.plot_results()