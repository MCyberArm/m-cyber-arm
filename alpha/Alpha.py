import time
import RPi.GPIO as GPIO
from tkinter import *
import pygame

# constants
elbowNum = 24
grabberNum = 12
controlTypes = {'Keyboard', 'Controller'}

# global variables
grabberIsOn = 0
currentPos = 7.5
controls = {}
Remapping = 0
CFGPath = "config.txt"
# S1D = "Servo 1 Down"
# S1U = "Servo 1 Up"
# S2T = "Servo 2 Toggle" (because that's all we do with it)
controls['k'] = {}
controls['c'] = {}
lastPressedButton = ''
root = Tk()
controlVar = StringVar(root)
toggleHoldVar = IntVar(root)

# setup GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(elbowNum, GPIO.OUT)
GPIO.setup(grabberNum, GPIO.OUT)
elbowPWM = GPIO.PWM(elbowNum, 50)
grabberPWM = GPIO.PWM(grabberNum, 50)
elbowPWM.start(7.5)
grabberPWM.start(2.5)
# Second number above is the refresh rate for the servo (in Hz)


# functions
def loadCFG():
    global controls
    global CFGPath
    try:
        with open(CFGPath, 'r') as f:
            lines = f.readlines()
            for lne in lines:
                ctrls = lne.split()
                if len(ctrls) != 3 or (ctrls[0] != 'k' and ctrls[0] != 'c'):
                    
                    print("ERROR! Invalid config")
                    raise IOError
                controls[ctrls[0]][ctrls[1]] = ctrls[2]
                print("controls[",ctrls[0],"][",ctrls[1], "] = ", ctrls[2])


    except IOError as e:
        print("Couldn't find config file. Using default config instead. Error code: (%s)." % e)
        controls['k']['S1U'] = '<Up>'
        controls['k']['S1D'] = '<Down>'
        controls['k']['S2T'] = '<space>'
        controls['c']['S1U'] = '<y>'
        controls['c']['S1D'] = '<a>'
        controls['c']['S2T'] = '<x>'

def setupGPIO():
    print("Proper Initialization will go here")
    # Above number is amount to change by?? (Double Check)

def controlMenuChoose(*args):
    print('chose control type ' + args[0])

def S1U(event):
    holdVar = IntVar()
    holdVar.set(False)
    elbowUpPressed(holdVar)

def S1D(event):
    holdVar = IntVar()
    holdVar.set(False)
    elbowDownPressed(holdVar)

def S2T(event):
    grabberPressed()

def remapEvent(event):
    global Remapping
    Remapping = 1

def elbowUpPressed(toggleHoldVar):
    print('elbow up pressed')
    global currentPos
    if toggleHoldVar.get():
        while currentPos > 2.5:
            currentPos = currentPos - 0.5
            elbowPWM.ChangeDutyCycle(currentPos)
            print("toggleHoldVar, currentPos =", currentPos)
            time.sleep(0.1)
    else:
        currentPos = max(currentPos - 0.5, 2.5)
        elbowPWM.ChangeDutyCycle(currentPos)
        print("currentPos =", currentPos)

def elbowDownPressed(toggleHoldVar):
    print('elbow down pressed')
    global currentPos
    if toggleHoldVar.get():
        while currentPos < 12.5:
            currentPos = currentPos + 0.5
            elbowPWM.ChangeDutyCycle(currentPos)
            print("toggleHoldVar, currentPos =", currentPos)
            time.sleep(0.1)
    else:
        currentPos = min(12.5, currentPos + 0.5)
        elbowPWM.ChangeDutyCycle(currentPos)
        print("currentPos =", currentPos) 

def grabberPressed():
    global grabberIsOn
    grabberIsOn ^= 1
    print('grabber pressed: ' + str(grabberIsOn))
    grabberValues = [2.5, 5.5]
    grabberPWM.ChangeDutyCycle(grabberValues[grabberIsOn])

def remap(function, inputKey):
    # Get button pressed here
    global controls
    controls['k'][function] = inputKey

def onRemapClose():
    global Remapping
    Remapping = -1

def remapEvent(event):
    global lastPressedButton
    print("Printing in remapEvent")
    if(lastPressedButton == ''):
        return
    # Check if pressed a protected key (ESC, Tab, etc)
    print(repr(event.char))
    remap(lastPressedButton, repr(event.char))
    lastPressedButton = ''

