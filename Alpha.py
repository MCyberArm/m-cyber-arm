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
	GPIO.set(portNum, GPIO.OUT)

def handleInput():
	print('Hello, this program is designed to control a basic mechanical arm through human input. Type "help" for usage instructions."
	inputString = input("Enter a command here, or type  'help' for more options")
	if inputString == "help" || "Help":
		printHelp()

def printHelp():
	print("Help Menu Here")


def main():
	handleInput()



if __name__ == '__main__':
	main()
