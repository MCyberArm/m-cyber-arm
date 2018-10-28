"""
 Authors

__PUT__YOUR__NAMES__HERE!!!

Neil Kenney, nfkenney@umich.edu




"""


import RPi.GPIO as GPIO
import time
import mscvrt
portNum = 24


def setupGPIO():
	GPIO.setmode(GPIO.BCM)
	#GPIO.set(portNum, GPIO.OUT)
	GPIO.setwarnings(False)
	GPIO.setup(portNum, GPIO.OUT)

def handleInput():
	print('Hello, this program is designed to control a basic mechanical arm through human input. Type "h" for usage instructions.\n')
	while True:
		inputString = input("Enter a command here, or type  'help' for more options\n")
		if inputString == 'h' or inputString == 'H':
			printHelp()
		elif(inputString == 'w' or inputString == "W" or inputString == "S" or inputString == 's'):
			moveArm(inputString)
		else:
			print('ERROR! Invalid Input. Type "help" for controls')
			printHelp()

def printHelp():
	print("Help Menu Here")
	print("Controls:")
	print("Key			Function")
	print("W			Move Arm Forward")
	print("S			Move Arm Backward")
	print("H			Print this help message")
	print("Q			Quit the Application")

def main():
	setupGPIO()
	try:
		handleInput()
	except KeyboardInterrupt:
		GPIO.output(portNum, 0)
		GPIO.cleanup()

def moveArm(key):
	if key == "w" or key=='W':
		#Move upwards
		GPIO.output(portNum, 1)
		print("Moving Arm Forwards")
	elif key  == 's' or key == 'S':
		# Move backwards
		GPIO.output(portNum, 0)
		print("Moving Arm Backwards")
	else:
		print("ERROR! Invalid Input")


if __name__ == '__main__':
	main()
