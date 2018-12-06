"""
joint.py

A controllable servo on the arm
"""

import pigpio
from tkinter import *
import time
import constants
from constants import ServoName
from constants import ServoCommand
from constants import ControlType


class Joint:
    def __init__(self, name, gpio_pin, init_pos, min_pos, max_pos, delta_pos, curr_control_type, locked, held, last_pressed_button_joint, last_pressed_button_command, pi, swap_rotate_enabled):
        self.name = name
        
        self.gpio_pin = gpio_pin
        self.pos = init_pos
        self.min_pos = min_pos
        self.max_pos = max_pos
        self.delta_pos = delta_pos
        
        self.rotate_direction = 1
        self.swap_rotate_enabled = swap_rotate_enabled
        
        self.curr_control_type = curr_control_type
        self.locked = locked
        self.held = held
        
        self.last_pressed_button_joint = last_pressed_button_joint
        self.last_pressed_button_command = last_pressed_button_command
        
        self.remap_ui_button_texts = {}
        
        self.pi = pi

    def setup_ui_button(self, app, command_type, text, row, column):
        button = Button(app, font = '-weight bold', text = text, command = lambda: self.move(None, command_type), width = 16, height = 4)
        button.grid(row = row, column = column, columnspan = 3)
    
    def setup_remap_ui_button(self, app, command_type, text, row, column):
        # TODO: change text in GUI when button is pressed to indicate that it's waiting for a new key
        text_variable = StringVar()
        text_variable.set(text)
        self.remap_ui_button_texts[command_type] = text_variable
        remap_button = Button(app, font = '-weight bold', textvariable = text_variable, command = lambda: remap_start(self, command_type), width = 24, height = 4)
        remap_button.grid(row = row, column = column, columnspan = 4)
    
    def move(self, control_type, command):
        if control_type != ControlType.MOUSE and control_type != ControlType.KEYBOARD and control_type != ControlType.CONTROLLER:
            print('ERROR: invalid control type when calling move() for', self.name)
        
        if self.locked.get():
            print(self.name, 'is locked')
            return
        
        print('command:', command.value)
        if control_type != ControlType.MOUSE:
            if control_type.value != self.curr_control_type.get():
                print(self.name + ': ' + control_type.value + ' is locked')
                return
            
            # TODO: figure out how to interrupt the held loop (by pressing same button again)
            if self.held.get():
                while True:
                    # update position
                    if command == ServoCommand.UP:
                        self.pos = max(self.pos - self.delta_pos, self.min_pos)
                    elif command == ServoCommand.DOWN:
                        self.pos = min(self.pos + self.delta_pos, self.max_pos)
                    elif command == ServoCommand.TOGGLE:
                        if self.pos == self.min_pos:
                            self.pos = self.max_pos
                        else:
                            self.pos = self.min_pos
                    
                    # update position of joint
                    print(self.name + ' ' + command.value + ':', self.pos)
                    self.pi.set_PWM_dutycycle(self.gpio_pin, self.pos)

                    if command == ServoCommand.UP and self.pos == self.min_pos: break
                    elif command == ServoCommand.DOWN and self.pos == self.max_pos: break
                    elif command == ServoCommand.TOGGLE: break
                    
                    time.sleep(0.2)
                return
            
        # update position
        if command == ServoCommand.UP:
            self.pos = max(self.pos - self.delta_pos, self.min_pos)
        elif command == ServoCommand.DOWN:
            self.pos = min(self.pos + self.delta_pos, self.max_pos)
        elif command == ServoCommand.TOGGLE:
            if not self.swap_rotate_enabled:
                if self.pos == self.min_pos:
                    self.pos = self.max_pos
                else:
                    self.pos = self.min_pos
            else:
                if self.rotate_direction == 1:
                    self.pos = min(self.pos + self.delta_pos, self.max_pos)
                else:
                    self.pos = max(self.pos - self.delta_pos, self.min_pos)
                
                if self.pos == self.min_pos or self.pos == self.max_pos:
                    print(self.name + ': change direction')
                    self.rotate_direction *= -1
        
        print(self.name + ' ' + command.value + ':', self.pos)
        
        # update position of joint
        self.pi.set_PWM_dutycycle(self.gpio_pin, self.pos)

def remap_start(joint, command):
    joint.last_pressed_button_joint.set(joint.name)
    joint.last_pressed_button_command.set(command.value)
    
