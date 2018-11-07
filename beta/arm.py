"""
arm.py

The primary class that represents the arm's servos and any connected GUIs
"""

import RPi.GPIO as gpio
from tkinter import *
import constants
from constants import ServoName
from constants import ServoCommand
from joint import Joint

class Arm:
    def __init__(self):
        load_control_config()
        setup_joints()
        self.root = Tk()
    
    def load_control_config(self):
        self.controls = constants.CONTROLS_DEFAULT_CONFIG
        try:
            with open(constants.CONFIG_PATH, 'r') as f:
                lines = f.readlines()
                if len(lines) != constants.NUM_CONTROLS:
                    raise IOError
                for line in lines:
                    ctrls = line.split()
                    if len(ctrls) != 4 or (ctrls[0] != ControlType.KEYBOARD and ctrls[0] != ControlType.CONTROLLER):
                        raise IOError
                    # TODO: check if control is valid
                    # format: [control_type] [servo_name] [servo_command] [control]
                    self.controls[ctrls[0]][ctrls[1]][ctrls[2]] = ctrls[3]
        except IOError as e:
            print("ERROR: invalid config")
            print("Using default config instead. Error code: (%s)." % e)
            self.controls = constants.CONTROLS_DEFAULT_CONFIG
    
    def setup_joints(self):
        gpio.setmode(gpio.BCM)
        gpio.setwarnings(False)
        
        self.joints = {
            ServoName.GRABBER: Joint(name = ServoName.GRABBER, gpio_pin = constants.GPIO_GRABBER, init_pos = 2.5),
            ServoName.ELBOW: Joint(name = ServoName.ELBOW, gpio_pin = constants.GPIO_ELBOW, init_pos = 7.5),
            ServoName.WRIST: Joint(name = ServoName.WRIST, gpio_pin = constants.GPIO_WRIST, init_pos = 7.5)
        }
        
        # TODO
        self.joints[ServoName.GRABBER].setup_key_binds(commands_to_keys = self.controls[ControlType.KEYBOARD][ServoName.GRABBER])
        self.joints[ServoName.ELBOW].setup_key_binds(commands_to_keys = self.controls[ControlType.KEYBOARD][ServoName.ELBOW])
        self.joints[ServoName.WRIST].setup_key_binds(commands_to_keys = self.controls[ControlType.KEYBOARD][ServoName.WRIST])

