"""
# Estructura de una clase en python
class DataBase:
    def __init__(self, valor):
        pass

    def Saludo (self):
        pass
    
    def Despedida(self):
        pass

    def Pregunta(self):
        pass

"""

# Bibliotecas
import os

class DataBase:
    def __init__(self, lista:list):
        # Inicializamos variables necesarias
        self.carros = lista 
        self.NombreCar = str
        self.Price = str
        self.Speed = str
        self.Window = str
        self.Door = str



    def ShowCars(self):
        """
        Input: -> None

        Process:
            - recorro la lista 
            - Guardo la info de cada item por posicion
            - imprimo mi informacion
        
        Output: <- None
        """

        # recorremos, Guardamos e imprimimos por cada iteracion el for
        for car in self.carros:
            self.NombreCar = car[0]
            self.Price = car[1]
            self.Speed = car[2]
            self.Window = car[3]
            self.Door = car[4]

            print(f'Nombre: {self.NombreCar}\nPrice: {self.Price}\nSpeed: {self.Speed}\nWindows: {self.Window}\nDoors: {self.Door}\n\n\n')



    def ShowCar(self):
        """
        Input: -> None

        Process: 
            - Muestra los nombres de los autos
            - Limpia pantalla
            - Input del nombre a buscar
            - Busca el auto e imprime caracteristicas
        
        Output : <- None
        """
        
        # Mostramos los nombres de los Autos
        os.system("clear") # Limpiar pantalla para linux & mac
        #os.system("cls") # Limpiar pantalla para windows

        print("=== Nombre de autos existentes ===")
        for car in self.carros:
            print(car[0])


        # Solicitamos entrada de autos
        self.NombreCar = input("Nombre de auto a buscar: ")
       
        os.system("clear") # Limpiar pantalla para linux & mac
        #os.system("cls") # Limpiar pantalla para windows


        # Mostramos la info completa de esa coincidencia
        print("== Caracteristicas ==")
        for item in self.carros:
            if item[0] == self.NombreCar:
                self.NombreCar = item[0]
                self.Price = item[1]
                self.Speed = item[2]
                self.Window = item[3]
                self.Door = item[4]


        # Imprimimos
        print(f'Nombre:{self.NombreCar}\nPrice:{self.Price}\nSpeed:{self.Speed}\nWindows:{self.Window}\nDoors:{self.Door}\n\n\n')
    


    def AddCar(self):
        """
        Input: -> None

        Process:
            -Input por parte del usuario de cada informacion
            - Creamos un Set de lista 
            - Agregamos ese set a la lista original
            - Imprimimos
        
        Output: <- None
        """

        #solicitamos la info
        self.NombreCar = input("Nombre a añadir: ")
        self.Price = input("Precio a añadir: ")
        self.Speed = input("Velocidad a añadir: ")
        self.Window = input("Ventanas a añadir: ")
        self.Door = input("Puertas a añadir: ")
        
        #creamos el set y lo añadimos
        self.carros.append([self.NombreCar,
        self.Price,
        self.Speed,
        self.Window,
        self.Door])

        os.system("clear") # Limpiar pantalla para linux & mac
        #os.system("cls") # Limpiar pantalla para windows
    


    def DeleteCar(self):

        """
        Input: -> None
        Process:
            - Imprimimos los nombres
            - Pedimos input
            - Eliminamos 
            - Reducimos el largo de lista para que no de error de index out of range
        """
        
        # Mostramos los nombres de los Autos
        os.system("clear") # Limpiar pantalla para linux & mac
        #os.system("cls") # Limpiar pantalla para windows

        print("=== Nombre de autos existentes ===")
        for car in self.carros:
            print(car[0])
        
        # Input de usuario del nombre el auto a eliminar
        self.NombreCar = input("Nombre del auto a eliminar: ")

        os.system("clear") # Limpiar pantalla para linux & mac
        #os.system("cls") # Limpiar pantalla para windows

        # Lo buscamos y lo eliminamos
        """
        Aqui corregi algo, debemos buscar el index y luego eliminarlo fuera del for\
        si no el for graba que son 3 indices con el len y al eliminarlo adentro se reduce\
        a 2, lo que genera error de out of index
        """

        FinalIndex = int
        for index in range(0,len(self.carros)): # Recorremos y buscamos index
            if self.carros[index][0] == self.NombreCar:
                FinalIndex =  index

        del self.carros[FinalIndex] # Eliminamos

        print("== Elemento Eliminado ==")








