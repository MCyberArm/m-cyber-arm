"""
mouse_main.py

- Inputs mouse movements
- Controls arm with the attached mouse
"""

import time
from arm import Arm
import constants
from main_ui import init_main_ui
from remap_ui import init_remap_ui


def main():
# try:
    arm = Arm()
    
    # pygame.init()
    # pygame.joystick.init()
    
    while True:
        arm.handle_mouse_input()
        
        time.sleep(0.2)
# except:
    print('Closing application')
    # TODO: disable pwm and GPIO things here
    # TODO: save changes to controls file

if __name__ == '__main__':
    main()