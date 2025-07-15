'''
Exercise 2: Map and Calculate Average

Write a Python program that takes a list of numbers and uses lambda functions to square each number and then calculates the average of the squared values.

Example:
Input: [1, 2, 3, 4] 
Output: 7.5 

Explanation: Squaring each number and finding the average of the squared values.
'''

if __name__ == '__main__':
    import os; os.system('cls')
    numbers_list = [1,2,3,4] 
    print((lambda iterable_object: sum([value**2 for value in iterable_object])/len(iterable_object))(numbers_list))