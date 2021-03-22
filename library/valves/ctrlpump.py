import RPi.GPIO as GPIO

def pumpon():
    in1 = 16
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(in1, GPIO.OUT)
    print('Pump on')
    GPIO.output(in1, True)
    GPIO.cleanup()

def pumpoff():
    in1=16
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(in1, GPIO.OUT)
    print('Pump off')
    GPIO.output(in1, False)
    GPIO.cleanup()

