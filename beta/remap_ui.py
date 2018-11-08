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
    
    # remappable buttons
    i = 1
    for servo_name, joint in arm.joints.items():
        for servo_command, key in joint.keyboard_controls.items():
            text = servo_name.value + ' ' + servo_command.value + ' ' + key
            joint.setup_remap_ui_button(app, servo_command, text, i, 0)
            i += 1
    
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
    # TODO: get it to work with controller remapping
    app.bind("<Key>", lambda event: get_new_key(event, arm))
    app.focus()

    return app

def get_new_key(event, arm):
    if arm.last_pressed_button_joint.get() != '':
        key_pressed = repr(event.char)
        remap(arm, event.char)

def remap(arm, new_key):
    print('remap', arm.last_pressed_button_joint.get(), arm.last_pressed_button_command.get(), 'with', new_key)
    # TODO: maybe have function that converts new_key to <new_key> to handle weird edge cases (if they exist)
    # TODO: handle controller button changes
    # TODO: handle non-letter characters (such as arrow keys)
    
    servo_name = ServoName(arm.last_pressed_button_joint.get())
    command = ServoCommand(arm.last_pressed_button_command.get())
    new_key = '<' + new_key + '>'
    
    arm.controls[ControlType.KEYBOARD][servo_name][command] = new_key
    curr_text = arm.joints[servo_name].remap_ui_button_texts[command].get()
    arm.joints[servo_name].remap_ui_button_texts[command].set(' '.join(curr_text.split(' ')[:-1]) + ' ' + new_key)
    
    # TODO: update joint's controls
    arm.last_pressed_button_joint.set('')
    arm.last_pressed_button_command.set('')