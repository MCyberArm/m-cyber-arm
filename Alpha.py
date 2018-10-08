"""
 Authors

__PUT__YOUR__NAMES__HERE!!!

Neil Kenney, nfkenney@umich.edu




"""


import RPi.GPIO as GPIO
import time

portNum = 24


def setupGPIO():
	GPIO.setmode(GPIO.BCM)
	#GPIO.set(portNum, GPIO.OUT)
	GPIO.setwarnings(False)
	GPIO.setup(portNum, GPIO.OUT)

def handleInput():
	print('Hello, this program is designed to control a basic mechanical arm through human input. Type "help" for usage instructions.')
	while true:
		inputString = input("Enter a command here, or type  'help' for more options")
		if inputString == "help" or inputString == "Help":
			printHelp()
		elif(char(inputString) == 'w' or char(intputString) == "W" or char(inputString) == "S" or char(inputString) == 'w'):
			moveArm(char(inputString))
		else:
			print("ERROR! Invalid Input")
			printHelp()

def printHelp():
	print("Help Menu Here")
	print("Controls:"):
	print("Key			Function")
	print("W			Move Arm Forward")
	print("S			Move Arm Backward")
	print("H			Print this help message")

def main():
	handleInput()


def moveArm(char key):
	if key == "w" || key=='W':
		#Move upwards
		GPIO.output(portNum, 1)
		print("Moving Arm Forwards")
	elif key  == 's' || key == 'S':
		# Move backwards
		GPIO.output(portNum, 0)
		print("Moving Arm Backwards")
	else:
		print("ERROR! Invalid Input")


if __name__ == '__main__':
	main()
