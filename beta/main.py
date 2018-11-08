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
from remap_ui import init_remap_ui


def main():
# try:
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
        
        time.sleep(0.2)
# except:
    print('Closing application')
    # TODO: disable pwm and GPIO things here
    # TODO: save changes to controls file

if __name__ == '__main__':
    main()
