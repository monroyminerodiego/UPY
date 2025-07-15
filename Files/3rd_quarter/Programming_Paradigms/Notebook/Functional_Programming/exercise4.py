'''
Exercise 4: Filtering Strings

Write a Python program that takes a list of strings and uses lambda functions to filter out all the strings that contain the letter 'a'.

Example:
Input: ["apple", "banana", "cherry", "date", "fig"] 
Output: ["apple","banana", "date"] 

Explanation: Filtering out the strings containing the letter 'a'.
'''

if __name__ == '__main__':
    import os; os.system('cls')
    string_list = ["apple", "banana", "cherry", "date", "fig"]
    print((lambda array: [value for value in array if 'a' in value])(string_list))