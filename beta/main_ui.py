"""
main_ui.py

The main UI the user will be interacting with
"""

import constants

def init_main_ui(controls):
    # make window
    root.title('MCyber Arm UI')
    
    # make frame
    app = Frame(root)
    app.grid()
    app.configure(background = 'gray')

    # title label
    title = Label(app, text = 'MCyber Arm UI', font = '-weight bold')
    title.grid(row = 0, column = 0, columnspan = 8)

    # control type dropdown menu
    controlVar.set('Keyboard')
    controlMenu = OptionMenu(app, controlVar, *constants.CONTROL_TYPES, command = controlMenuChoose)
    controlMenu.config(width = 20, height = 4, font = '-weight bold')
    controlMenu.grid(row = 1, column = 0, columnspan = 3)

    # checkbox for whether to hold directional button for input
    toggleHoldCheckbox = Checkbutton(app, font = '-weight bold', text = 'Toggle Button Holding', variable = toggleHoldVar, width = 20, height = 4)
    toggleHoldCheckbox.grid(row = 2, column = 0, columnspan = 3)

    # buttons for arm movement
    elbowUpButton = Button(app, font = '-weight bold', text = 'Elbow Up', command = lambda: elbowUpPressed(toggleHoldVar), width = 16, height = 4)
    elbowUpButton.grid(row = 3, column = 3, columnspan = 3)

    wristLeftButton = Button(app, font = '-weight bold', text = 'Wrist Left', command = lambda: WristLeftPressed(toggleHoldVar), width = 16, height = 4)
    wristLeftButton.grid(row = 4, column = 0, columnspan = 3)
    
    grabberButton = Button(app, font = '-weight bold', text = 'Grab', command = grabberPressed, width = 16, height = 4)
    grabberButton.grid(row = 4, column = 0, columnspan = 3)
    
    wristRightButton = Button(app, font = '-weight bold', text = 'Wrist Right', command = lambda: WristRightPressed(toggleHoldVar), width = 16, height = 4)
    wristRightButton.grid(row = 4, column = 3, columnspan = 3)

    elbowDownButton = Button(app, font = '-weight bold', text = 'Elbow Down', command = lambda: elbowDownPressed(toggleHoldVar), width = 16, height = 4)
    elbowDownButton.grid(row = 5, column = 0, columnspan = 3)



    # tutorial text box
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
        ', controls['k']['S1U'], ' - Up\n\
        ', controls['k']['S1D'], ' - Down\n\
        ', controls['k']['S2T'],' - Toggle Grab'
    tutorial = Label(app, text = tutorialText, font = '-weight bold')
    tutorial.grid(row = 1, column = 3, columnspan = 5, rowspan = 4)

    # keyboard events
    app.bind(controls['k']['S1U'], S1U) 
    app.bind(controls['k']['S1D'], S1D)
    app.bind(controls['k']['S2T'], S2T)
    app.bind("<Tab>", remapEvent)
    app.focus()

    return app