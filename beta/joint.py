"""
joint.py

A controllable servo on the arm
"""

# import RPi.GPIO as gpio
from tkinter import *
import constants
from constants import ServoName
from constants import ServoCommand
from constants import ControlType

class Joint:
    def __init__(self, name, gpio_pin, init_pos, min_pos, max_pos, delta_pos, curr_control_type, locked, last_pressed_button_joint, last_pressed_button_command):
        self.name = name
        
        self.gpio_pin = gpio_pin
        self.pos = init_pos
        self.min_pos = min_pos
        self.max_pos = max_pos
        self.delta_pos = delta_pos
        
        self.curr_control_type = curr_control_type
        self.locked = locked
        
        self.last_pressed_button_joint = last_pressed_button_joint
        self.last_pressed_button_command = last_pressed_button_command
        
        self.remap_ui_button_texts = {}
        
        # gpio.setup(gpio_pin, gpio.OUT)
        # self.pwm = gpio.PWM(gpio_pin, constants.SERVO_HERTZ)
        # self.pwm.start(init_pos)
    
    def setup_ui_button(self, app, command_type, text, row, column):
        self.button = Button(app, font = '-weight bold', text = text, command = lambda: self.move(None, command_type), width = 16, height = 4)
        self.button.grid(row = row, column = column, columnspan = 3)
    
    def setup_remap_ui_button(self, app, command_type, text, row, column):
        # TODO: change text in GUI when button is pressed to indicate that it's waiting for a new key
        text_variable = StringVar()
        text_variable.set(text)
        self.remap_ui_button_texts[command_type] = text_variable
        self.remap_button = Button(app, font = '-weight bold', textvariable = text_variable, command = lambda: remap_start(self, command_type), width = 24, height = 4)
        self.remap_button.grid(row = row, column = column, columnspan = 4)

    def update_key_binds(self, commands_to_keys):
        self.keyboard_controls = commands_to_keys
    
    def setup_controller_binds(self, commands_to_buttons):
        self.controller_controls = commands_to_buttons
    
    def move(self, control_type, command):
        if control_type != None and control_type.value != self.curr_control_type.get():
            print(self.name + ': ' + control_type.value + ' is locked')
            return
        
        if self.locked.get():
            print(self.name, 'is locked')
            return
        
        # TODO: add feature for button holding (gradual change in movement automatically)
        
        print('command:', command.value)
        
        if command == ServoCommand.UP:
            self.pos = max(self.pos - self.delta_pos, self.min_pos)
        elif command == ServoCommand.DOWN:
            self.pos = min(self.pos + self.delta_pos, self.max_pos)
        elif command == ServoCommand.TOGGLE:
            # TODO: deal with case where joint is almost closed and then gets toggled (should open)
            if self.pos == self.min_pos:
                self.pos = self.max_pos
            else:
                self.pos = self.min_pos
        # else:
            # TODO: bad; throw error
        
        print(self.name + ' ' + command.value + ':', self.pos)
        
        # update position of joint
        # self.pwm.ChangeDutyCycle(self.pos)


def remap_start(joint, command):
    joint.last_pressed_button_joint.set(joint.name)
    joint.last_pressed_button_command.set(command.value)
    