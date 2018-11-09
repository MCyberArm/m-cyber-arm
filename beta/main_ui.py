"""
main_ui.py

The main UI the user will be interacting with
"""

from tkinter import *
import constants
from constants import ServoName
from constants import ServoCommand
from constants import ControlType
from arm import Arm
from joint import Joint

def init_main_ui(arm):
    # make window
    arm.root.title('M Cyber Arm UI')
    
    # make frame
    app = Frame(arm.root)
    app.grid()
    app.configure(background = 'gray')

    # title label
    title = Label(app, text = 'MCyber Arm UI', font = '-weight bold')
    title.grid(row = 0, column = 0, columnspan = 14)

    # control type dropdown menu
    control_type_set = {control_type.value for control_type in constants.ControlType}
    controlMenu = OptionMenu(app, arm.curr_control_type, *control_type_set, command = lambda choice: print('selected', choice))
    controlMenu.config(width = 20, height = 4, font = '-weight bold')
    controlMenu.grid(row = 1, column = 0, columnspan = 4)
    
    # checkbox for whether to lock the arm in place
    toggle_lock_checkbox = Checkbutton(app, font = '-weight bold', text = 'Toggle Arm Lock', variable = arm.locked, width = 20, height = 4)
    toggle_lock_checkbox.grid(row = 2, column = 0, columnspan = 4)

    # checkbox for whether to hold directional button for input
    # TODO: implement this
    # toggle_hold_checkbox = Checkbutton(app, font = '-weight bold', text = 'Toggle Button Holding', variable = TODO, width = 20, height = 4)
    # toggle_hold_checkbox.grid(row = 2, column = 5, columnspan = 4)

    # buttons for arm movement
    arm.joints[ServoName.ELBOW].setup_ui_button(app, command_type = ServoCommand.UP, text = 'Elbow Up', row = 3, column = 3)
    arm.joints[ServoName.WRIST].setup_ui_button(app, command_type = ServoCommand.UP, text = 'Wrist Left', row = 4, column = 0)
    arm.joints[ServoName.GRABBER].setup_ui_button(app, command_type = ServoCommand.TOGGLE, text = 'Grab', row = 4, column = 3)
    arm.joints[ServoName.WRIST].setup_ui_button(app, command_type = ServoCommand.DOWN, text = 'Wrist Right', row = 4, column = 6)
    arm.joints[ServoName.ELBOW].setup_ui_button(app, command_type = ServoCommand.DOWN, text = 'Elbow Down', row = 5, column = 3)

    # tutorial text box
    tutorialText = 'Tutorial\n\
        This UI provides a panel to both control the \n\
        arm and configure its settings. To begin select\n\
        from the top dropdown to set the control for\n\
        Arm movement to either Keyboard or Controller.\n\
        Below you can see the control mappings for each\n\
        configuration.\n\n'\
    + display_controls(arm, ControlType.CONTROLLER) + '\n' + display_controls(arm, ControlType.KEYBOARD)

    tutorial = Label(app, text = tutorialText, font = '-weight bold')
    tutorial.grid(row = 1, column = 9, columnspan = 5, rowspan = 4)
    
    # remapping button
    remap_button = Button(app, font = '-weight bold', text = 'Remap Controls', command = lambda: arm.remapping.set(1), width = 16, height = 4)
    remap_button.grid(row = 6, column = 0, columnspan = 3)

    # keyboard events
    for name, joint in arm.joints.items():
        for servo_command, key in joint.keyboard_controls.items():
            print(joint.name + ': bind', key, 'to', servo_command.value)
            app.bind(key, eval_key_bind(joint, ControlType.KEYBOARD, servo_command))
    
    arm.root.protocol("WM_DELETE_WINDOW", lambda: arm.remapping.set(2))
    
    app.focus()

    return app

def display_controls(arm, control_type):
    output = control_type.value + ':\n'
    
    for servo_name, controls in arm.controls[control_type].items():
        for servo_command, binding in controls.items():
            output += servo_name.value + ' ' + servo_command.value + ' ' + binding + '\n'
    
    return output

# required because lambdas are lazily evaluated in python, causing weird behavior when calling the same lambda in a for loop
eval_key_bind = lambda joint, control_type, servo_command: (lambda e: joint.move(control_type, servo_command))