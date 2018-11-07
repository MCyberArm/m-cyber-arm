"""
joint.py

A controllable servo on the arm
"""

import RPi.GPIO as gpio
import constants
from constants import ServoName
from constants import ServoCommand

class Joint:
    def __init__(self, name, gpio_pin, init_pos):
        self.name = name
        
        gpio.setup(gpio_pin, gpio.OUT)
        self.pwm = gpio.PWM(gpio_pin, constants.SERVO_HERTZ)
        self.pwm.start(init_pos)
        
        self.gpio_pin = gpio_pin
        self.pos = init_pos
    
    def setup_ui_button(self, command_type, text, row, column):
        self.button = Button(app, font = '-weight bold', text = text, command = lambda: move(command_type), width = 16, height = 4)
        self.button.grid(row = row, column = column, columnspan = 3)
    
    def setup_key_binds(self, commands_to_keys):
        # TODO
    
    def keyboard_bindings(self, app):
        # TODO
        app.bind(key, lambda e: move(command_type))
    
    def move(self, command):
        if command == ServoCommand.UP:
            # TODO
        elif command == ServoCommand.DOWN:
            # TODO
        elif command == ServoCommand.TOGGLE:
            # TODO
        else:
            # TODO: bad, throw error
            
        