"""
arm.py

The primary class that represents the arm's servos and any connected GUIs
"""

# import RPi.GPIO as gpio
from tkinter import *
import constants
from constants import ServoName
from constants import ServoCommand
from constants import ControlType
from joint import Joint

class Arm:
    def __init__(self):
        self.load_control_config()
        self.setup_joints()
        self.root = Tk()
        self.last_pressed_button = None
    
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
            print("ERROR: invalid config")
            print("Using default config instead. Error code: (%s)." % e)
            self.controls = constants.CONTROLS_DEFAULT_CONFIG
    
    def setup_joints(self):
        # gpio.setmode(gpio.BCM)
        # gpio.setwarnings(False)
        
        self.joints = {
            ServoName.GRABBER: Joint(name = ServoName.GRABBER.value, gpio_pin = constants.GPIO_GRABBER, init_pos = 2.5, min_pos = constants.SERVO_POS_MIN, max_pos = constants.SERVO_POS_MAX, delta_pos = constants.SERVO_POS_DELTA),
            ServoName.ELBOW: Joint(name = ServoName.ELBOW.value, gpio_pin = constants.GPIO_ELBOW, init_pos = 7.5, min_pos = constants.SERVO_POS_MIN, max_pos = constants.SERVO_POS_MAX, delta_pos = constants.SERVO_POS_DELTA),
            ServoName.WRIST: Joint(name = ServoName.WRIST.value, gpio_pin = constants.GPIO_WRIST, init_pos = 7.5, min_pos = constants.SERVO_POS_MIN, max_pos = constants.SERVO_POS_MAX, delta_pos = constants.SERVO_POS_DELTA)
        }
        
        self.joints[ServoName.GRABBER].setup_key_binds(commands_to_keys = self.controls[ControlType.KEYBOARD][ServoName.GRABBER])
        self.joints[ServoName.ELBOW].setup_key_binds(commands_to_keys = self.controls[ControlType.KEYBOARD][ServoName.ELBOW])
        self.joints[ServoName.WRIST].setup_key_binds(commands_to_keys = self.controls[ControlType.KEYBOARD][ServoName.WRIST])

