import time
from tkinter import *

# make window
root = Tk()
root.title('M Cyber Arm UI')

# make frame
app = Frame(root)
app.grid()
app.configure(background = 'gray')

# title label
title = Label(app, text = 'M Cyber Arm UI', width = 30, font = '-weight bold')
