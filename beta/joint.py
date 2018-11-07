"""
joint.py

A controllable servo on the arm
"""

import RPi.GPIO as gpio
import constants
from constants import ServoName
from constants import ServoCommand

class Joint:
    def __init__(self, name, gpio_pin, init_pos, min_pos, max_pos, delta_pos):
        self.name = name
        
        gpio.setup(gpio_pin, gpio.OUT)
        self.pwm = gpio.PWM(gpio_pin, constants.SERVO_HERTZ)
        self.pwm.start(init_pos)
        
        self.gpio_pin = gpio_pin
        self.pos = init_pos
        self.min_pos = min_pos
        self.max_pos = max_pos
        self.delta_pos = delta_pos
        
        self.locked = False
        self.held = False
    
    def setup_ui_button(self, app, command_type, text, row, column):
        self.button = Button(app, font = '-weight bold', text = text, command = lambda: move(command_type), width = 16, height = 4)
        self.button.grid(row = row, column = column, columnspan = 3)
    
    def setup_remap_ui_button(self, app, command_type, text, row, column):
        self.remap_button = Button(app, font = '-weight bold', text = text, command = lambda: move(command_type), width = 16, height = 4)
        elbowUpButton = Button(app, font = '-weight bold', text = 'Elbow Up', command = lambda: lastPressedButton = 'S1U', width = 16, height = 4)
        elbowUpButton.grid(row = 3, column = 0, columnspan = 3)
    
    def setup_key_binds(self, commands_to_keys):
        self.controls = commands_to_keys
    
    def bind_keys(self, app):
        for servo_command, key in self.controls:
            app.bind(key, lambda e: move(servo_command))
    
    def move(self, command):
        if self.locked:
            return
        
        # TODO: handle when held is set to true
        
        if command == ServoCommand.UP:
            self.pos = max(self.pos - self.delta_pos, delta.min_pos)
        elif command == ServoCommand.DOWN:
            self.pos = min(self.pos + self.delta_pos, delta.max_pos)
        elif command == ServoCommand.TOGGLE:
            # TODO: deal with case where joint is almost closed and then gets toggled (should open)
            if self.pos == self.min_pos:
                self.pos = self.max_pos
            else:
                self.pos = self.min_pos
        else:
            # TODO: bad; throw error
        
        # update position of joint
        self.pwm.ChangeDutyCycle(self.pos)
