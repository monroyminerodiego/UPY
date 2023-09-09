import os
import time

print('''
---------------------------------------------------------------
Program made to add, subtract, multiply and divide two numbers
---------------------------------------------------------------
''')
def sum(x1,x2):
    print('The answer is: '+str(round(x1+x2,2)))
def subs(x1,x2):
    print('The answer is: '+str(round(x1-x2,2)))
def mul(x1,x2):
    print('The answer is: '+str(round(x1*x2,2)))
def div(x1,x2):
    print('The answer is: '+str(round(x1/x2,2)))

loop = 'y'
while loop == 'y':
    x1 = float(input('Write the first number: '))
    x2 = float(input('Write the second number: '))
    operation = input('''Choose an option:
    a. Add
    b. Substract
    c. Multiply
    d. Divide\n''').lower()
    if operation == 'a':
        sum(x1,x2)
        loop = input('Try another operation? (Y/N): ').lower()
    elif operation == 'b':
        subs(x1,x2)
        loop = input('Try another operation? (Y/N): ').lower()
    elif operation == 'c':
        mul(x1,x2)
        loop = input('Try another operation? (Y/N): ').lower()
    elif operation == 'd':
        div(x1,x2)
        loop = input('Try another operation? (Y/N): ').lower()
    else:
        print('You entered an incorrect option.')
        time.sleep(2)
        loop = 'y'
    os.system('cls')
print('Thanks for using it!')