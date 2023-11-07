'''
Exercise 1: Filter and Transform with Lambda Functions

Write a Python program that takes a list of numbers and does the following using lambda functions:
    * Filter out all the even numbers from the list.
    * Square each of the remaining odd numbers.
    * Calculate the sum of the squared odd numbers.

Example: 
Input: [1, 2, 3, 4, 5, 6]
Output: 35 

Explanation: Filtering out the even numbers gives [1, 3, 5]. Squaring these numbers and summing them gives 1^2 + 3^2 + 5^2 = 35.
'''

if __name__ == '__main__':
    import os; os.system('cls')
    list_of_numbers = [1, 2, 3, 4, 5, 6]
    print((lambda array: sum([value**2 for value in array if value%2!=0]))(list_of_numbers))
    