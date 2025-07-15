import numpy as np
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import messagebox

# Función que implementa el método de Runge-Kutta de segundo orden
def runge_kutta_2nd_order(f, y0, t0, t_end, h):
    t_values = np.arange(t0, t_end+h, h)  # Valores de tiempo
    y_values = [y0]  # Lista para almacenar los valores de y
    iterations = int((t_end - t0) / h)  # Número de iteraciones

    for i in range(iterations):
        t = t_values[i]
        y = y_values[i]
        k1 = h * f(t, y)  # Primer paso
        k2 = h * f(t + h / 2, y + k1 / 2)  # Segundo paso
        y_next = y + k2 # Valor siguiente
        y_values.append(y_next)  # Agregar el nuevo valor a la lista

    return t_values, y_values, iterations

# Función que se llama al presionar el botón "Resolver"
def solve():
    try:
        # Obtener los parámetros de la interfaz
        equation = equation_entry.get()
        y0 = float(y0_entry.get())
        t0 = float(t0_entry.get())
        t_end = float(t_end_entry.get())
        h = float(h_entry.get())

        # Definir la función a partir de la ecuación ingresada
        # Aquí se evalúa la ecuación como una función lambda
        f = eval("lambda t, y: " + equation)

        # Llamar a la función de Runge-Kutta
        t_values, y_values, iterations = runge_kutta_2nd_order(f, y0, t0, t_end, h)

        # Mostrar el número de iteraciones
        y_clean_values = [float(f"{number:0.5f}") for number in y_values]
        string_resultado = f"Se realizaron {iterations} iteraciones.\nValores en t: {t_values}\nValores en y: {y_clean_values}"
        messagebox.showinfo("Resultado", string_resultado)
        print(string_resultado)

        # Graficar los resultados
        plt.plot(t_values, y_values, label='Solución')
        plt.xlabel('t')
        plt.ylabel('y')
        plt.title('Solución de la Ecuación Diferencial')
        plt.legend()
        plt.grid()
        plt.show()

    except Exception as e:
        messagebox.showerror("Error", str(e))
        raise e

# Crear la interfaz gráfica
root = tk.Tk()
root.title("Solver de Ecuaciones Diferenciales")

# Etiquetas y campos de entrada
tk.Label(root, text="Ecuación (en términos de t y y):").pack()
equation_entry = tk.Entry(root)
equation_entry.pack()
equation_entry.insert(0,"0.2 * t * y")

tk.Label(root, text="Valor inicial y0:").pack()
y0_entry = tk.Entry(root)
y0_entry.pack()
y0_entry.insert(0,"1")

tk.Label(root, text="Tiempo inicial t0:").pack()
t0_entry = tk.Entry(root)
t0_entry.pack()
t0_entry.insert(0,"1")

tk.Label(root, text="Tiempo final t_end:").pack()
t_end_entry = tk.Entry(root)
t_end_entry.pack()
t_end_entry.insert(0,"1.5")

tk.Label(root, text="Paso h:").pack()
h_entry = tk.Entry(root)
h_entry.pack()
h_entry.insert(0,"0.05")

# Botón para resolver
solve_button = tk.Button(root, text="Resolver", command=solve)
solve_button.pack()

# Iniciar la interfaz
root.mainloop()