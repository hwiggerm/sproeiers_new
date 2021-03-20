import RPi.GPIO as GPIO

in1 = 16

GPIO.setmode(GPIO.BOARD)
GPIO.setup(in1, GPIO.OUT)


def pumpon():
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(in1, GPIO.OUT)
    print('Pump on')
    GPIO.output(in1, True)
    GPIO.cleanup()

def pumpoff():
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(in1, GPIO.OUT)
    print('Pump off')
    GPIO.output(in1, False)
    GPIO.cleanup()

