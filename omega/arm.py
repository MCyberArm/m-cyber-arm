"""
arm.py

The primary class that represents the arm's servos and any connected GUIs
"""

import pigpio
import pygame
from pynput import mouse
from tkinter import *
import constants
from constants import ServoName
from constants import ServoCommand
from constants import ControlType
from constants import MouseControl
from constants import MouseBind
from joint import Joint

class Arm:
    def __init__(self, curr_control_type):
        self.root = Tk()
        
        self.curr_control_type = StringVar(self.root)
        self.curr_control_type.set(curr_control_type)
        
        self.locked = SystemLock(False)
        
        self.held = BooleanVar(self.root)
        self.held.set(False)
        
        # remapping: -1 for not remapping, 1 for remapping, 0 for no current transition between frames, 2 for end of application
        self.remapping = IntVar(self.root)
        self.remapping.set(-1)
        
        self.last_pressed_button_joint = StringVar(self.root)
        self.last_pressed_button_command = StringVar(self.root)
        
        self.load_control_config()
        self.setup_joints()
    
    def load_control_config(self):
        self.controls = constants.CONTROLS_DEFAULT_CONFIG
        self.mouse_controls = constants.CONTROLS_MOUSE_DEFAULT_CONFIG
        try:
            with open(constants.CONTROLS_CONFIG_PATH, 'r') as f:
                lines = f.readlines()
                if len(lines) != constants.NUM_CONTROLS:
                    raise IOError('Number of controls in config (' + str(len(lines)) + ') should be ' + str(constants.NUM_CONTROLS))
                for line in lines:
                    ctrls = line.split()
                    
                    # TODO: check if control is valid
                    if len(ctrls) == 5 and ctrls[0] == ControlType.MOUSE.value:
                        # format in file: [control_type] [servo_name] [servo_command] [mouse_control] [mouse_bind]
                        self.mouse_controls[MouseControl(ctrls[3])][MouseBind(ctrls[4])][ServoName(ctrls[1])] = ServoCommand(ctrls[2])
                    elif len(ctrls) == 4 and (ctrls[0] == ControlType.KEYBOARD.value or ctrls[0] == ControlType.CONTROLLER.value):
                        # format in file: [control_type] [servo_name] [servo_command] [control]
                        self.controls[ControlType(ctrls[0])][ServoName(ctrls[1])][ServoCommand(ctrls[2])] = ctrls[3]
                    else:
                        raise IOError(ctrls)

        except IOError as e:
            print('ERROR: invalid config:', repr(e))
            print('Using default config instead')
            self.controls = constants.CONTROLS_DEFAULT_CONFIG
            self.mouse_controls = constants.CONTROLS_MOUSE_DEFAULT_CONFIG
    
    def save_control_config(self):
        with open(constants.CONTROLS_CONFIG_PATH, 'w') as f:
            for control_type, servos in self.controls.items():
                for servo_name, servo_commands in servos.items():
                    for servo_command, binding in servo_commands.items():
                        f.write(control_type.value + " " + servo_name.value + " " + servo_command.value + " " + binding + "\n")
    
    def setup_joints(self):
        pi = pigpio.pi()
 
        # pi.set_mode(constants.GPIO_GRABBER, pigpio.OUTPUT)
        # pi.set_mode(constants.GPIO_ELBOW, pigpio.OUTPUT)
        # pi.set_mode(constants.GPIO_WRIST, pigpio.OUTPUT)
 
        self.joints = {
            ServoName.GRABBER: Joint(ServoName.GRABBER.value, constants.GPIO_GRABBER, constants.GRABBER_POS_INIT, constants.GRABBER_POS_MIN, constants.GRABBER_POS_MAX, constants.SERVO_POS_DELTA, self.curr_control_type, self.locked, self.held, self.last_pressed_button_joint, self.last_pressed_button_command, pi, False),
            ServoName.ELBOW: Joint(ServoName.ELBOW.value, constants.GPIO_ELBOW, constants.ELBOW_POS_INIT, constants.ELBOW_POS_MIN, constants.ELBOW_POS_MAX, constants.SERVO_POS_DELTA, self.curr_control_type, self.locked, self.held, self.last_pressed_button_joint, self.last_pressed_button_command, pi, False),
            ServoName.WRIST: Joint(ServoName.WRIST.value, constants.GPIO_WRIST, constants.WRIST_POS_INIT, constants.WRIST_POS_MIN, constants.WRIST_POS_MAX, constants.SERVO_POS_DELTA, self.curr_control_type, self.locked, self.held, self.last_pressed_button_joint, self.last_pressed_button_command, pi, True)
        }
        
    def handle_joystick(self):
        count = pygame.joystick.get_count()
        if count == 1:
            # controller is detected
       	    controller = pygame.joystick.Joystick(0)
            controller.init()

            # only allows for one button to be pressed at a time
            button_pressed = False
            for servo_name, commands in self.controls[ControlType.CONTROLLER].items():
                if button_pressed:
                    break
                for servo_command, button in commands.items():
                    if controller.get_button(constants.CONTROLS_XBOX_BINDINGS[button]) == 1:
                        joint.move(ControlType.CONTROLLER, servo_command)
                        button_pressed = True
                        break
    
    def handle_physical_buttons(self):
        TODO = 1
        # TODO: handle physical buttons

    def handle_mouse_input(self):
        print('handle mouse input')
        with mouse.Listener(
            on_move = lambda x, y: self.mouse_move(x, y),
            on_click = lambda x, y, button, pressed: self.mouse_click(x, y, button, pressed),
            on_scroll = lambda x, y, dx, dy: self.mouse_scroll(x, y, dx, dy)
        ) as listener:
            listener.join()
    
    def mouse_move(self, x, y):
        pass

    def mouse_click(self, x, y, button, pressed):
        if pressed:
            if button == mouse.Button.left:
                print('mouse: left pressed')
                for servo_name, servo_command in self.mouse_controls[MouseControl.CLICK][MouseBind.LEFT].items():
                    self.joints[servo_name].move(ControlType.MOUSE, servo_command)
            elif button == mouse.Button.right:
                print('mouse: right pressed')
                print(self.mouse_controls)
                for servo_name, servo_command in self.mouse_controls[MouseControl.CLICK][MouseBind.RIGHT].items():
                    self.joints[servo_name].move(ControlType.MOUSE, servo_command)
            elif button == mouse.Button.middle:
                print('mouse: middle pressed')
                self.locked.toggle()
                print('set lock to true' if self.locked.get() else 'set lock to false')
                
                # TODO: add joint to self.joints for ServoName.ALL???
        
    
    def mouse_scroll(self, x, y, dx, dy):
        if dy > 0:
            print('mouse: scroll up')
            for servo_name, servo_command in self.mouse_controls[MouseControl.SCROLL][MouseBind.UP].items():
                self.joints[servo_name].move(ControlType.MOUSE, servo_command)
        elif dy < 0:
            print('mouse: scroll down')
            for servo_name, servo_command in self.mouse_controls[MouseControl.SCROLL][MouseBind.DOWN].items():
                self.joints[servo_name].move(ControlType.MOUSE, servo_command)
    

class SystemLock:
    def __init__(self, init_locked):
        self.locked = init_locked
    
    def lock(self):
        self.locked = True
    
    def unlock(self):
        self.locked = False
    
    def toggle(self):
        self.locked = not self.locked
    
    def get(self):
        return self.locked
