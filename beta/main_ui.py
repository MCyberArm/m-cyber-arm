"""
main_ui.py

The main UI the user will be interacting with
"""

import constants
from constants import ServoName
from constants import ServoCommand
from constants import ControlType
from arm import Arm
from joint import Joint

def init_main_ui(arm):
    # make window
    arm.root.title('MCyber Arm UI')
    
    # make frame
    app = Frame(arm.root)
    app.grid()
    app.configure(background = 'gray')

    # title label
    title = Label(app, text = 'MCyber Arm UI', font = '-weight bold')
    title.grid(row = 0, column = 0, columnspan = 8)

    # control type dropdown menu
    controlVar.set('Keyboard')
    # TODO: remove CONTROL_TYPES and replace with enum, fix controlVar and this OptionMenu
    controlMenu = OptionMenu(app, controlVar, *constants.CONTROL_TYPES, command = controlMenuChoose)        # TODO: make controlMenuChoose function
    controlMenu.config(width = 20, height = 4, font = '-weight bold')
    controlMenu.grid(row = 1, column = 0, columnspan = 3)

    # checkbox for whether to hold directional button for input
    # TODO: fix toggleHoldVar
    toggleHoldCheckbox = Checkbutton(app, font = '-weight bold', text = 'Toggle Button Holding', variable = toggleHoldVar, width = 20, height = 4)
    toggleHoldCheckbox.grid(row = 2, column = 0, columnspan = 3)

    # buttons for arm movement
    arm.joints[ServoName.ELBOW].setup_ui_button(command_type = ServoCommand.UP, text = 'Elbow Up', row = 3, column = 3)
    arm.joints[ServoName.WRIST].setup_ui_button(command_type = ServoCommand.UP, text = 'Wrist Left', row = 4, column = 0)
    arm.joints[ServoName.GRABBER].setup_ui_button(command_type = ServoCommand.TOGGLE, text = 'Grab', row = 4, column = 3)
    arm.joints[ServoName.WRIST].setup_ui_button(command_type = ServoCommand.DOWN, text = 'Wrist Right', row = 4, column = 6)
    arm.joints[ServoName.ELBOW].setup_ui_button(command_type = ServoCommand.DOWN, text = 'Elbow Down', row = 5, column = 3)

    # tutorial text box
    # TODO: have tutorial text display all controls (include custom xbox controller controls)
    tutorialText = 'Tutorial\n\
        This UI provides a panel to both control the \n\
        arm and configure its settings. To begin select\n\
        from the top dropdown to set the control for\n\
        Arm movement to either Keyboard or Controller.\n\
        Below you can see the control mappings for each\n\
        configuration.\n\n\
        Controller:\n\
        Y - Up\n\
        A - Down\n\
        X - Toggle Grab\n\n\
        Keyboard:\n\
        ', arm.controls['k']['elbow_down'], ' - Up\n\
        ', arm.controls['k']['elbow_up'], ' - Down\n\
        ', arm.controls['k']['grabber_toggle'],' - Toggle Grab'
    tutorial = Label(app, text = tutorialText, font = '-weight bold')
    tutorial.grid(row = 1, column = 3, columnspan = 5, rowspan = 4)

    # keyboard events
    # TODO
    arm.joints[ServoName.GRABBER].keyboard_bindings(app = app)
    
    # app.bind(controls['k']['S1U'], S1U)
    # app.bind(controls['k']['S1D'], S1D)
    # app.bind(controls['k']['S2T'], S2T)
    
    app.bind("<Tab>", remapEvent)       # TODO: make function to handle this
    
    app.focus()

    return app