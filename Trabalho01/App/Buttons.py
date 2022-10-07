from tkinter import *

root = Tk()

# Creating input fields (here because we will use it in fuctions):
box = Entry(root, width=50, borderwidth = 5)

# (1) Notice Entry is a class that receives a object of the class Tk (a screen).
# (2) borderwidth is the border size of the button.

# Making some function for a button:
def myClick():
    myLabel = Label(root, text = "Look! I clicked a button!")
    myLabel.grid()

# Making some function for a button but using text field:
def printTextField():
    textFieldStuff = box.get()
    myLabel = Label(root, text = textFieldStuff)
    myLabel.grid()

# Every button is a object from the class button:
isAButton = Button(root, text = "Click Me!", state = 'normal', padx = 50, pady = 50, command = myClick, fg = "green", bg = "white")
isNotAButton = Button(root, text = "Do not click Me!", state = 'disabled')
printButton = Button(root, text = "Print text", state = 'normal', command = printTextField)

# (1) The state defines propreties of the button.
# (2) The padx defines the size in relation to x-axis.
# (3) The pady defines the size in relation to y-axis.
# (4) The fg defines the button text color.
# (5) The bg defines the button background color.
# (6) The command defines the fuction that the button will run when clicked.

# Putting Button in the screen:
isAButton.grid(row=1, column=1)
isNotAButton.grid(row=2, column=1)
printButton.grid()
box.grid()

root.mainloop()