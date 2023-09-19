# DATA STRUCTURES FOLDER

## Detailed Description
* Notebook
    * **parentesis_balance.py**<br>
    It is useful to be able to detect whether the parentheses in a source file are balanced or not.
    A stack can be used: " a+(b+c)*[(d+e])/f "  
    While the end of the input file has not been reached:
        1. Discard symbols that do not need to be balanced.
        2. If it is an opening parenthesis, push it to the stack.
        3. If it is a closing parenthesis, perform a pop and compare:  
            If they are of the same type, continue...  
            If they are of different types, report an error...
        6. If the end of the file is reached and the stack is not empty, report an error.

## Change Log
### 2023-09-14
- Notebook: Creation of 'parentesis_balance.py' file

## Made By
* Diego Monroy Minero