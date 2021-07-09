import RPi.GPIO as GPIO
import time
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
    returnstatus, returnmessage = ctrlvalves.openvalve(klepsysteem,'tuinon')
    if returnstatus:
        return('Sproei tuinkant' + returnmessage)
    else:
        return('Error in switching tuinkant'+ returnmessage)

def sproeizwembad():
    returnstatus, returnmessage = ctrlvalves.openvalve(klepsysteem,'zwembadon')
    if returnstatus:
        return('Sproei zwembad' + returnmessage)
    else:
        return('Error in switching zwembad'+ returnmessage)

def startsproeier():
    returnstatus, returnmessage = ctrlvalves.openvalve(klepsysteem,'tuinon')
    if returnstatus:
        pumpon()
        return(True,'Sproei tuin' + returnmessage )
    else:
        return(False,'Pomp niet aan error is kleppen' + returnmessage)

def stopsproeier():
    pumpoff()
    returnstatus, returnmessage = ctrlvalves.openvalve(klepsysteem,'poweroff')

    if returnstatus:
        return(True,'Poweroff executed'+ returnmessage)
    else:
        #error in switching
        time.sleep(10)

        #try again 
        returnstatus, returnmessage = ctrlvalves.openvalve(klepsysteem,'poweroff')
        if returnstatus:
            return(True,'Poweroff completed'+ returnmessage) 
        else:
            return(False,'Error in poweroff kleppen'+ returnmessage)
