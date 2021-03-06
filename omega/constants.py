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
SERVO_POS_MIN = 500
SERVO_POS_MAX = 2500
SERVO_POS_DELTA = 200


# initial, min, and max servo locations
GRABBER_POS_INIT = 700
GRABBER_POS_MIN = 700
GRABBER_POS_MAX = 2000

ELBOW_POS_INIT = SERVO_POS_MIN
ELBOW_POS_MIN =  SERVO_POS_MIN
ELBOW_POS_MAX = SERVO_POS_MAX

WRIST_POS_INIT = SERVO_POS_MIN
WRIST_POS_MIN = SERVO_POS_MIN
WRIST_POS_MAX = SERVO_POS_MAX


class ServoName(Enum):
    GRABBER = 'grabber'
    ELBOW = 'elbow'
    WRIST = 'wrist'
    ALL = 'all'

class ServoCommand(Enum):
    UP = 'up'
    DOWN = 'down'
    TOGGLE = 'toggle'
    MOVE = 'move'
    LOCK = 'lock'

class ControlType(Enum):
    KEYBOARD = 'Keyboard'
    CONTROLLER = 'Controller'
    MOUSE = 'Mouse'

class MouseControl(Enum):
    CLICK = 'click'
    SCROLL = 'scroll'

class MouseBind(Enum):
    LEFT = 'left'
    MIDDLE = 'middle'
    RIGHT = 'right'
    UP = 'up'
    DOWN = 'down'


# controls
CONTROLS_CONFIG_PATH = 'controls_config.txt'
NUM_CONTROLS = 15       # number of controls specified in controls config file
CONTROLS_DEFAULT_CONFIG = {
    ControlType.KEYBOARD: {
        ServoName.GRABBER: {ServoCommand.TOGGLE: '<space>'},
        ServoName.ELBOW: {ServoCommand.UP: '<Up>', ServoCommand.DOWN: '<Down>'},
        ServoName.WRIST: {ServoCommand.UP: '<Left>', ServoCommand.DOWN: '<Right>'}
    }, ControlType.CONTROLLER: {
        ServoName.GRABBER: {ServoCommand.TOGGLE: '<x>'},
        ServoName.ELBOW: {ServoCommand.UP: '<a>', ServoCommand.DOWN: '<y>'},
        ServoName.WRIST: {ServoCommand.UP: '<left_bumper>', ServoCommand.DOWN: '<right_bumper>'}
    }
}

CONTROLS_MOUSE_DEFAULT_CONFIG = {
    MouseControl.CLICK: {
        MouseBind.RIGHT: {ServoName.GRABBER: ServoCommand.TOGGLE},
        MouseBind.MIDDLE: {ServoName.ALL: ServoCommand.LOCK},
        MouseBind.LEFT: {ServoName.WRIST: ServoCommand.MOVE}},
    MouseControl.SCROLL: {MouseBind.UP: {ServoName.ELBOW: ServoCommand.UP}, MouseBind.DOWN: {ServoName.ELBOW: ServoCommand.DOWN}}
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
