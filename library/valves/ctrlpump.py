import RPi.GPIO as GPIO
in1 = 16

def portinit():
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(in1, GPIO.OUT)


def pumpon():
    portinit()
    GPIO.output(in1, True)

def pumpoff():
    portinit()
    GPIO.output(in1, False)

