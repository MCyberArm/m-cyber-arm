"""
mouse_main.py

- Inputs mouse movements
- Controls arm with the attached mouse
"""

import time
from arm import Arm
import constants


def main():
    arm = Arm()
    
    arm.handle_mouse_input()

if __name__ == '__main__':
    main()
