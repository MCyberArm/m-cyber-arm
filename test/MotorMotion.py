import RPi.GPIO as GPIO
import time

servoPIN = 24
GPIO.setmode(GPIO.BCM)
GPIO.setup(servoPIN, GPIO.OUT)

p = GPIO.PWM(servoPIN, 50) # GPIO 17 for PWM with 50Hz
p.start(10) # Initialization

try:
    i = 2.5
    while i <= 12.5:    
        p.ChangeDutyCycle(i)
        print("Set:", i)
        i += 1
        time.sleep(0.5)
        break
except KeyboardInterrupt:
  p.stop()
  GPIO.cleanup()
