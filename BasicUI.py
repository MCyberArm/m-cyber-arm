import time
import RPi.GPIO as GPIO
from tkinter import *

# constants
servoNum = 24
LEDNum = 25
controlTypes = {'Keyboard/Mouse', 'Controller'}

# global variables
grabberIsOn = 0
currentPos = 7.5

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
def setupGPIO():
    print("Proper Initialization will go here")
    # Above number is amount to change by?? (Double Check)

def controlMenuChoose(*args):
    print('chose control type ' + args[0])

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
    
    # keyboard events
    app.bind('<Up>', lambda: elbowUpPressed(toggleHoldVar)) 
    app.bind('<Down>', lambda: elbowDownPressed(toggleHoldVar))

    root.mainloop()

def main():
    setupGPIO()
    try:
        setupUI()
    except KeyboardInterrupt:
        GPIO.output(LEDNum, 0)
        p.stop()
        GPIO.cleanup()

    GPIO.output(LEDNum, 0)
    p.stop()
    GPIO.cleanup()

if __name__ == '__main__':
    main()

