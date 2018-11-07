"""
constants.py

Lists all constants used by this project
"""

# servo GPIO pin numbers on the Raspberry Pi
GPIO_GRABBER = 12
GPIO_WRIST = -1			# TODO: assign GPIO pin
GPIO_ELBOW = 24

# controls
CONTROLS_CONFIG_PATH = "controls_config.txt"
NUM_CONTROLS = 10		# number of controls specified in controls config file
CONTROLS_DEFAULT_CONFIG = {
	'k': {
		'grabber_toggle': '<space>',
		'elbow_down': '<Up>',
		'elbow_up': '<Down>'
		'wrist_left': '<Left>',
		'wrist_right': '<Right>'
	}, 'c': {
		'grabber_toggle': '<x>',
		'elbow_down': '<a>',
		'elbow_up': '<y>',
		'wrist_left': '<2>',	# TODO: temporarily left and right bumpers on controller
		'wrist_right': '<7>'
	}
}
CONTROL_TYPES = {'Keyboard', 'Controller'}

# servos
SERVO_HERTZ = 50
