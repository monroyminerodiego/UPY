# Crear listas para mantener un seguimiento de los datos de los coches
CarNames = []
CarData = []

# Función para agregar un coche a la lista
def add_car(Name, Price, Speed, Windows, Doors):
    Car = {
        'Name': Name,
        'Price': Price,
        'Speed': Speed,
        'Windows': Windows,
        'Doors': Doors
    }
    CarNames.append(Name)
    CarData.append(Car)

# Función para editar los datos de un coche existente
def edit_car(Name, NewName, NewPrice, NewSpeed, NewWindows, NewDoors):
    if Name in CarNames:
        Index = CarNames.index(Name)
        CarData[Index]['Name'] = NewName
        CarData[Index]['Price'] = NewPrice
        CarData[Index]['Speed'] = NewSpeed
        CarData[Index]['Windows'] = NewWindows
        CarData[Index]['Doors'] = NewDoors
        CarNames[Index] = NewName
    else:
        print("Car's not on the list.")

# Función para eliminar un coche de la lista
def delete_car(Name):
    if Name in CarNames:
        Index = CarNames.index(Name)
        CarNames.pop(Index)
        CarData.pop(Index)
    else:
        print("Car's not on the list.")

# Función para consultar coches e imprimir datos de una posición
def search_car(Index):
    if Index >= 0 and Index < len(CarData):
        Car = CarData[Index]
        print("Name:", Car['Name'])
        print("Price:", Car['Price'])
        print("Speed:", Car['Speed'])
        print("Windows:", Car['Windows'])
        print("Doors:", Car['Doors'])
    else:
        print("Index out of range.")

# Función para agregar un nuevo elemento a la lista
def add_new_element():
    Name = input("Enter the name of the new car: ")
    Price = float(input("Enter the price of the new car: "))
    Speed = int(input("Enter the speed of the new car: "))
    Windows = int(input("Enter the number of windows of the new car: "))
    Doors = int(input("Enter the number of doors of the new car: "))

    add_car(Name, Price, Speed, Windows, Doors)
    print(f"Car '{Name}' added succesfully.")

# Función para mostrar el menú y recibir la opción del usuario
def show_menu():
    print("\n--- Menú ---")
    print("1. Search a car")
    print("2. Edit a car")
    print("3. Delete a car")
    print("4. Add new car")
    print("5. Exit")
    return input("Enter your option: ")

# Agregar los 15 coches especificados
dfCars = [
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

for Car in dfCars:
    add_car(*Car)

# Bucle principal del programa
while True:
    UserChoice = show_menu()

    if UserChoice == "1":
        Index = int(input("Ingrese la posición del coche a consultar: "))
        search_car(Index)
    elif UserChoice == "2":
        nombre = input("Ingrese el nombre del coche a editar: ")
        nuevo_nombre = input("Ingrese el nuevo nombre: ")
        nuevo_precio = float(input("Ingrese el nuevo precio: "))
        nueva_velocidad = int(input("Ingrese la nueva velocidad: "))
        nuevas_ventanas = int(input("Ingrese el número de nuevas ventanas: "))
        nuevas_puertas = int(input("Ingrese el número de nuevas puertas: "))
        edit_car(nombre, nuevo_nombre, nuevo_precio, nueva_velocidad, nuevas_ventanas, nuevas_puertas)
        print("Coche editado con éxito.")
    elif UserChoice == "3":
        nombre = input("Ingrese el nombre del coche a eliminar: ")
        delete_car(nombre)
        print("Coche eliminado con éxito.")
    elif UserChoice == "4":
        add_new_element()
    elif UserChoice == "5":
        print("¡Hasta luego!")
        break
    else:
        print("Opción no válida. Por favor, seleccione una opción válida del menú.")