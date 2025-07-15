print('''
--------------------------------------------------------
Program made to convert degrees to radians and viceversa
--------------------------------------------------------
''')
import math
import os

def deg_to_rad(x):
    degrees = (x*math.pi)/180
    return degrees
def rad_to_deg(x):
    radians = (x*180)/math.pi
    return radians

loop = 'y'
while loop == 'y':
    try:
        x = float(input('Enter a number: '))
    except:
        print("You didn't enter a number")
        x = float(input('Enter a number: '))

    operation = input('''Choose an option:
    a. Convert from radians to degrees
    b. Convert from degrees to radians\n''').lower()
    if operation == 'a':
        result = round(rad_to_deg(x),4)
        print('The result of your conversion is: '+str(result)+'°')
    elif operation == 'b':
        result = round(deg_to_rad(x),4)
        print('The result of your conversion is: '+str(result)+' radians')
    else:
        print('You chose an invalid option')
        operation = input('''Choose an option:
    a. Convert from radians to degrees
    b. Convert from degrees to radians\n''').lower()
    loop = input('Do you want to do another conversion?(Y/N): ').lower()
    if loop == 'y':
        os.system('cls')
print('\nProgram made by Diego Monroy')