"""
constants.py

Lists all constants used by this project
"""

from enum import Enum


# servo GPIO pin numbers on the Raspberry Pi
GPIO_GRABBER = 12
GPIO_WRIST = 18
GPIO_ELBOW = 24

# physical button GPIO pin numbers
GPIO_BUTTON_GRABBER = 15
GPIO_BUTTON_WRIST = 17
GPIO_BUTTON_ELBOW = 19

# servos
SERVO_HERTZ = 50
SERVO_POS_MIN = 2.5
SERVO_POS_MAX = 12.5
SERVO_POS_DELTA = 0.5

class ServoName(Enum):
    GRABBER = 'grabber'
    ELBOW = 'elbow'
    WRIST = 'wrist'

class ServoCommand(Enum):
    UP = 'up'
    DOWN = 'down'
    TOGGLE = 'toggle'

class ControlType(Enum):
    KEYBOARD = 'Keyboard'
    CONTROLLER = 'Controller'
    PHYSICAL = 'Physical Buttons'


# controls
CONTROLS_CONFIG_PATH = 'controls_config.txt'
NUM_CONTROLS = 10       # number of controls specified in controls config file
CONTROLS_DEFAULT_CONFIG = {
    ControlType.KEYBOARD: {
        ServoName.GRABBER: {ServoCommand.TOGGLE: '<space>'},
        ServoName.ELBOW: {ServoCommand.UP: '<Up>', ServoCommand.DOWN: '<Down>'},
        ServoName.WRIST: {ServoCommand.UP: '<Left>', ServoCommand.DOWN: '<Right>'}
    }, ControlType.CONTROLLER: {
        ServoName.GRABBER: {ServoCommand.TOGGLE: '<x>'},
        ServoName.ELBOW: {ServoCommand.UP: '<a>', ServoCommand.DOWN: '<y>'},
        ServoName.WRIST: {ServoCommand.UP: '<left_bumper>', ServoCommand.DOWN: '<right_bumper>'}
        # TODO: temporarily left and right bumpers on controller
    }
}

CONTROLS_XBOX_BINDINGS = {
    '<a>': 1,
    '<b>': 2,
    '<x>': 3,
    '<y>': 4,
    '<left_bumper>': 5,
    '<right_bumper>': 6
}

CONTROL_REMAP_KEY = '<Tab>'
CLOSE_WINDOW = '<Escape>'       # TODO: have escape exit each gui frame
