import RPi.GPIO as GPIO
import os
from library.valves import ctrlvalves

in1 = 16


klepsysteem = os.environ.get('KLEPSYSTEEM')


def portinit():
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(in1, GPIO.OUT)


def pumpon():
    GPIO.output(in1, True)

def pumpoff():
    GPIO.output(in1, False)


def sproeituin():
    if ctrlvalves.openvalve(klepsysteem,'tuinon'):
        return('Proei  tuin')
    else:
        return('Error in switching tuin')

def sproeizwembad():
    if ctrlvalves.openvalve(klepsysteem,'zwembadon'):
        return('Sproei zwembad')
    else:
        return('Error in switching zwembad')

def startsproeier():
    if ctrlvalves.openvalve(klepsysteem,'tuinon'):
        pumpon()
        return('Sproei tuin')
    else:
        return('Pomp niet aan error is kleppen')

def stopsproeier():
    pumpoff()

    if ctrlvalves.openvalve(klepsysteem,'poweroff'):
        return('Run Poweroff')
    else:
        #error in switching
        time.sleep(10)
        #try again 
        if ctrlvalves.openvalve(klepsysteem,'poweroff'):
            return('Poweroff completed') 
        else:
            return('Error in poweroff kleppen')
