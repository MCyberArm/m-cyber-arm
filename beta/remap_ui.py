"""
remap_ui.py

The UI allowing the user to change control bindings
"""

def init_remap_ui(arm):
    # make window
    root.title('M Cyber Arm Key Remapping UI')
    
    # make frame
    app = Frame(arm.root)
    app.grid()
    app.configure(background = 'gray')

    # title label
    title = Label(app, text = 'M Cyber Arm Key Remapping UI', font = '-weight bold')
    title.grid(row = 0, column = 0, columnspan = 8)

    # button to return to arm control
    root.protocol("WM_DELETE_WINDOW", onRemapClose)

    # buttons for arm movement
    elbowUpButton = Button(app, font = '-weight bold', text = 'Elbow Up', command = lambda: arm.last_pressed_button = 'S1U', width = 16, height = 4)
    elbowUpButton.grid(row = 3, column = 0, columnspan = 3)

    elbowDownButton = Button(app, font = '-weight bold', text = 'Elbow Down', command = lambda: arm.last_pressed_button = 'S1D', width = 16, height = 4)
    elbowDownButton.grid(row = 4, column = 0, columnspan = 3)

    grabberButton = Button(app, font = '-weight bold', text = 'Grab', command = lambda: arm.last_pressed_button = 'S2T', width = 16, height = 4)
    grabberButton.grid(row = 5, column = 0, columnspan = 3)

    # tutorial text box
    tutorialText = 'Tutorial\n\
        This UI provides a panel to remap the keys used \n\
        to control the Pi. Press a key to map it to the \n\
        command shown at the top of the screen, or press\n\
        Tab to keep the current mapping. Below you can\n\
        see the current mappings for each action. Currently,\n\
        this feature is for keyboard only. \n\
        Controller:\n\
        Y - Up\n\
        A - Down\n\
        X - Toggle Grab\n\n\
        Keyboard:\n\
        ', ServoName.ELBOW, ' ', ServoCommand.UP, ' - ', arm.controls[ControlType.KEYBOARD][ServoName.ELBOW][ServoCommand.UP], '\n\
        ', ServoName.ELBOW, ' ', ServoCommand.DOWN, ' - ', arm.controls[ControlType.KEYBOARD][ServoName.ELBOW][ServoCommand.DOWN], '\n\
        ', ServoName.WRIST, ' ', ServoCommand.UP, ' - ', arm.controls[ControlType.KEYBOARD][ServoName.WRIST][ServoCommand.UP], '\n\
        ', ServoName.WRIST, ' ', ServoCommand.DOWN, ' - ', arm.controls[ControlType.KEYBOARD][ServoName.WRIST][ServoCommand.DOWN], '\n\
        ', ServoName.GRABBER, ' ', ServoCommand.TOGGLE, ' - ', arm.controls[ControlType.KEYBOARD][ServoName.GRABBER][ServoCommand.TOGGLE]
    tutorial = Label(app, text = tutorialText, font = '-weight bold')
    tutorial.grid(row = 1, column = 3, columnspan = 5, rowspan = 4)

    # keyboard events
    app.bind("<Key>", remapEvent)       # TODO: make remap_event function
    app.focus()

    return app