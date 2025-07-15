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

    * **Non-Linear_Structures** <br>
        Make a program for each of the types of structures non-linear:
        * binary.py <br> 1 tree program where it gives me the options to create, insert, delete and perform tours.
        * graphs.py <br> 1 graph program where it gives me the options to create, insert a vertex and delete a vertex.

    * **lottery.py** <br> Script that generates 40 lottery cards with 16 different images, selecting them from the 54 available cards

## Made By
* Diego Monroy Minero