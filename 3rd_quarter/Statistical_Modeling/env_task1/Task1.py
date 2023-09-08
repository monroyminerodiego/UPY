# Crear listas para mantener un seguimiento de los datos de los coches
CarNames = []
CarData = []

# Función para agregar un coche a la lista
def agregar_coche(nombre, precio, velocidad, ventanas, puertas):
    coche = {
        'Nombre': nombre,
        'Precio': precio,
        'Velocidad': velocidad,
        'Ventanas': ventanas,
        'Puertas': puertas
    }
    CarNames.append(nombre)
    CarData.append(coche)

# Función para editar los datos de un coche existente
def editar_coche(nombre, nuevo_nombre, nuevo_precio, nueva_velocidad, nuevas_ventanas, nuevas_puertas):
    if nombre in CarNames:
        index = CarNames.index(nombre)
        CarData[index]['Nombre'] = nuevo_nombre
        CarData[index]['Precio'] = nuevo_precio
        CarData[index]['Velocidad'] = nueva_velocidad
        CarData[index]['Ventanas'] = nuevas_ventanas
        CarData[index]['Puertas'] = nuevas_puertas
        CarNames[index] = nuevo_nombre
    else:
        print("El coche no existe en la lista.")

# Función para eliminar un coche de la lista
def eliminar_coche(nombre):
    if nombre in CarNames:
        index = CarNames.index(nombre)
        CarNames.pop(index)
        CarData.pop(index)
    else:
        print("El coche no existe en la lista.")

# Función para consultar coches e imprimir datos de una posición
def consultar_coche(posicion):
    if posicion >= 0 and posicion < len(CarData):
        coche = CarData[posicion]
        print("Nombre:", coche['Nombre'])
        print("Precio:", coche['Precio'])
        print("Velocidad:", coche['Velocidad'])
        print("Ventanas:", coche['Ventanas'])
        print("Puertas:", coche['Puertas'])
    else:
        print("Posición fuera de rango.")

# Función para agregar un nuevo elemento a la lista
def agregar_nuevo_elemento():
    nombre = input("Ingrese el nombre del nuevo coche: ")
    precio = float(input("Ingrese el precio del nuevo coche: "))
    velocidad = int(input("Ingrese la velocidad del nuevo coche: "))
    ventanas = int(input("Ingrese el número de ventanas del nuevo coche: "))
    puertas = int(input("Ingrese el número de puertas del nuevo coche: "))

    agregar_coche(nombre, precio, velocidad, ventanas, puertas)
    print(f"El coche '{nombre}' ha sido agregado a la lista.")

# Función para mostrar el menú y recibir la opción del usuario
def mostrar_menu():
    print("\n--- Menú ---")
    print("1. Consultar coche")
    print("2. Editar coche")
    print("3. Eliminar coche")
    print("4. Agregar nuevo coche")
    print("5. Salir")
    return input("Seleccione una opción: ")

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
    agregar_coche(*auto)

# Bucle principal del programa
while True:
    opcion = mostrar_menu()

    if opcion == "1":
        posicion = int(input("Ingrese la posición del coche a consultar: "))
        consultar_coche(posicion)
    elif opcion == "2":
        nombre = input("Ingrese el nombre del coche a editar: ")
        nuevo_nombre = input("Ingrese el nuevo nombre: ")
        nuevo_precio = float(input("Ingrese el nuevo precio: "))
        nueva_velocidad = int(input("Ingrese la nueva velocidad: "))
        nuevas_ventanas = int(input("Ingrese el número de nuevas ventanas: "))
        nuevas_puertas = int(input("Ingrese el número de nuevas puertas: "))
        editar_coche(nombre, nuevo_nombre, nuevo_precio, nueva_velocidad, nuevas_ventanas, nuevas_puertas)
        print("Coche editado con éxito.")
    elif opcion == "3":
        nombre = input("Ingrese el nombre del coche a eliminar: ")
        eliminar_coche(nombre)
        print("Coche eliminado con éxito.")
    elif opcion == "4":
        agregar_nuevo_elemento()
    elif opcion == "5":
        print("¡Hasta luego!")
        break
    else:
        print("Opción no válida. Por favor, seleccione una opción válida del menú.")