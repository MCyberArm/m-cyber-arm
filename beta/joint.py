"""
joint.py

A controllable servo on the arm
"""

import RPi.GPIO as gpio
import constants

class Joint:
	def __init__(self, gpio_pin, init_pos):
		gpio.setup(gpio_pin, gpio.OUT)
		self.pwm = gpio.PWM(gpio_pin, constants.SERVO_HERTZ)
		self.pwm.start(init_pos)
		
		self.gpio_pin = gpio_pin
		self.pos = init_pos
		