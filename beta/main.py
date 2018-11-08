"""
main.py

- creates arm object
- main loop 
- handles gui updates
- handles xbox controller input
"""

# import pygame
import time
from arm import Arm
import constants
from main_ui import init_main_ui

def main():
	# initialize arm object
	arm = Arm()

	app = init_main_ui(arm)
	
	# pygame.init()
	# pygame.joystick.init()
	
	quit = False
	while not quit:
		app.update()
		
		time.sleep(0.2)


if __name__ == '__main__':
    main()
