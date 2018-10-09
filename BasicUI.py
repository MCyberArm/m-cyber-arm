import time
import RPi.GPIO as GPIO
from tkinter import *
import pygame

# constants
servoNum = 24
LEDNum = 25
controlTypes = {'Keyboard', 'Controller'}

# global variables
grabberIsOn = 0
currentPos = 7.5
controls = {}
controls['k'] = {}
controls['c'] = {}
root = Tk()
controlVar = StringVar(root)
toggleHoldVar = IntVar(root)

# setup GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(servoNum, GPIO.OUT)
GPIO.setup(LEDNum, GPIO.OUT)
p=GPIO.PWM(servoNum, 50)
p.start(7.5)
# Second number above is the refresh rate for the servo (in Hz)


# functions
def loadCFG():
    global controls
    CFGPath = "config.txt"
    try:
        with open(CFGPath, 'r') as f:
            lines = f.readlines()
            for lne in lines:
                ctrls = lne.split()
                if len(ctrls) != 3 or (ctrls[0] != 'k' and ctrls[0] != 'c'):
                    
                    print("ERROR! Invalid config")
                    exit(1)
                controls[ctrls[0]][ctrls[1]] = ctrls[2]
                print("controls[",ctrls[0],"][",ctrls[1], "] = ", ctrls[2])


    except IOError as e:
        print("Couldn't find config file. Using default config instead. Error code: (%s)." % e)
        controls['k']['S1D'] = '<Up>'
        controls['k']['S1U'] = '<Down>'
        controls['k']['S2T'] = '<space>'
        controls['c']['S1D'] = '<a>'
        controls['c']['S1U'] = '<y>'
        controls['c']['S2T'] = '<x>'

def writeCFG():
    global controls
    print("Editing config")
    print("Press to move servo 1 down, or press ENTER to keep existing keybind:")
    # read input here
    print("Press to move servo 1 up, or press ENTER to keep existing keybind:")
    # read input here
    print("Press button to toggle clamp, or press ENTER to keep existing keybind:")
    # read input here

    #open file
    with open("CFG", w) as f:
        for keyVal, ctrlType in controls.items():
            for fnctn, keybind in ctrlType.items():
                write(ctrlType, " ", fnctn, keybind)



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
    writeCFG()

def elbowUpPressed(toggleHoldVar):
    print('elbow up pressed')
    global currentPos
    if toggleHoldVar.get():
        while currentPos>2.5:
            currentPos = currentPos - 0.5
            p.ChangeDutyCycle(currentPos)
            print("toggleHoldVar, currentPos = ", currentPos)
            time.sleep(0.1)
    else:
        currentPos = max(currentPos - 0.5, 2.5)
        p.ChangeDutyCycle(currentPos)
        print("currentPos = ", currentPos)

def elbowDownPressed(toggleHoldVar):
    print('elbow down pressed')
    global currentPos
    if toggleHoldVar.get():
        while currentPos<12.5:
            currentPos = currentPos + 0.5
            p.ChangeDutyCycle(currentPos)
            print("toggleHoldVar, currentPos = ", currentPos)
            time.sleep(0.1)
    else:
        currentPos = min(12.5, currentPos + 0.5)
        p.ChangeDutyCycle(currentPos)
        print("currentPos = ",currentPos) 

def grabberPressed():
    global grabberIsOn
    grabberIsOn ^= 1
    print('grabber pressed: ' + str(grabberIsOn))
    GPIO.output(LEDNum, grabberIsOn)

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
    #app.bind("<Tab>", remapEvent)
    app.focus()

    #root.mainloop()

    return app

def main():
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

if __name__ == '__main__':
    main()

