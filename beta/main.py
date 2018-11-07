"""
main.py

- creates arm object
- main loop 
- handles gui updates
- handles xbox controller input
"""

import pygame
from arm import Arm
import constants
from main_ui import init_main_ui

def main():
	# initialize arm object
	arm = Arm()

	app = init_main_ui()
	pygame.init()
	pygame.joystick.init()

if __name__ == '__main__':
    main()
