import os; os.system('cls')

def push(list,element):
    list.append(element)
    return list

def pop(list):
    elemento = list.pop(-1)
    return [list,elemento]

def balance_parenthesis(stack_to_balance):
    stack_to_balance = list(stack_to_balance)
    final_stack = []
    for element in stack_to_balance:
        if (element != ')') and (element != '('):
            continue
        elif element == '(':
            final_stack = push(final_stack,element)
        elif element == ')':
            result = pop(final_stack)
            final_stack = result[0]
            popped_element = result[1]
            if not(element == popped_element):
                return False
    return False if len(final_stack) != 0 else True

        

if __name__ == '__main__':
    stack = 'a+(b+c)*[(d+e])/f'
    print('Error...!' if not(balance_parenthesis(stack)) else 'Success...!')
        