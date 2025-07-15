'''
Made by:
Juan Antonio Cell Vazquez
Sergio Barrera Chan
Ariel Buenfil Gongora
Diego Monroy Minero
'''

if __name__ == '__main__':
    '''
    1. Case: Factorial Calculation
    Write a functional program to calculate the factorial of a given number using recursion.
    '''
    number = int(input('Introduce a number: '))
    factorial = lambda x: 1 if x == 0 else x * factorial(x - 1)
    final_result = factorial(number)
    print(final_result)

    '''
    10. Recursive File Search

    Write a functional program to recursively search for files with a specific extension in a
    given directory and its subdirectories.
    '''
    import os; os.system('cls')
    extension = '.png'
    ParentDirectory = 'Images/'
    os.chdir(ParentDirectory)
    obtain_subdirectory = lambda array: [os.path.splitext(route)[0] for route in array if os.path.splitext(route)[1] == extension]
    print(obtain_subdirectory(os.listdir()))
