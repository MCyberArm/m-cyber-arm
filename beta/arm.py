"""
arm.py

The primary class that represents the arm's servos and any connected GUIs
"""

import RPi.GPIO as GPIO
from tkinter import *
import constants

class Arm:
	def __init__(self):
		setupGPIO()
		root = Tk()
	
	def setupGPIO():
		GPIO.setmode(GPIO.BCM)
		GPIO.setwarnings(False)
		
		GPIO.setup(constants.GPIO_GRABBER, GPIO.OUT)
		GPIO.setup(constants.GPIO_ELBOW, GPIO.OUT)
		# GPIO.setup(constants.GPIO_WRIST, GPIO.OUT)
		
		self.grabberPWM = GPIO.PWM(grabberNum, 50)
		self.elbowPWM = GPIO.PWM(elbowNum, 50)
		
		self.grabberPWM.start(2.5)
		self.elbowPWM.start(7.5)
	
	
