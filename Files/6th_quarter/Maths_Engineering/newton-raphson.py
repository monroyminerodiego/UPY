import tkinter as tk
from tkinter import ttk, messagebox
import sympy as sp

class NewtonRaphsonApp:
    def __init__(self, master):
        self.master = master
        master.title("Newton-Raphson")
        master.geometry("600x700")
        master.configure(bg='#2C3E50')

        # Estilo para widgets
        style = ttk.Style()
        style.theme_use('clam')

        # Configuración de colores
        bg_color = '#2C3E50'
        fg_color = '#ECF0F1'
        entry_bg = '#34495E'
        button_color = '#3498DB'

        # Frame principal
        main_frame = tk.Frame(master, bg=bg_color)
        main_frame.pack(expand=True, fill="both", padx=20, pady=20)

        # Título
        title_label = tk.Label(
            main_frame, 
            text="Método de Newton-Raphson", 
            font=("Arial", 24, "bold"),
            bg=bg_color, 
            fg='#FFFFFF'
        )
        title_label.pack(pady=(30, 20))

        # Estilo personalizado para entradas y etiquetas
        style.configure('Custom.TLabel', 
            background=bg_color, 
            foreground=fg_color, 
            font=('Arial', 12)
        )

        style.configure('Custom.TEntry', 
            background=entry_bg,
            foreground=fg_color
        )

        # Frame de entradas
        input_frame = tk.Frame(main_frame, bg=bg_color)
        input_frame.pack(padx=40, fill="x")

        # Función
        ttk.Label(input_frame, text="Función (en términos de x):", 
                  style='Custom.TLabel').pack(anchor="w", pady=(10, 5))
        self.func_entry = ttk.Entry(input_frame, width=50,)
        self.func_entry.pack(pady=5)
        self.func_entry.insert(0, "x**2 - 4")

        # Valor inicial
        ttk.Label(input_frame, text="Valor inicial:", 
                  style='Custom.TLabel').pack(anchor="w", pady=(10, 5))
        self.x0_entry = ttk.Entry(input_frame, width=50)
        self.x0_entry.pack(pady=5)
        self.x0_entry.insert(0, "1.0")

        # Tolerancia
        ttk.Label(input_frame, text="Tolerancia:", 
                  style='Custom.TLabel').pack(anchor="w", pady=(10, 5))
        self.tol_entry = ttk.Entry(input_frame, width=50)
        self.tol_entry.pack(pady=5)
        self.tol_entry.insert(0, "1e-6")

        # Máximo de iteraciones
        ttk.Label(input_frame, text="Máximo de iteraciones:", 
                  style='Custom.TLabel').pack(anchor="w", pady=(10, 5))
        self.max_iter_entry = ttk.Entry(input_frame, width=50)
        self.max_iter_entry.pack(pady=5)
        self.max_iter_entry.insert(0, "100")

        # Botón de calcular
        calc_button = tk.Button(
            main_frame, 
            text="Calcular Raíz", 
            command=self.newton_raphson,
            bg=button_color,
            fg='white',
            font=("Arial", 14, "bold"),
            relief=tk.FLAT,
            activebackground='#2980B9'
        )
        calc_button.pack(pady=20)

        # Área de resultados
        self.result_text = tk.Text(
            main_frame, 
            width=60, 
            height=10,
            bg=entry_bg, 
            fg=fg_color,
            font=("Consolas", 12),
            borderwidth=2,
            relief=tk.FLAT
        )
        self.result_text.pack(padx=20)
        self.result_text.config(state=tk.DISABLED)

    def newton_raphson(self):
        try:
            # ----------------------------------------------------------------------------------------------------------------------------------------------------

            
            # Valores de entrada
            func_str = self.func_entry.get() 
            #Es la función f(x) que se ingresa en el formulario, en términos de x. Ejemplo: x**2 - 4
            
            x0 = float(self.x0_entry.get())
            #Es el valor inicial proporcionado por el usuario, el cual se utiliza como primera estimación de la raíz.
            
            tol = float(self.tol_entry.get())
            #La tolerancia especificada por el usuario. Sirve como criterio de paro. 
            #Si dos valores consecutivos están más cerca que esta tolerancia, se considera que el método ha convergido.
            #Que el método de Newton-Raphson haya convergido significa que se ha encontrado una solución con la precisión deseada. 
            
            
            max_iter = int(self.max_iter_entry.get())
            #El número máximo de iteraciones permitidas antes de que el método abandone.
            #epresenta el número máximo de iteraciones permitidas para que el algoritmo intente encontrar una raíz antes de detenerse.

           
            # ----------------------------------------------------------------------------------------------------------------------------------------------------
           
            
            # Preparar símbolos y función
            x = sp.symbols('x') 
            #Declara x como un símbolo matemático para trabajar con Sympy
            
            func = sp.sympify(func_str)
            #Convierte la función ingresada como texto en una expresión simbólica, entendible por Sympy.
            
            func_prime = sp.diff(func, x)
            #Calcula la derivada simbólica de f(x), que se usa en el método
            
            
            # ----------------------------------------------------------------------------------------------------------------------------------------------------

            
            # Método de Newton-Raphson
            iteration = 0
            while iteration < max_iter:
                f_x0 = func.evalf(subs={x: x0}) #Sustituye x0 en f(x) y evalúa su valor.
                f_prime_x0 = func_prime.evalf(subs={x: x0}) #Sustituye x0 en f′(x) y evalúa su valor.
                
                if abs(f_prime_x0) < 1e-10:
                    self.mostrar_resultado("La derivada es muy pequeña, el método puede no converger.")
                    return
                #Si f′(x0) es cercano a cero, se interrumpe el cálculo porque esto genera un divisor muy pequeño 
                #en la fórmula de actualización, lo que puede causar errores numéricos.
                
                
                x1 = x0 - f_x0 / f_prime_x0
                #Aplica la fórmula del método de Newton-Raphson:

                
                # Comprobar el criterio de paro
                if abs(x1 - x0) < tol:
                    resultado = f"Raíz encontrada: {x1}\nNúmero de iteraciones: {iteration+1}"
                    self.mostrar_resultado(resultado)
                    return
                #Si la diferencia entre x1 y x0 es menor que la tolerancia, 
                #se asume que el método ha convergido, y el programa muestra la raíz encontrada.
                
                x0 = x1 #Actualiza x0 para usarlo en la siguiente iteración.
                iteration += 1 #Incrementa el contador de iteraciones.

            
            self.mostrar_resultado("El método no convergió después del número máximo de iteraciones.")

        except Exception as e:
            messagebox.showerror("Error", str(e))

    def mostrar_resultado(self, resultado):
        # Habilitar el área de texto, limpiarla, insertar el resultado, y deshabilitarla
        self.result_text.config(state=tk.NORMAL)
        self.result_text.delete('1.0', tk.END)
        self.result_text.insert(tk.END, resultado)
        self.result_text.config(state=tk.DISABLED)

def main():
    root = tk.Tk()
    app = NewtonRaphsonApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()