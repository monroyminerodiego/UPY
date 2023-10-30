# Car Data Managment  
## Instructions given by teacher 
Hello everyone!

We have an exciting task ahead of us: efficient car data management. 
We have 15 cars, each with five key attributes: Name, Price, Speed, Windows and Doors. 
Our mission is to develop a robust and efficient code that allows:

    - Add a car to the corresponding list (example: the name is added to 'CarNames').
    - Edit the data of an existing car.
    - Remove a car from the list.
    - Query cars (print data from one position).

Our goal is to make this task an example of excellence in data management. Let's work together to create an elegant and efficient solution that demonstrates our commitment to quality.


## Pseudocode of the script

- Declaration of
    - Libraries: 
        * 'os' will be used only to clear the eco of the terminal
    - Global Variables: 
        * <class 'list'> 'CarNames': will be used to store only the names of the cars
        * <class 'list'> 'CarData': will be used to store dictionaries with information of all the cars in our Data Frame
    - Functions:
        * To add a car to the lists
        * To edit a car
        * To delete a car
        * To search a car
        * To show a menu
    - Data Frame:
        * A list of 15 cars with their respective features

- Add the Data Frame to the lists

- Make a loop that repeats until user's choice says the opposite with:
    - The statement to clear the eco of the terminal
    - The users choice based on the menu
    - According to users choice:
        - If user's choice is a valid option of the menu, then call the according function.
        - If user's choice is not a valid option, deploy a message
        

## Explanation of functions 

<table>
    <thead>
        <tr>
            <th>Function Name</th>
            <th>Inputs</th>
            <th>Description</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td align="center">add_car()</td>
            <td align="center">
                * Name: class 'str'<br>
                * Price: class 'float'<br>
                * Speed: class 'int'<br>
                * Windows: class 'int'<br>
                * Doors: class 'int'<br>
            </td>
            <td align="center">
                - 'Car' dictionary is declared, having ['Name','Price','Speed','Windows','Doors'] as keys and their respective input attached as value.<br>
                - '.append()' method used on list 'CarNames' to add 'Name' as a new element.<br>
                - '.append()' method used on list 'CarData' to add 'Car' dictionary as a new element.<br>
                - Returns a string giving positive feedback<br>
            </td>
        </tr>
        <tr>
            <td align="center">edit_car()</td>
            <td align="center">
                * Name: class 'str' <br>
                * NewName: class 'str'<br>
                * NewPrice: class 'float'<br>
                * NewSpeed: class 'int'<br>
                * NewWindows: class 'int'<br>
                * NewDoors: class 'int'<br>
            </td>
            <td align="center">
                If 'Name' makes a match in list 'CarNames', then:<br>
                    - Variable 'Index' is declared with the index of 'Name' in list 'CarNames'.<br>
                    - 'NewName', 'NewPrice', 'NewSpeed', 'NewWindows' and 'NewDoors' will be the replacement for the old values of the dictionary.<br>
                    - It returns a string giving positive feedback<br>
                <br>
                Every other scenario:<br>
                    - It returns a string giving negative feedback<br>
            </td>
        </tr>
        <tr>
            <td align="center">delete_car()</td>
            <td align="center">
                * Name: class 'str'
            </td>
            <td align="center">
            If 'Name' makes a match in list 'CarNames', then:<br>
                - 'Index' variable is declared, with the index of 'Name' in 'CarNames' list, as value.<br>
                - With that index variable, '.pop()' method is called on both 'CarNames' and 'CarData' lists.<br>
                - It returns a string giving positive feedback<br>
            <br>
            Every other scenario:<br>
                - It returns a string giving negative feedback<br>
            </td>
        </tr>
        <tr>
            <td align="center">search_car()</td>
            <td align="center">* Index: class 'int'</td>
            <td align="center">
            If 'Index' is between 0 and the lenth of list 'CarData', then:<br>
                - 'Car' variable is declared with the corresponding dictionary stored in list 'CarData' looked up by 'Index' variable<br>
                - A string with all the information of the dictionary will be returned<br>
            <br>
            Every other scenario:<br>
                - A string giving negative feedback will be returned.<br>
            </td>
        </tr>
        <tr>
            <td align="center">ask_new_car()</td>
            <td align="center">* Expects 0 inputs</td>
            <td align="center">
            - 'Name' variable is declared asking for the input to user.<br>
            - 'Price' variable is declared asking for the input to user, but automatically converting the input to class 'float'<br>
            - 'Speed' variable is declared asking for the input to user, but automatically converting the input to class 'int'<br>
            - 'Windows' variable is declared asking for the input to user, but automatically converting the input to class 'int'<br>
            - 'Doors' variable is declared asking for the input to user, but automatically converting the input to class 'int'<br>
            <br>
            - 'add_car()' function is called, passing by arguments the previous declared variables and the output of that function will be returned<br>
            </td>
        </tr>
        <tr>
            <td align="center">show_menu</td>
            <td align="center">Expects 0 arguments.</td>
            <td align="center">
            - Funtion that will only print the menu of the script<br>
            <br>
            - Returns the option entered by user via input.<br>
            </td>
        </tr>
    </tbody>
</table>  

--- 

## Made By
- Juan Antonio Cel Vazquez
- Sergio Johanan Barrera Chan
- Ariel Joel Buenfil Góngora
- Diego Monroy Minero