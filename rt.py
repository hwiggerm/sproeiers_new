import RPi.GPIO as GPIO
import time

in1 = 16

GPIO.setmode(GPIO.BOARD)
GPIO.setup(in1, GPIO.OUT)

print('Pump on')
GPIO.output(in1, True)
time.sleep(10)


print('Pump off')
GPIO.output(in1, False)


#cleanup
GPIO.cleanup()
