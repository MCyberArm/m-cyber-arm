import time
import RPi.GPIO as GPIO
from tkinter import *

# constants
portNum = 24
controlTypes = {'Keyboard/Mouse', 'Controller'}

# global variables
grabberIsOn = 0

root = Tk()
controlVar = StringVar(root)
toggleHoldVar = IntVar(root)

# functions
def setupGPIO():
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    GPIO.setup(portNum, GPIO.OUT)

def controlMenuChoose(*args):
    print('chose control type ' + args[0])

def elbowUpPressed():
    print('elbow up pressed')

def elbowDownPressed():
    print('elbow down pressed')

def grabberPressed():
    global grabberIsOn
    grabberIsOn ^= 1
    print('grabber pressed: ' + str(grabberIsOn))
    GPIO.output(portNum, grabberIsOn)

def setupUI():
    # make window
    root.title('M Cyber Arm UI')
    
    # make frame
    app = Frame(root)
    app.grid()
    app.configure(background = 'gray')

    # title label
    title = Label(app, text = 'M Cyber Arm UI', width = 30, font = '-weight bold')
    title.grid(row = 0, column = 0, columnspan = 3)

    # control type dropdown menu
    controlVar.set('Keyboard/Mouse')
    controlMenu = OptionMenu(app, controlVar, *controlTypes, command = controlMenuChoose)
    controlMenu.grid(row = 1, column = 0, columnspan = 3)

    # checkbox for whether to hold directional button for input
    toggleHoldCheckbox = Checkbutton(app, font = '-weight bold', text = 'Toggle Button Holding', variable = toggleHoldVar)
    toggleHoldCheckbox.grid(row = 2, column = 0, columnspan = 3)

    # buttons for arm movement
    elbowUpButton = Button(app, font = '-weight bold', text = 'Elbow Up', command = elbowUpPressed)
    elbowUpButton.grid(row = 3, column = 0, columnspan = 3)

    elbowDownButton = Button(app, font = '-weight bold', text = 'Elbow Down', command = elbowDownPressed)
    elbowDownButton.grid(row = 4, column = 0, columnspan = 3)

    grabberButton = Button(app, font = '-weight bold', text = 'Grab', command = grabberPressed)
    grabberButton.grid(row = 5, column = 0, columnspan = 3)

    root.mainloop()

def main():
    setupGPIO()
 
    try:
        setupUI()
    except KeyboardInterrupt:
        GPIO.output(portNum, 0)
        GPIO.cleanup()

    GPIO.output(portNum, 0)
    GPIO.cleanup()

if __name__ == '__main__':
    main()

