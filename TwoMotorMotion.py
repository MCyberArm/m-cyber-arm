import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)

GPIO.setup(24, GPIO.OUT)

try:
	while True:
		GPIO.output(24, 1)
		time.sleep(0.0015)
		GPIO.output(24, 0)

		time.sleep(2)
except KeyboardInterrupt:
	GPIO.cleanup()

except:
	print "Something weird happened"
	GPIO.cleanup()
