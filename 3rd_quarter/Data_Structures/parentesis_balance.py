'''
It is useful to be able to detect whether the parentheses in a source file are balanced or not.

A stack can be used: a+(b+c)*[(d+e])/f

While the end of the input file has not been reached:

    * Discard symbols that do not need to be balanced.
    * If it is an opening parenthesis, push it to the stack.
    * If it is a closing parenthesis, perform a pop and compare.
    * If they are of the same type, continue.
    * If they are of different types, report an error.
    * If the end of the file is reached and the stack is not empty, report an error.
'''

def push(list,element):
    list.append(element)
    return list

def pop(list):
    return list.pop()

def balance_parenthesis(stack_to_balance):
    stack_to_balance = stack_to_balance.split()
    print(stack_to_balance)

if __name__ == '__main__':
    stack = 'a+(b+c)*[(d+e])/f'
    if balance_parenthesis(stack):
        print('Error')
    else:
        print('Stack is in balance')