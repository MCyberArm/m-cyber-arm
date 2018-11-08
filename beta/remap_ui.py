"""
remap_ui.py

The UI allowing the user to change control bindings
"""

from tkinter import *
from main_ui import display_controls
import constants
from constants import ServoName
from constants import ServoCommand
from constants import ControlType
from arm import Arm
from joint import Joint

# TODO: allow remapping of controller buttons

def init_remap_ui(arm):
    # make window
    arm.root.title('M Cyber Arm Key Remapping UI')
    
    # make frame
    app = Frame(arm.root)
    app.grid()
    app.configure(background = 'gray')

    # title label
    title = Label(app, text = 'M Cyber Arm Key Remapping UI', font = '-weight bold')
    title.grid(row = 0, column = 0, columnspan = 8)

    # buttons for arm movement
    # elbowUpButton = Button(app, font = '-weight bold', text = 'Elbow Up', command = lambda: arm.last_pressed_button.set('S1U'), width = 16, height = 4)
    # elbowUpButton.grid(row = 3, column = 0, columnspan = 3)

    # elbowDownButton = Button(app, font = '-weight bold', text = 'Elbow Down', command = lambda: arm.last_pressed_button.set('S1D'), width = 16, height = 4)
    # elbowDownButton.grid(row = 4, column = 0, columnspan = 3)

    # grabberButton = Button(app, font = '-weight bold', text = 'Grab', command = lambda: arm.last_pressed_button.set('S2T'), width = 16, height = 4)
    # grabberButton.grid(row = 5, column = 0, columnspan = 3)

    # tutorial text box
    tutorialText = 'Tutorial\n\
        This UI provides a panel to remap the keys used \n\
        to control the Pi. Press a key to map it to the \n\
        command shown at the top of the screen, or press\n\
        Tab to keep the current mapping. Below you can\n\
        see the current mappings for each action. Currently,\n\
        this feature is for keyboard only. \n\n'\
        + display_controls(arm, ControlType.CONTROLLER) + '\n' + display_controls(arm, ControlType.KEYBOARD)
    tutorial = Label(app, text = tutorialText, font = '-weight bold')
    tutorial.grid(row = 1, column = 3, columnspan = 5, rowspan = 4)
    
    # button to return to arm control
    arm.root.protocol("WM_DELETE_WINDOW", lambda: arm.remapping.set(-1))

    # keyboard events
    # app.bind("<Key>", remap_event)       # TODO: make remap_event function
    app.focus()

    return app
