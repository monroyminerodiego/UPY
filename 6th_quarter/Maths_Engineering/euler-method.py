import tkinter as tk
from tkinter import messagebox
import sympy as sp
import matplotlib.pyplot as plt

def euler_method_gui():
    def solve_euler():
        try:
            # Obtener valores de entrada desde la interfaz gráfica.
            # func_str: la ecuación diferencial f(x, y) como string.
            func_str = func_entry.get()
            x0 = float(x0_entry.get())  # Valor inicial de x (x0).
            y0 = float(y0_entry.get())  # Valor inicial de y (y0).
            h = float(h_entry.get())    # Tamaño del paso (h).
            x_final = float(x_final_entry.get())  # Valor final de x.

            # Validar que los valores ingresados sean consistentes.
            if h <= 0 or x_final <= x0:
                raise ValueError("h debe ser positivo y x_final debe ser mayor que x0.")

            # Convertir la función f(x, y) a una expresión simbólica usando sympy.
            x, y = sp.symbols('x y')  # Definir variables simbólicas x e y.
            f = sp.sympify(func_str)  # Convertir la función de texto a una expresión matemática.

            # Determinar el número de pasos necesarios basados en el rango de x y el tamaño del paso h.
            n_steps = int((x_final - x0) / h)
            
            # Inicializar listas para almacenar valores de x e y.
            # Estas listas contendrán los valores calculados en cada paso del método de Euler.
            x_values = [x0]  # La lista comienza con el valor inicial de x.
            y_values = [y0]  # La lista comienza con el valor inicial de y.

            # Implementar el método de Euler para resolver la EDO.
            for i in range(n_steps):
                # Obtener los valores actuales (x_n, y_n).
                xn = x_values[-1]  # Último valor de x en la lista (x_n).
                yn = y_values[-1]  # Último valor de y en la lista (y_n).

                # Evaluar la función f(x, y) en el punto actual (x_n, y_n).
                # Esto corresponde a calcular f(x_n, y_n) en la ecuación del método de Euler.
                try:
                    fn = f.subs({x: xn, y: yn})  # Reemplazar x y y con xn y yn en f(x, y).
                    fn = float(fn)  # Asegurar que el resultado sea un número flotante.
                except Exception as e:
                    raise ValueError(f"Error al evaluar f en (x={xn}, y={yn}): {e}")

                # Calcular el próximo valor de y usando la fórmula del método de Euler:
                # y_{n+1} = y_n + h * f(x_n, y_n)
                yn_plus_1 = yn + h * fn

                # Calcular el próximo valor de x usando la fórmula:
                # x_{n+1} = x_n + h
                xn_plus_1 = xn + h

                # Almacenar los valores calculados (x_{n+1}, y_{n+1}) en las listas correspondientes.
                x_values.append(xn_plus_1)
                y_values.append(yn_plus_1)

            # Mostrar los resultados calculados en el área de texto de la interfaz gráfica.
            # Cada par (x, y) se muestra con 5 decimales.
            results = "".join([f"x = {xi:.5f}, y = {yi:.5f}\n" for xi, yi in zip(x_values, y_values)])
            result_text.delete(1.0, tk.END)
            result_text.insert(tk.END, results)

            # Graficar los resultados obtenidos.
            plt.figure(figsize=(8, 6))
            plt.plot(x_values, y_values, marker='o', label='Método de Euler')
            plt.title('Solución Aproximada - Método de Euler')
            plt.xlabel('x')  # Etiqueta del eje x.
            plt.ylabel('y')  # Etiqueta del eje y.
            plt.grid(True)   # Mostrar la cuadrícula en la gráfica.
            plt.legend()     # Mostrar la leyenda para identificar la curva.
            plt.show()

        except ValueError as ve:
            # Mostrar errores relacionados con valores inválidos ingresados por el usuario.
            messagebox.showerror("Error de Validación", f"{ve}")
        except Exception as e:
            # Mostrar cualquier otro error inesperado.
            messagebox.showerror("Error", f"Ha ocurrido un error inesperado: {e}")

    # Crear ventana principal de la interfaz gráfica.
    root = tk.Tk()
    root.title("Método de Euler")
    root.configure(bg="#2f2f2f")

    # Título principal.
    title_label = tk.Label(root, text="Método de Euler para ecuaciones diferenciales", 
                            font=("Arial", 16, "bold"), fg="white", bg="#2f2f2f")
    title_label.grid(row=0, column=0, columnspan=2, pady=10)

    # Crear entradas y etiquetas para que el usuario introduzca datos.
    tk.Label(root, text="Función f(x, y)\n(Ejemplo: 4*x + 3*y):", font=("Arial", 12), fg="white", bg="#2f2f2f").grid(row=1, column=0, padx=10, pady=5)
    func_entry = tk.Entry(root, width=30, font=("Arial", 12))
    func_entry.grid(row=1, column=1, padx=10, pady=5)

    tk.Label(root, text="x0 (Valor inicial de x):", font=("Arial", 12), fg="white", bg="#2f2f2f").grid(row=2, column=0, padx=10, pady=5)
    x0_entry = tk.Entry(root, width=10, font=("Arial", 12))
    x0_entry.grid(row=2, column=1, padx=10, pady=5, sticky="w")

    tk.Label(root, text="y0 (Valor inicial de y):", font=("Arial", 12), fg="white", bg="#2f2f2f").grid(row=3, column=0, padx=10, pady=5)
    y0_entry = tk.Entry(root, width=10, font=("Arial", 12))
    y0_entry.grid(row=3, column=1, padx=10, pady=5, sticky="w")

    tk.Label(root, text="Tamaño del paso (h):", font=("Arial", 12), fg="white", bg="#2f2f2f").grid(row=4, column=0, padx=10, pady=5)
    h_entry = tk.Entry(root, width=10, font=("Arial", 12))
    h_entry.grid(row=4, column=1, padx=10, pady=5, sticky="w")

    tk.Label(root, text="x final:", font=("Arial", 12), fg="white", bg="#2f2f2f").grid(row=5, column=0, padx=10, pady=5)
    x_final_entry = tk.Entry(root, width=10, font=("Arial", 12))
    x_final_entry.grid(row=5, column=1, padx=10, pady=5, sticky="w")

    # Botón para resolver la ecuación diferencial usando el método de Euler.
    solve_button = tk.Button(root, text="Resolver", command=solve_euler, font=("Arial", 12), bg="#4caf50", fg="white")
    solve_button.grid(row=6, column=0, columnspan=2, pady=10)

    # Área de texto para mostrar resultados.
    result_text = tk.Text(root, width=50, height=15, font=("Arial", 12), fg="white", bg="#3e3e3e")
    result_text.grid(row=7, column=0, columnspan=2, padx=10, pady=10)

    # Ejecutar la ventana principal.
    root.mainloop()

if __name__ == "__main__":
    euler_method_gui()