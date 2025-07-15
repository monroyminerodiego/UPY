import os
os.system('cls')

class Employee:
    def __init__(self,name = str, salary = float, type = str, senority = int):
        self.name = name
        self.salary = salary
        self.type = type
        self.senority = senority

    def increase_salary(self,type,senority):
        if type == 'R' and senority <= 2:
            self.salary += 1000
        elif type == 'R' and senority > 2:
            self.salary += 2000
        elif type == 'M' and senority <= 2:
            self.salary += 3000
        elif type == 'M' and senority > 2:
            self.salary += 5000



# Inherence
class Manager(Employee):
    def __init__(self,name = str, salary = float, type = str, senority = int, employees_under = int):
        super().__init__(name,salary,type,senority)
        self.employes_under = employees_under
        self.employees_list = []

    # Abstraction
    def add_employees(self,employee_list = list):
        for employee in employee_list:
            self.employees_list.append(employee)

    # Polyimorphism
    def give_bonus(self):
        if self.senority <= 1:
            bonus = 0
        elif self.senority > 1 and self.senority < 5:
            bonus = 5000
        else:
            bonus = 7000

        return bonus

class RegularEmployee(Employee):
    def __init__(self,name = str, salary = float, type = str, senority = int, manager_name = str):
        super().__init__(name,salary,type,senority)
        self.manager_name = manager_name

    
    def give_bonus(self):
        if self.senority <= 1:
            bonus = 0
        elif self.senority > 1 and self.senority < 5:
            bonus = 5000
        else:
            bonus = 7000

        return bonus

if __name__ == '__main__':
    df = [
        ['Ariel Buenfil Gongora',35000.45, 'R', 1, 'Diego Monroy'],
        ['Sergio Barrera Chan', 45000.12, 'R', 3, 'Diego Monroy'],
        ['Juan Cel Vazquez', 50000.01, 'R', 7, 'Diego Monroy'],
        ['Diego Monroy', 85000.25, 'M', 6]
    ]

    employees_list = []
    managers_list = []

    for row in df:
        print(f'Information of {row[0]} - {"Manager" if row[2] == "M" else "Regular"}')

        if row[2] == 'R':
            employee = RegularEmployee(row[0],row[1],row[2],row[3],row[4])
            employees_list.append(row[0])
            print(f'Giving {employee.give_bonus()} bonus')

        elif row[2] == 'M':
            employee = Manager(row[0],row[1],row[2],row[3])
            managers_list.append(employee)
            print(f'Giving {employee.give_bonus()} bonus')
            print(f'Adding {employees_list} as employees under charge')
            # Encapsulation
            employee.add_employees(employees_list)

        print('\n\n\n')



    