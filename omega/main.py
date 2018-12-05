"""
main.py

- creates arm object
- main loop 
- handles gui updates, frame switches
- handles xbox controller input
"""

import pygame
import time
from arm import Arm
import constants
from main_ui import init_main_ui
from remap_ui import init_remap_ui


def main():
    arm = Arm()
    
    app = None
    
    # pygame.init()
    # pygame.joystick.init()
    
    while True:
        if arm.remapping.get() == -1:
            print('switch to main ui')
            if app:
                app.destroy()
            app = init_main_ui(arm)
            arm.remapping.set(0)
        elif arm.remapping.get() == 1:
            print('switch to remap ui')
            if app:
                app.destroy()
            app = init_remap_ui(arm)
            arm.remapping.set(0)
        elif arm.remapping.get() == 2:
            app.destroy()
            arm.root.destroy()
            break
        
        app.update()
        
        arm.handle_joystick()
        
        arm.handle_physical_buttons()
        
        time.sleep(0.2)
    
    arm.save_control_config()
    print('Closing application')

if __name__ == '__main__':
    main()
