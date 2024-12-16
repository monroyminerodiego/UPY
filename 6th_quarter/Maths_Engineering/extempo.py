# Importamos las bibliotecas necesarias
import numpy as np
import matplotlib.pyplot as plt

# Definimos la función de la ecuación diferencial (ejemplo: dy/dx = f(x, y))
def f(x, y):
    return 4 * np.log(x**2 + y**2) - np.cos(x) # Ecuación específica para este ejemplo

# Método de Euler
def euler_method(f, x0, y0, x_end, h):
    n_steps = int((x_end - x0) / h)  # Número de pasos
    x_vals = [x0]
    y_vals = [y0]

    for _ in range(n_steps):
        y_next = y_vals[-1] + h * f(x_vals[-1], y_vals[-1])  # Fórmula de Euler
        x_next = x_vals[-1] + h

        x_vals.append(x_next)
        y_vals.append(y_next)

    return np.array(x_vals), np.array(y_vals)

# Método de Runge-Kutta de segundo orden
def runge_kutta_2(f, x0, y0, x_end, h):
    n_steps = int((x_end - x0) / h)  # Número de pasos
    x_vals = [x0]
    y_vals = [y0]

    for _ in range(n_steps):
        x_curr = x_vals[-1]
        y_curr = y_vals[-1]

        k1 = f(x_curr, y_curr)  # Pendiente inicial
        k2 = f(x_curr + h, y_curr + h * k1)  # Pendiente al siguiente punto

        y_next = y_curr + (h / 2) * (k1 + k2)  # Promedio de pendientes
        x_next = x_curr + h

        x_vals.append(x_next)
        y_vals.append(y_next)

    return np.array(x_vals), np.array(y_vals)

# Solución exacta (si se conoce, para comparar)
def exact_solution(x):
    return np.exp(0.1 * (x**2 - 1))  # Solución exacta para esta ecuación diferencial

# Configuración inicial
x0 = 1   # Valor inicial de x
y0 = 1   # Valor inicial de y
x_end = 2  # Valor final de x
h = 0.05   # Tamaño del paso

# Llamamos a los métodos
x_euler, y_euler = euler_method(f, x0, y0, x_end, h)
# x_rk2, y_rk2 = runge_kutta_2(f, x0, y0, x_end, h)

# Valores exactos para graficar
x_exact = np.linspace(x0, x_end, 1000)
y_exact = exact_solution(x_exact)

# Tabulación de resultados
print("\nResultados Tabulados:\n")
print(f"{'x':<10}{'y (Euler)':<15}")
for i in range(len(x_euler)):
    y_exact_val = exact_solution(x_euler[i])
    print(f"{x_euler[i]:<10.5f}{y_euler[i]:<15.5f}{y_exact_val:<15.5f}")

# Visualización de resultados
plt.figure(figsize=(10, 6))
plt.plot(x_euler, y_euler, label='Euler', marker='o', linestyle='--')
# plt.plot(x_rk2, y_rk2, label='Runge-Kutta 2', marker='x', linestyle='--')
plt.plot(x_exact, y_exact, label='Solución Exacta', color='black', linewidth=1.5)
plt.title('Solución de la ecuación diferencial')
plt.xlabel('x')
plt.ylabel('y')
plt.legend()
plt.grid()
plt.show()

