import numpy as np
from scipy.integrate import solve_ivp
import matplotlib.pyplot as plt

# Parameterdefinitionen
m = 134  # Masse des Flugzeugs in kg
g = 9.81  # Erdbeschleunigung in m/s²
rho = 1.225  # Luftdichte in kg/m³
A = 10  # Querschnittsfläche in m²
C_D = 0.3  # Widerstandsbeiwert
C_L = 1.2  # Auftriebsbeiwert
T = np.array([2100, 0, 0])  # Schubkraft in x, y, z
collision_time = 50  # Zeitpunkt der Kollision in Sekunden
collision_force = np.array([500, 300, -1000])  # Stoßkräfte durch die Kollision in x, y, z

# Widerstands- und Auftriebskraft
def drag_force(v):
    return 0.5 * rho * v**2 * A * C_D

def lift_force(v):
    return 0.5 * rho * v**2 * A * C_L

# Differentialgleichungen
def equations(t, y):
    x, y_pos, z, v_x, v_y, v_z = y
    D_x = drag_force(v_x)
    D_y = drag_force(v_y)
    D_z = drag_force(v_z)
    L = lift_force(np.sqrt(v_x**2 + v_y**2 + v_z**2))
    
    # Hinzufügen der Stoßkräfte bei der Kollision
    if t >= collision_time:
        F_collision = collision_force
    else:
        F_collision = np.array([0, 0, 0])
    
    # Beschleunigungen berechnen
    a_x = (T[0] - D_x + F_collision[0]) / m
    a_y = (T[1] - D_y + F_collision[1]) / m
    a_z = (L - m * g - D_z + T[2] + F_collision[2]) / m
    
    return [v_x, v_y, v_z, a_x, a_y, a_z]

# Anfangswerte: Positionen und Geschwindigkeiten in x, y, z
y0 = [0, 0, 0, 50, 0, 50]  # Startposition und -geschwindigkeit

# Zeitbereich
t_span = (0, 100)  # 0 bis 100 Sekunden
t_eval = np.linspace(*t_span, 1000)

# Numerische Lösung der Differentialgleichungen
solution = solve_ivp(equations, t_span, y0, t_eval=t_eval, method='RK45')

# Plot der Ergebnisse
plt.figure(figsize=(12, 6))
plt.plot(solution.t, solution.y[2], label='Höhe (z)', color='red')
plt.plot(solution.t, solution.y[0], label='Position x', color='blue')
plt.plot(solution.t, solution.y[1], label='Position y', color='green')
plt.axvline(collision_time, color='black', linestyle='--', label='Kollisionszeitpunkt')
plt.xlabel('Zeit (s)')
plt.ylabel('Position (m)')
plt.title('Bewegung des Flugzeugs bei einer Kollision')
plt.legend()
plt.grid(True)

plt.savefig('collision_simulation.png', dpi=300)
plt.show()
