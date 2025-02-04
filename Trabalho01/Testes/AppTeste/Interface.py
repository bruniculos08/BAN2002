from tkinter import *

# Creating a screen (class Tk):
root = Tk()

# Creating a label widget:
myLabel1 = Label(root, text="Hello, world 1!")
myLabel2 = Label(root, text="My name is Torvalds!")
# Obs.: Label é um classe

# Showing it into the screen:
myLabel1.grid(row = 0, column = 0)
myLabel2.grid(row = 1, column = 5)

# Note that mainloop() makes the function that generates the screen keep running:
root.mainloop()