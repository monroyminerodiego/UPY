"""
Event-Oriented Programming in Python

Instructions:
Create a simple event-driven program in Python that responds to button clicks.

Requirements:

    * Use a GUI library like Tkinter.
    * Create a window with a button.
    * Define an event handler function that prints a message when the button is clicked.
    * Associate the event handler with the button click event.


Made by
Diego Monroy
"""



import tkinter as tk

def press(window):
    window = tk.Toplevel(window) 
    tk.Label(window, text='Thank you, slave! -_-', bg='#D3E6F2').pack()

window = tk.Tk()
window.config(bg='#D3E6F2')

tk.Label(window, bg='#D3E6F2',text='Jelou word...! c:').pack(expand=True)

btn = tk.Button(window, text='Dare you to click me! :p', bg='#D3E6F2', command=lambda:press(window=window))
btn.pack(expand=True)

window.mainloop()