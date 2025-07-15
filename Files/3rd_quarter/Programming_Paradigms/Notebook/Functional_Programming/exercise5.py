'''
Exercise 5: Calculate Factorials

Write a Python program that takes a list of integers and uses lambda functions to calculate the factorial of each number in the list.

Example: 
Input: [1, 2, 3, 4, 5] 
Output: [1, 2, 6, 24, 120]

Explanation: Calculating the factorial of each number in the list
'''

if __name__ == '__main__':
    import os; os.system('cls')
    integer_list = [1, 2, 3, 4, 5] 
    factorial = lambda n: 1 if n <= 0 else n * factorial(n - 1)
    print([factorial(value) for value in integer_list])