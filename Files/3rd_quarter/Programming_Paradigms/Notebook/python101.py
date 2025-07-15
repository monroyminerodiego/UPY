import os; os.system('cls')
# 1. Class - Define a class called Car
class Car:
    # 2. Instance - Initialize an instance of the class with attributes
    def __init__(self, brand, model):
        self.brand = brand
        self.model = model
 
    # 3. Object - Create two objects (cars) from the class
    def info(self):
        print(f"Hello, the brand of the car is {self.brand}\nAnd the model is {self.model}.")
 
# 4. Message - Sending a message to the object
car1 = Car("Honda", 'City')
car1.info()  # Calls the info method on car1
 
car2 = Car("Mitsubishi", 'Lancer')
car2.info()  # Calls the info method on car2
 
# 5. Inheritance - Create a subclass that inherits from Car
class Driver(Car):
    def __init__(self, name, age, licence_id):
        super().__init__(name, age)
        self.licence_id = licence_id
        self.tournaments = []
 
    def info_gas(self, fuel_measure):
        print(f"A {self.brand} {self.model} needs {fuel_measure} gallons.")
 
    # 7. Abstraction - Encapsulate the concept of enrolling in a course
    def register_tournament(self, tornament_name):
        self.tournaments.append(tornament_name)
        print(f"{self.brand} {self.model} has won the tournament: {tornament_name}")
 
# 6. Polymorphism - Using polymorphism to call greet method on different objects
def get_info(car):
    car.info()
 
driver = Driver("Mariana", 22, "2109110")
get_info(car1)  # Polymorphism with a car object
get_info(driver)   # Polymorphism with a driver object
 
# 8. Encapsulation - Accessing attributes through methods, encapsulating data
driver.register_tournament("Grand Pix")
 
# Accessing the encapsulated course list
print(f"The {driver.brand} {driver.model} has won the torunaments: {driver.tournaments}")