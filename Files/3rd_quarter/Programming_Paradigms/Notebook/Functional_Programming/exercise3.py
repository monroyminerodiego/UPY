'''
Exercise 3: Sorting a List of Dictionaries

Write a Python program that takes a list of dictionaries, where each dictionary contains a name and an age, and uses lambda functions to sort the list by age in descending order.

Example:
Input: [{"name": "Alice", "age": 25}, {"name": "Bob", "age": 30}, {"name": "Charlie", "age": 20}]
Output: [{"name": "Bob", "age": 30}, {"name": "Alice", "age": 25}, {"name": "Charlie", "age": 20}] 

Explanation: The list is sorted by age in descending order using a lambda function.
'''

if __name__ == '__main__':
    import os; os.system('cls')
    dictionaries_list = [{"name": "Alice", "age": 25}, {"name": "Bob", "age": 30}, {"name": "Charlie", "age": 20}]
    print(sorted(dictionaries_list, key=lambda dictionary: dictionary['age'],reverse=True))