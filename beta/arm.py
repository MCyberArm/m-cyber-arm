"""
arm.py

The primary class that represents the arm's servos and any connected GUIs
"""

# import RPi.GPIO as gpio
# import pygame
from tkinter import *
import constants
from constants import ServoName
from constants import ServoCommand
from constants import ControlType
from joint import Joint

class Arm:
    def __init__(self):
        self.root = Tk()
        self.curr_control_type = StringVar(self.root)
        self.locked = BooleanVar(self.root)
        
        self.load_control_config()
        self.setup_joints()
        
        # TODO: handle last pressed button sane as for curr_control_type and locked
        # self.last_pressed_button = StringVar(self.root)
    
    def load_control_config(self):
        self.controls = constants.CONTROLS_DEFAULT_CONFIG
        try:
            with open(constants.CONTROLS_CONFIG_PATH, 'r') as f:
                lines = f.readlines()
                if len(lines) != constants.NUM_CONTROLS:
                    raise IOError
                for line in lines:
                    ctrls = line.split()
                    if len(ctrls) != 4 or (ctrls[0] != ControlType.KEYBOARD.value and ctrls[0] != ControlType.CONTROLLER.value):
                        raise IOError
                    # TODO: check if control is valid
                    # format: [control_type] [servo_name] [servo_command] [control]
                    self.controls[ControlType(ctrls[0])][ServoName(ctrls[1])][ServoCommand(ctrls[2])] = ctrls[3]
        except IOError as e:
            print('ERROR: invalid config')
            print('Using default config instead')
            self.controls = constants.CONTROLS_DEFAULT_CONFIG
    
    def setup_joints(self):
        # gpio.setmode(gpio.BCM)
        # gpio.setwarnings(False)
        
        self.joints = {
            ServoName.GRABBER: Joint(ServoName.GRABBER.value, constants.GPIO_GRABBER, 2.5, constants.SERVO_POS_MIN, constants.SERVO_POS_MAX, constants.SERVO_POS_DELTA, self.curr_control_type, self.locked),
            ServoName.ELBOW: Joint(ServoName.ELBOW.value, constants.GPIO_ELBOW, 7.5, constants.SERVO_POS_MIN, constants.SERVO_POS_MAX, constants.SERVO_POS_DELTA, self.curr_control_type, self.locked),
            ServoName.WRIST: Joint(ServoName.WRIST.value, constants.GPIO_WRIST, 7.5, constants.SERVO_POS_MIN, constants.SERVO_POS_MAX, constants.SERVO_POS_DELTA, self.curr_control_type, self.locked)
        }
        
        # TODO: make this into a for loop iterating over each joint
        self.joints[ServoName.GRABBER].setup_key_binds(commands_to_keys = self.controls[ControlType.KEYBOARD][ServoName.GRABBER])
        self.joints[ServoName.ELBOW].setup_key_binds(commands_to_keys = self.controls[ControlType.KEYBOARD][ServoName.ELBOW])
        self.joints[ServoName.WRIST].setup_key_binds(commands_to_keys = self.controls[ControlType.KEYBOARD][ServoName.WRIST])
        
        self.joints[ServoName.GRABBER].setup_controller_binds(commands_to_buttons = self.controls[ControlType.CONTROLLER][ServoName.GRABBER])
        self.joints[ServoName.ELBOW].setup_controller_binds(commands_to_buttons = self.controls[ControlType.CONTROLLER][ServoName.ELBOW])
        self.joints[ServoName.WRIST].setup_controller_binds(commands_to_buttons = self.controls[ControlType.CONTROLLER][ServoName.WRIST])

    def handle_joystick(self):
        count = 1   # TEMP  
        # count = pygame.joystick.get_count()
        # if count == 1:
        #     # controller is detected
        #     controller = pygame.joystick.Joystick(0)
        #     controller.init()

        #     # only allows for one button to be pressed at a time
        #     button_pressed = False
        #     for joint in self.joints:
        #         if button_pressed:
        #             break
        #         for servo_command, button in joint.controller_controls:
        #             if controller.get_button(constants.CONTROLS_XBOX_BINDINGS[button]) == 1:
        #                 joint.move(ControlType.CONTROLLER, servo_command)
        #                 button_pressed = True
        #                 break
            
            