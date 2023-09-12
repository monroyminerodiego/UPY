class Coche:
    def _init_(self, nombre, precio, velocidad, ventanas, puertas):
        self.nombre = nombre
        self.precio = precio
        self.velocidad = velocidad
        self.ventanas = ventanas
        self.puertas = puertas

    def _str_(self):
        return f"Nombre: {self.nombre}\nPrecio: {self.precio}\nVelocidad: {self.velocidad}\nVentanas: {self.ventanas}\nPuertas: {self.puertas}"

class CatalogoCoches:
    def _init_(self):
        self.coches = []

    def agregar_coche(self, coche):
        self.coches.append(coche)

    def editar_coche(self, nombre, nuevo_nombre, nuevo_precio, nueva_velocidad, nuevas_ventanas, nuevas_puertas):
        for coche in self.coches:
            if coche.nombre == nombre:
                coche.nombre = nuevo_nombre
                coche.precio = nuevo_precio
                coche.velocidad = nueva_velocidad
                coche.ventanas = nuevas_ventanas
                coche.puertas = nuevas_puertas
                break

    def eliminar_coche(self, nombre):
        for coche in self.coches:
            if coche.nombre == nombre:
                self.coches.remove(coche)
                break

    def consultar_coche(self, posicion):
        if 0 <= posicion < len(self.coches):
            print(self.coches[posicion])
        else:
            print("Posición fuera de rango.")

    def mostrar_coches(self):
        for i, coche in enumerate(self.coches):
            print(f"{i}. {coche.nombre}")

def mostrar_menu():
    print("\n--- Menú ---")
    print("1. Consultar coche")
    print("2. Editar coche")
    print("3. Eliminar coche")
    print("4. Agregar nuevo coche")
    print("5. Salir")
    return input("Seleccione una opción: ")

# Crear una instancia de CatalogoCoches
catalogo = CatalogoCoches()

# Agregar los 15 coches especificados
autos = [
   ("Rolls-Royce Phantom", 450000, 150, 4, 4),
    ("Bentley Continental GT", 250000, 200, 2, 2),
    ("Mercedes-Benz S-Class", 100000, 155, 4, 4),
    ("BMW 7 Series", 95000, 160, 4, 4),
    ("Audi A8", 85000, 155, 4, 4),
    ("Porsche Panamera", 90000, 170, 4, 4),
    ("Jaguar XJ", 80000, 155, 4, 4),
    ("Lexus LS", 80000, 150, 4, 4),
    ("Maserati Quattroporte", 120000, 190, 4, 4),
    ("Aston Martin DB11", 230000, 200, 2, 2),
    ("Tesla Model S (alto rendimiento)", 80000, 163, 4, 4),
    ("Cadillac Escalade", 75000, 120, 4, 4),
    ("Lincoln Navigator", 85000, 140, 4, 4),
    ("Range Rover Vogue", 95000, 130, 4, 4),
    ("Lamborghini Urus (SUV de lujo)", 200000, 190, 4, 4)

]

for auto in autos:
    coche = Coche(*auto)
    catalogo.agregar_coche(coche)

# Bucle principal del programa
while True:
    opcion = mostrar_menu()

    if opcion == "1":
        posicion = int(input("Ingrese la posición del coche a consultar: "))
        catalogo.consultar_coche(posicion)
    elif opcion == "2":
        nombre = input("Ingrese el nombre del coche a editar: ")
        nuevo_nombre = input("Ingrese el nuevo nombre: ")
        nuevo_precio = float(input("Ingrese el nuevo precio: "))
        nueva_velocidad = int(input("Ingrese la nueva velocidad: "))
        nuevas_ventanas = int(input("Ingrese el número de nuevas ventanas: "))
        nuevas_puertas = int(input("Ingrese el número de nuevas puertas: "))
        catalogo.editar_coche(nombre, nuevo_nombre, nuevo_precio, nueva_velocidad, nuevas_ventanas, nuevas_puertas)
        print("Coche editado con éxito.")
    elif opcion == "3":
        nombre = input("Ingrese el nombre del coche a eliminar: ")
        catalogo.eliminar_coche(nombre)
        print("Coche eliminado con éxito.")
    elif opcion == "4":
        # Agregar un nuevo coche al catálogo
        nombre = input("Ingrese el nombre del nuevo coche: ")
        precio = float(input("Ingrese el precio del nuevo coche: "))
        velocidad = int(input("Ingrese la velocidad del nuevo coche: "))
        ventanas = int(input("Ingrese el número de ventanas del nuevo coche: "))
        puertas = int(input("Ingrese el número de puertas del nuevo coche: "))

        coche_nuevo = Coche(nombre, precio, velocidad, ventanas, puertas)
        catalogo.agregar_coche(coche_nuevo)
        print(f"El coche '{nombre}' ha sido agregado al catálogo.")
    elif opcion == "5":
        print("¡Hasta luego!")
        break
    else:
        print("Opción no válida. Por favor, seleccione una opción válida del menú.")