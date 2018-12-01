"""
constants.py

Lists all constants used by this project
"""

from enum import Enum


# servo GPIO pin numbers on the Raspberry Pi
GPIO_GRABBER = 24
GPIO_WRIST = 12
GPIO_ELBOW = 18


# servos
SERVO_HERTZ = 50
SERVO_POS_MIN = 2.5
SERVO_POS_MAX = 12.5
SERVO_POS_DELTA = 0.5


# initial, min, and max servo locations
GRABBER_POS_INIT = 8.75
GRABBER_POS_MIN = 8.75
GRABBER_POS_MAX = 11

ELBOW_POS_INIT = 7.5
ELBOW_POS_MIN = SERVO_POS_MIN
ELBOW_POS_MAX = SERVO_POS_MAX

WRIST_POS_INIT = 7.5
WRIST_POS_MIN = SERVO_POS_MIN
WRIST_POS_MAX = SERVO_POS_MAX


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
    MOUSE = 'Mouse'


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
    # }, ControlType.MOUSE: {
    #     ServoName.GRABBER: {ServoCommand.TOGGLE: 'right'},
    #     ServoName.ELBOW: {ServoCommand.UP: 'scroll_up', ServoCommand.DOWN: 'scroll_down'},
    # }
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
