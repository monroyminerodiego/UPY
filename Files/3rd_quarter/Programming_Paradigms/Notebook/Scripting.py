"""
Scripting
Create a Python script that automates a file manipulation task.

Requirements:
    * The script should take user input for the source and destination directories.
    * It should list all files in the source directory.
    * Copy each file from the source directory to the destination directory.
    * Print a message for each file copied.

Made by
Diego Monroy Minero
"""

import os

def move_to(path_input:str,path_destination:str):
    os.chdir(path_input)
    os.system('dir')
    files = os.listdir()
    for file in files:
        os.rename(file,os.path.join(path_destination,file))
        print(f'{file} moved successfully...!')

if __name__ == '__main__':
    move_to(
        path_input='UPY/3rd_quarter/Programming_Paradigms/Notebook/Functional_Programming',
        path_destination='UPY/3rd_quarter/Programming_Paradigms/Notebook/Practicing_anonymous_functions'
    )