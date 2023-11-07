'''
Exercise 2: Sorting a List of Tuples
Write a Python program that takes a list of tuples, where each tuple contains a name and an age. Use lambda functions to sort the list by age in ascending order.

Example: 
Input: [("Juan", 25), ("Pablo", 30), ("Jose", 20)] 
Output: [("Jose", 20), ("Juan", 25), ("Pablo", 30)] 

Explanation: The list is sorted by age in ascending order using a lambda function.
'''

if __name__ == '__main__':
    import os; os.system('cls')
    list_of_tuples = [("Juan", 25), ("Pablo", 30), ("Jose", 20)]
    print(sorted(list_of_tuples, key=lambda tuple: tuple[0]))