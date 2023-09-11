# Car Data Managment (script)

## -------------- Instructions given by teacher --------------
Hello everyone!

We have an exciting task ahead of us: efficient car data management. 
We have 15 cars, each with five key attributes: Name, Price, Speed, Windows and Doors. 
Our mission is to develop a robust and efficient code that allows:

    - Add a car to the corresponding list (example: the name is added to 'CarNames').
    - Edit the data of an existing car.
    - Remove a car from the list.
    - Query cars (print data from one position).

Our goal is to make this task an example of excellence in data management. Let's work together to create an elegant and efficient solution that demonstrates our commitment to quality.

--- 

## -------------- Pseudocode of the script --------------

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
        
--- 

## -------------- Explanation of functions --------------

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
            <td align="center"><p>
                * Name: <class 'str'>
                * Price: <class 'float'>
                * Speed: <class 'int'>
                * Windows: <class 'int'>
                * Doors: <class 'int'>
            </p></td>
            <td align="center"><p>
                - 'Car' dictionary is declared, having ['Name','Price','Speed','Windows','Doors'] as keys and their respective input attached as value.
                - '.append()' method used on list 'CarNames' to add 'Name' as a new element.
                - '.append()' method used on list 'CarData' to add 'Car' dictionary as a new element.
                - Returns a string giving positive feedback
            </p></td>
        </tr>
    </tbody>
</table>

### add_car(Name = str(), Price = float(), Speed = int(), Windows = int(), Doors = int()):
    ---------- Inputs ----------
    * Name: <class 'str'>
    * Price: <class 'float'>
    * Speed: <class 'int'>
    * Windows: <class 'int'>
    * Doors: <class 'int'>

    ---------- Explanation ----------
    - 'Car' dictionary is declared, having ['Name','Price','Speed','Windows','Doors'] as keys and their respective input attached as value.
    - '.append()' method used on list 'CarNames' to add 'Name' as a new element.
    - '.append()' method used on list 'CarData' to add 'Car' dictionary as a new element.
    
    - Returns a string giving positive feedback

### edit_car(Name = str(), NewName = str(), NewPricen = float(), NewSpeed = int(), NewWindows = int(), NewDoors = int()):
    ---------- Inputs ----------
    * Name: <class 'str'> 
    * NewName: <class 'str'>
    * NewPrice: <class 'float'>
    * NewSpeed: <class 'int'>
    * NewWindows: <class 'int'>
    * NewDoors: <class 'int'>

    ---------- Explanation ----------
    If 'Name' makes a match in list 'CarNames', then:
        - Variable 'Index' is declared with the index of 'Name' in list 'CarNames'.
        - 'NewName', 'NewPrice', 'NewSpeed', 'NewWindows' and 'NewDoors' will be the replacement for the old values of the dictionary.
        - It returns a string giving positive feedback

    Every other scenario:
        - It returns a string giving negative feedback

### delete_car(Name = str()):
    ---------- Inputs ----------
    * Name: <class 'str'>

    ---------- Explanation ----------
    If 'Name' makes a match in list 'CarNames', then:
        - 'Index' variable is declared, with the index of 'Name' in 'CarNames' list, as value.
        - With that index variable, '.pop()' method is called on both 'CarNames' and 'CarData' lists.
        - It returns a string giving positive feedback

    Every other scenario:
        - It returns a string giving negative feedback
  
### search_car(Index = int()):
    ---------- Inputs ----------
    * Index: <class 'int'>

    ---------- Explanation ----------
    If 'Index' is between 0 and the lenth of list 'CarData', then:
        - 'Car' variable is declared with the corresponding dictionary stored in list 'CarData' looked up by 'Index' variable
        - A string with all the information of the dictionary will be returned
    
    Every other scenario:
        - A string giving negative feedback will be returned.
 
### ask_new_car():
    ---------- Inputs ----------
    * Expects 0 inputs

    ---------- Explanation ----------
    - 'Name' variable is declared asking for the input to user.
    - 'Price' variable is declared asking for the input to user, but automatically converting the input to <class 'float'>
    - 'Speed' variable is declared asking for the input to user, but automatically converting the input to <class 'int'>
    - 'Windows' variable is declared asking for the input to user, but automatically converting the input to <class 'int'>
    - 'Doors' variable is declared asking for the input to user, but automatically converting the input to <class 'int'>
    
    - 'add_car()' function is called, passing by arguments the previous declared variables and the output of that function will be returned
    
### show_menu():
    ---------- Inputs ----------
    * Expects 0 arguments.

    ---------- Explanation ----------
    - Funtion that will only print the menu of the script

    - Returns the option entered by user via input.

--- 
 
## -------------- Made By --------------
- Diego Monroy Minero
- Sergio Barrera Chan
- Juan Antonio Cel Vazquez
- Ariel Joel Buenfil Góngora