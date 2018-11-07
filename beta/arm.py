"""
arm.py

The primary class that represents the arm's servos and any connected GUIs
"""

import RPi.GPIO as gpio
from tkinter import *
import constants
from joint import Joint

class Arm:
    def __init__(self):
        load_control_config()
        setup_joints()
        self.root = Tk()
    
    def load_control_config():
        self.controls = {'k': {}, 'c': {}}
        try:
            with open(constants.CONFIG_PATH, 'r') as f:
                lines = f.readlines()
                if len(lines) != constants.NUM_CONTROLS:
                    raise IOError
                for line in lines:
                    ctrls = line.split()
                    if len(ctrls) != 3 or (ctrls[0] != 'k' and ctrls[0] != 'c'):
                        raise IOError
                    # TODO: check if controls key is valid (ctrls[1]) (e.g. grabber_toggle)
                    self.controls[ctrls[0]][ctrls[1]] = ctrls[2]
        except IOError as e:
            print("ERROR: invalid config")
            print("Using default config instead. Error code: (%s)." % e)
            self.controls = constants.CONTROLS_DEFAULT_CONFIG
    
    def setup_joints():
        gpio.setmode(gpio.BCM)
        gpio.setwarnings(False)
        
        self.joints = [
            Joint(constants.GPIO_GRABBER, 2.5),
            Joint(constants.GPIO_ELBOW, 7.5),
            Joint(constants.GPIO_WRIST, 7.5)
        ]
    
    
