import numpy as np
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import messagebox

# Función que implementa el método de Runge-Kutta de segundo orden
def runge_kutta_2nd_order(f, y0, t0, tf, h):
    t_values = np.arange(t0, tf, h)  # Valores de tiempo
    y_values = [y0]  # Lista para almacenar los valores de y
    iterations = len(t_values) - 1  # Número de iteraciones

    for i in range(iterations):
        t = t_values[i]
        y = y_values[i]
        k1 = h * f(t, y)  # Primer paso
        k2 = h * f(t + h, y + k1)  # Segundo paso
        y_next = y + (k1 + k2) / 2  # Valor siguiente
        y_values.append(y_next)  # Agregar el nuevo valor a la lista

    return t_values, y_values, iterations

# Función para resolver la ecuación y graficar el resultado
def solve_and_plot():
    try:
        # Obtener los parámetros de la interfaz
        equation = eval(equation_entry.get())  # La ecuación debe ser una función
        y0 = float(y0_entry.get())
        t0 = float(t0_entry.get())
        tf = float(tf_entry.get())
        h = float(h_entry.get())

        # Definir la función a resolver
        def f(t, y):
            return equation(t, y)

        # Llamar al método de Runge-Kutta
        t_values, y_values, iterations = runge_kutta_2nd_order(f, y0, t0, tf, h)

        # Graficar los resultados
        plt.plot(t_values, y_values, label='Solución RK2')
        plt.xlabel('Tiempo')
        plt.ylabel('y(t)')
        plt.title('Solución de la Ecuación Diferencial')
        plt.legend()
        plt.grid()
        plt.show()

        # Mostrar el número de iteraciones
        messagebox.showinfo("Resultado", f"Se realizaron {iterations} iteraciones.")

    except Exception as e:
        messagebox.showerror("Error", str(e))

# Crear la interfaz gráfica
root = tk.Tk()
root.title("Solver de Ecuaciones Diferenciales - RK2")

# Entradas para los parámetros
tk.Label(root, text="Ecuación (como función de t y y):").pack()
equation_entry = tk.Entry(root)
equation_entry.pack()

tk.Label(root, text="Valor inicial y0:").pack()
y0_entry = tk.Entry(root)
y0_entry.pack()

tk.Label(root, text="Tiempo inicial t0:").pack()
t0_entry = tk.Entry(root)
t0_entry.pack()

tk.Label(root, text="Tiempo final tf:").pack()
tf_entry = tk.Entry(root)
tf_entry.pack()

tk.Label(root, text="Paso h:").pack()
h_entry = tk.Entry(root)
h_entry.pack()

# Botón para resolver la ecuación
solve_button = tk.Button(root, text="Resolver y Graficar", command=solve_and_plot)
solve_button.pack()

# Iniciar la interfaz
root.mainloop()