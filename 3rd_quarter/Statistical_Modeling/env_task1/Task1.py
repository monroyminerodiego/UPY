import os

CarNames = []
CarData = []

def add_car(Name = str(), Price = float(), Speed = int(), Windows = int(), Doors = int()):
    """
    ---------- Arguments ----------
    * Name: <class 'str'>
    * Price: <class 'float'>
    * Speed: <class 'int'>
    * Windows: <class 'int'>
    * Doors: <class 'int'>

    ---------- Explanation ----------
    - 'Car' dictionary is declared, having ['Name','Price','Speed','Windows','Doors'] as keys and their respective input attached as value.
    - '.append()' method used on list 'CarNames' to add 'Name' as a new element.
    - '.append()' method used on list 'CarData' to add 'Car' dictionary as a new element.

    - Returns a string giving positive feedback
    """
    Car = {
        'Name': Name,
        'Price': Price,
        'Speed': Speed,
        'Windows': Windows,
        'Doors': Doors
    }
    CarNames.append(Name)
    CarData.append(Car)

    return "Car added succesfully!"
def ask_new_car():
    """
    ---------- Arguments ----------
    * Expects 0 arguments

    ---------- Explanation ----------
    - 'Name' variable is declared asking for the input to user.
    - 'Price' variable is declared asking for the input to user, but automatically converting the input to <class 'float'>
    - 'Speed' variable is declared asking for the input to user, but automatically converting the input to <class 'int'>
    - 'Windows' variable is declared asking for the input to user, but automatically converting the input to <class 'int'>
    - 'Doors' variable is declared asking for the input to user, but automatically converting the input to <class 'int'>
    
    - 'add_car()' function is called, passing by arguments the previous declared variables and the output of that function will be returned
    """

    Name = input("\nEnter the name of the new car: ")
    Price = float(input("Enter the price of the new car: "))
    Speed = int(input("Enter the speed of the new car: "))
    Windows = int(input("Enter the number of windows of the new car: "))
    Doors = int(input("Enter the number of doors of the new car: "))

    return add_car(Name, Price, Speed, Windows, Doors)
def edit_car(Name = str(), NewName = str(), NewPricen = float(), NewSpeed = int(), NewWindows = int(), NewDoors = int()):
    """
    ---------- Arguments ----------
    * Name: <class 'str'> 
    * NewName: <class 'str'>
    * NewPrice: <class 'float'>
    * NewSpeed: <class 'int'>
    * NewWindows: <class 'int'>
    * NewDoors: <class 'int'>

    ---------- Explanation ----------
    If 'Name' makes a match in list 'CarNames', then:
        - Variable 'Index' is declared with the index of 'Name' in list 'CarNames'.
        - 'NewName', 'NewPrice', 'NewSpeed', 'NewWindows' and 'NewDoors' will be the replacement for the old values of the dictionary.
        - It returns a string giving positive feedback

    Every other scenario:
        - It returns a string giving negative feedback
    """
    if Name in CarNames:
        Index = CarNames.index(Name)
        CarData[Index]['Name'] = NewName
        CarData[Index]['Price'] = NewPrice
        CarData[Index]['Speed'] = NewSpeed
        CarData[Index]['Windows'] = NewWindows
        CarData[Index]['Doors'] = NewDoors
        CarNames[Index] = NewName
        return "Car edited succesfully."
    else:
        return "Car's not on the list."
def delete_car(Name = str()):
    """
    ---------- Arguments ----------
    * Name: <class 'str'>

    ---------- Explanation ----------
    If 'Name' makes a match in list 'CarNames', then:
        - 'Index' variable is declared, with the index of 'Name' in 'CarNames' list, as value.
        - With that index variable, '.pop()' method is called on both 'CarNames' and 'CarData' lists.
        - It returns a string giving positive feedback

    Every other scenario:
        - It returns a string giving negative feedback
    """
    if Name in CarNames:
        Index = CarNames.index(Name)
        CarNames.pop(Index)
        CarData.pop(Index)
        return "Car deleted succesfully"
    else:
        return "Car's not on the list."
def search_car(Index = int()):
    """
    ---------- Arguments ----------
    * Index: <class 'int'>

    ---------- Explanation ----------
    If 'Index' is between 0 and the lenth of list 'CarData', then:
        - 'Car' variable is declared with the corresponding dictionary stored in list 'CarData' looked up by 'Index' variable
        - A string with all the information of the dictionary will be returned
    
    Every other scenario:
        - A string giving negative feedback will be returned.
    """    
    if Index >= 0 and Index < len(CarData):
        Car = CarData[Index]
        return f"Name: {Car['Name']}\nPrice: {Car['Price']}\nSpeed: {Car['Speed']}\nWindows: {Car['Windows']}\nDoors: {Car['Doors']}"
    else:
        return "Index out of range"
def show_menu():
    """
    ---------- Arguments ----------
    * Expects 0 arguments.

    ---------- Explanation ----------
    - Funtion that will only print the menu of the script

    - Returns the option entered by user via input.
    """
    print("\n--- Menu ---\n1. Search a car\n2. Edit a car\n3. Delete a car\n4. Add new car\n5. Exit")
    return input("Enter your option: ")

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

while True:
    os.system('cls')

    UserChoice = show_menu()

    if UserChoice == "1":
        Index = int(input("\nInsert the position of the car you want to search: "))
        print(f'\n{search_car(Index)}')
        input("\n\n\nPress 'Enter' to continue...")

    elif UserChoice == "2":
        Name = input("\nEnter the name of the car to edit: ")
        NewName = input("Enter the new name: ")
        NewPrice = float(input("Enter the new price: "))
        NewSpeed = int(input("Enter the new speed: "))
        NewWindows = int(input("Enter the number of new windows: "))
        NewDoors = int(input("Enter the number of new doors: "))
        print(f'\n{edit_car(Name, NewName, NewPrice, NewSpeed, NewWindows, NewDoors)}')
        input("\n\n\nPress 'Enter' to continue...")
    
    elif UserChoice == "3":
        Name = input("\nEnter the name of the car to delete: ")
        print(f'\n{delete_car(Name)}')
        input("\n\n\nPress 'Enter' to continue...")
    
    elif UserChoice == "4":
        print(f'\n{ask_new_car()}')
        input("\n\n\nPress 'Enter' to continue...")
    
    elif UserChoice == "5":
        print('\nGood bye!')
        input("\n\n\nPress 'Enter' to continue...")
        break
    
    else:
        print("No valid option. Please, select a valid option from menu.")