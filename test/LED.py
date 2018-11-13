import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BCM)
#GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)
GPIO.setup(24,GPIO.OUT)
print "LED on"
GPIO.output(24,1)
time.sleep(1)
print "LED off"
GPIO.output(24,0)
