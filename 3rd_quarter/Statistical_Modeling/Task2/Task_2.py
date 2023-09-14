class Car:
    def _init_(self, Name, Price, Speed, Windows, Doors):
        self.name = Name
        self.price = Price
        self.speed = Speed
        self.windows = Windows
        self.doors = Doors

    def _str_(self):
        return f"Name: {self.name}\nPrice: {self.price}\nSpeed: {self.speed}\nWindows: {self.windows}\nDoors: {self.doors}"

class CarsMenu:
    def _init_(self):
        self.CarsList = []

    def add_car(self, car):
        self.CarsList.append(car)

    def edit_car(self, name, new_name, new_project, new_speed, new_windows, new_doors):
        for car in self.CarsList:
            if car.name == name:
                car.name = new_name
                car.price = new_project
                car.speed = new_speed
                car.windows = new_windows
                car.doors = new_doors
                break

    def delete_car(self, name):
        for car in self.CarsList:
            if car.name == name:
                self.CarsList.remove(car)
                break

    def lookup_car(self, position):
        if 0 <= position < len(self.CarsList):
            print(self.CarsList[position])
        else:
            print("Position out of range.")

    def show_cars(self):
        for i, car in enumerate(self.CarsList):
            print(f"{i}. {car.name}")

def show_menu():
    print("\n--- Menu ---")
    print("1. Look up for a car")
    print("2. Edit a car")
    print("3. Delete a car")
    print("4. Add new car")
    print("5. Exit")
    return input("Enter an option: ")



catalogue = CarsMenu()

cars_df = [
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
for car in cars_df:
    car_class = Car(*car)
    catalogue.add_car(car_class)

print(type(catalogue))

while True:
    user_option = show_menu()

    if user_option == "1":
        position = int(input("Enter the position of the car to look up: "))
        catalogue.lookup_car(position)
    elif user_option == "2":
        name = input("Enter the name of the car to edit: ")
        new_name = input("Enter the new name: ")
        new_price = float(input("Enter the new price: "))
        new_speed = int(input("Enter the new speed: "))
        new_windows = int(input("Enter the new windows: "))
        new_doors = int(input("Enter the new doors: "))
        catalogue.edit_car(name, new_name, new_price, new_speed, new_windows, new_doors)
        print("Car added successfully.")
    elif user_option == "3":
        name = input("Enter the name of the car to delete: ")
        catalogue.delete_car(name)
        print("Car deleted successfully")
    elif user_option == "4":
        name = input("Enter the name of the new car: ")
        price = float(input("Enter the price of the new car: "))
        speed = int(input("Enter the speed of the new car: "))
        windows = int(input("Enter the numer of windows of the new car: "))
        doors = int(input("Enter the number of doors of the car: "))

        new_car = Car(name, price, speed, windows, doors)
        catalogue.add_car(new_car)
        print(f"Car '{name}' added successfully.")
    elif user_option == "5":
        print("Good bye!")
        break
    else:
        print(" Invalid option. Please, enter a valid option from menu: ")