def remapUI():
    global controls
    global lastPressedButton
    # make window
    root.title('M Cyber Arm Key Remapping UI')
    
    # make frame
    remapApp = Frame(root)
    remapApp.grid()
    remapApp.configure(background = 'gray')

    # title label
    title = Label(app, text = 'M Cyber Arm Key Remapping UI', font = '-weight bold')
    title.grid(row = 0, column = 0, columnspan = 8)

    # button to return to arm control
    root.protocol("WM_DELETE_WINDOW", onRemapClose)

    # buttons for arm movement
    elbowUpButton = Button(app, font = '-weight bold', text = 'Elbow Up', command = lambda: lastPressedButton = 'S1U', width = 16, height = 4)
    elbowUpButton.grid(row = 3, column = 0, columnspan = 3)

    elbowDownButton = Button(app, font = '-weight bold', text = 'Elbow Down', command = lambda: lastPressedButton = 'S1D', width = 16, height = 4)
    elbowDownButton.grid(row = 4, column = 0, columnspan = 3)

    grabberButton = Button(app, font = '-weight bold', text = 'Grab', command = lambda: lastPressedButton = 'S2T', width = 16, height = 4)
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
        ', controls['k']['S1U'], ' - Up\n\
        ', controls['k']['S1D'], ' - Down\n\
        ', controls['k']['S2T'],' - Toggle Grab'
    tutorial = Label(app, text = tutorialText, font = '-weight bold')
    tutorial.grid(row = 1, column = 3, columnspan = 5, rowspan = 4)

    # keyboard events
    app.bind("<Key>", remapEvent)
    remapApp.focus()

    #root.mainloop()

    return remapApp


def setupUI():
    global controls
    
    # make window
    root.title('M Cyber Arm UI')
    
    # make frame
    app = Frame(root)
    app.grid()
    app.configure(background = 'gray')

    # title label
    title = Label(app, text = 'M Cyber Arm UI', font = '-weight bold')
    title.grid(row = 0, column = 0, columnspan = 8)

    # control type dropdown menu
    controlVar.set('Keyboard')
    controlMenu = OptionMenu(app, controlVar, *controlTypes, command = controlMenuChoose)
    controlMenu.config(width = 20, height = 4, font = '-weight bold')
    controlMenu.grid(row = 1, column = 0, columnspan = 3)

    # checkbox for whether to hold directional button for input
    toggleHoldCheckbox = Checkbutton(app, font = '-weight bold', text = 'Toggle Button Holding', variable = toggleHoldVar, width = 20, height = 4)
    toggleHoldCheckbox.grid(row = 2, column = 0, columnspan = 3)

    # buttons for arm movement
    elbowUpButton = Button(app, font = '-weight bold', text = 'Elbow Up', command = lambda: elbowUpPressed(toggleHoldVar), width = 16, height = 4)
    elbowUpButton.grid(row = 3, column = 0, columnspan = 3)

    elbowDownButton = Button(app, font = '-weight bold', text = 'Elbow Down', command = lambda: elbowDownPressed(toggleHoldVar), width = 16, height = 4)
    elbowDownButton.grid(row = 4, column = 0, columnspan = 3)

    grabberButton = Button(app, font = '-weight bold', text = 'Grab', command = grabberPressed, width = 16, height = 4)
    grabberButton.grid(row = 5, column = 0, columnspan = 3)

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

    #root.mainloop()

    return app

def main():
    global Remapping
    global CFGPath
    loadCFG()
    setupGPIO()
    try:
        app = setupUI()
        pygame.init()
        pygame.joystick.init()

        # main loop
        while True:
            app.update()
            
            for event in pygame.event.get():
                if event.type == pygame.JOYBUTTONDOWN:
                    print('button pressed')

            count = pygame.joystick.get_count()
            if(Remapping == 1):
                Remapping = 0
                app.destroy()
                app = remapUI()
            if(Remapping == -1):
                Remapping = 0
                app.destroy()
                app = setupUI()
            if count == 1:
                # controller is detected
                controller = pygame.joystick.Joystick(0)
                controller.init()

                armUpButton = controller.get_button(0)      # default: A (0)
                armDownButton = controller.get_button(3)    # default: Y (3)
                grabberButton = controller.get_button(2)    # default: X (2)                
                
                if armUpButton == 1:
                    elbowUpPressed(toggleHoldVar)
                elif armDownButton == 1:
                    elbowDownPressed(toggleHoldVar)
                if grabberButton == 1:
                    grabberPressed()
            time.sleep(0.2)
    except KeyboardInterrupt:
        GPIO.output(LEDNum, 0)
        p.stop()
        GPIO.cleanup()
        pygame.quit()

    GPIO.output(LEDNum, 0)
    p.stop()
    GPIO.cleanup()
    pygame.quit()
    #update controls here
    with open(CFGPath, w) as f:
    for keyVal, ctrlType in controls.items():
        for fnctn, keybind in ctrlType.items():
            write(ctrlType, " ", fnctn, keybind)


if __name__ == '__main__':
    main()

