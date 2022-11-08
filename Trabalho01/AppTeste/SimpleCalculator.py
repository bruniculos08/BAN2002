from tkinter import *
import re
from numpy import mat

screen = Tk()
screen.title = "Simple Calculator"

# (1) Defining the fiel where the expression will be shown:

field = Entry(screen, width=35, borderwidth=5)
field.grid(row=0, column=0, columnspan=3, padx=20, pady=10)

# Column span is the number of columns used by the object (like we can do for a cel in exceln making...
# ... the cell to ocupy certain number of normal cells)

# It's not necessary:
field.insert(0, "")

# (2) Define button fuctions:

def button_click(number):
    # Get the text in the field:
    current = field.get()
    # Delete the text on the field from index 0 to the last index (END):
    field.delete(0, END)
    field.insert(0, str(current) + str(number))

def button_clear():
    field.delete(0, END)

def button_add():
    first_number = field.get()
    global f_num
    global math
    math = "addition"
    f_num = int(first_number)
    current = field.get()
    field.delete(0, END)
    field.insert(0, str(current) + '+')

def button_sub():
    first_number = field.get()
    global f_num
    global math
    math = "subtration"
    f_num = int(first_number)
    current = field.get()
    field.delete(0, END)
    field.insert(0, str(current) + '-')

def button_mul():
    first_number = field.get()
    global f_num
    global math
    math = "multiply"
    f_num = int(first_number)
    current = field.get()
    field.delete(0, END)
    field.insert(0, str(current) + '*')

def button_div():
    first_number = field.get()
    global f_num
    global math
    math = "division"
    f_num = int(first_number)
    current = field.get()
    field.delete(0, END)
    field.insert(0, str(current) + '/')

def button_equal():

    second_number = field.get().replace('+', '_').replace('-', '_').replace('*', '_').replace('/', '_').split('_')[-1]
    field.delete(0, END)

    if math == "addition":
        field.insert(0, f_num + int(second_number))
    elif math == "subtration":
        field.insert(0, f_num - int(second_number))
    elif math == "multiply":
        field.insert(0, f_num * int(second_number))
    elif math == "division":
        field.insert(0, int(f_num / int(second_number)))

# Define number buttons:

button_1 = Button(screen, text="1", padx = 40, pady = 20, command=lambda: button_click(1))
button_2 = Button(screen, text="2", padx = 40, pady = 20, command=lambda: button_click(2))
button_3 = Button(screen, text="3", padx = 40, pady = 20, command=lambda: button_click(3))
button_4 = Button(screen, text="4", padx = 40, pady = 20, command=lambda: button_click(4))
button_5 = Button(screen, text="5", padx = 40, pady = 20, command=lambda: button_click(5))
button_6 = Button(screen, text="6", padx = 40, pady = 20, command=lambda: button_click(6))
button_7 = Button(screen, text="7", padx = 40, pady = 20, command=lambda: button_click(7))
button_8 = Button(screen, text="8", padx = 40, pady = 20, command=lambda: button_click(8))
button_9 = Button(screen, text="9", padx = 40, pady = 20, command=lambda: button_click(9))
button_0 = Button(screen, text="0", padx = 40, pady = 20, command=lambda: button_click(0))

# Define operations buttons:

clear_button = Button(screen, text="Clear", padx = 79, pady = 20, command=button_clear)
equal_button = Button(screen, text="=", padx = 91, pady = 20, command=button_equal)

add_button = Button(screen, text="+", padx = 39, pady = 20, command=button_add)
sub_button = Button(screen, text="-", padx = 41, pady = 20, command=button_sub)
mul_button = Button(screen, text="*", padx = 40, pady = 20, command=button_mul)
div_button = Button(screen, text="/", padx = 41, pady = 20, command=button_div)

# Put buttons in grid:

button_1.grid(row=1, column=0)
button_2.grid(row=1, column=1)
button_3.grid(row=1, column=2)
button_4.grid(row=2, column=0)
button_5.grid(row=2, column=1)
button_6.grid(row=2, column=2)
button_7.grid(row=3, column=0)
button_8.grid(row=3, column=1)
button_9.grid(row=3, column=2)
button_0.grid(row=4, column=0)

clear_button.grid(row=4, column=1, columnspan=2)
equal_button.grid(row=5, column=1, columnspan=2)
add_button.grid(row=5, column=0)
sub_button.grid(row=6, column=0)
mul_button.grid(row=6, column=1)
div_button.grid(row=6, column=2)

screen.mainloop()