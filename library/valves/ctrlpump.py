import RPi.GPIO as GPIO
in1 = 16

def portinit():
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(in1, GPIO.OUT)


def pumpon():
    GPIO.output(in1, True)

def pumpoff():
    GPIO.output(in1, False)

