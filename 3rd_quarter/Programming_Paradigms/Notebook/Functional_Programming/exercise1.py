'''
Exercise 1: Find Prime Numbers

Write a Python program that takes a list of numbers and uses lambda functions to filter out all the prime numbers from the list.

Example: 
Input: [2, 3, 4, 5, 6, 7, 8, 9] 
Output: [2, 3, 5, 7] 

Explanation: Filtering out the prime numbers from the list.
'''

if __name__ == '__main__':
    import os; os.system('cls')
    # list_numbers = [i for i in range(1,101)] # Array to get first 100 numbers
    numbers_list = [2, 3, 4, 5, 6, 7, 8, 9]
    print((lambda iterable_object: [value for value in iterable_object if ((value%2!=0) and (value%3!=0) and (value%5!=0) and (value%7!=0) and (value%13!=0)) or (value in [2,3,5,7,13])])(numbers_list))
