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
    try:
        arm = Arm()

        app = init_main_ui(arm)
        
        # pygame.init()
        # pygame.joystick.init()
        
        while True:
            app.update()
            
            arm.handle_joystick()
            
            time.sleep(0.2)
    except:
        print('Closing application')
        # TODO: disable pwm and GPIO things here    

if __name__ == '__main__':
    main()
