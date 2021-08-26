import RPi.GPIO as GPIO
import time
import os
import sys
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
        return(True,'Sproei tuinkant ' + returnmessage)
    else:
        return(False,'Error in switching tuinkant '+ returnmessage)

def sproeizwembad():
    returnstatus, returnmessage = ctrlvalves.openvalve(klepsysteem,'zwembadon')
    if returnstatus:
        return(True,'Sproei zwembad ' + returnmessage)
    else:
        return(False,'Error in switching zwembad '+ returnmessage)

def startsproeier():
    returnstatus, returnmessage = ctrlvalves.openvalve(klepsysteem,'tuinon')
    if returnstatus:
        pumpon()
        return(True,'Sproei tuin ' + returnmessage )
    else:
        return(False,'Pomp niet aan error is kleppen ' + returnmessage)

def stopsproeier():
    pumpoff()
    returnstatus, returnmessage = ctrlvalves.openvalve(klepsysteem,'poweroff')

    if returnstatus:
        return(True,'Poweroff executed '+ returnmessage)
    else:
        #error in switching
        time.sleep(10)

        #try again 
        returnstatus, returnmessage = ctrlvalves.openvalve(klepsysteem,'poweroff')
        if returnstatus:
            return(True,'Poweroff completed '+ returnmessage) 
        else:
            return(False,'Error in poweroff kleppen '+ returnmessage)

def adhocsproei(sproeitijd):
    print('Init pump')
    portinit()
    pumpoff()

    print('Kleppencheck')
    #reset kleppen on storing te voorkomen
    ctrlvalves.fixsproeiklep()

    #wacht tot de kleppen klaar zijn 
    time.sleep(30)

    print('Start')

    returnstatus, returnmessage = startsproeier()
    if returnstatus:
        print('A: Start met de tuin '+ returnmessage)
    else:
        return(False, 'A: Foutje '+ returnmessage)

    time.sleep((sproeitijd*60)/2)

    print('Switch')

    returnstatus, returnmessage = sproeizwembad()
    if returnstatus:
        print('A: Over naar het zwembad '+ returnmessage)
    else:
        return(False, 'A: Foutje '+ returnmessage)

    time.sleep((sproeitijd*60)/2)

    returnstatus, returnmessage = stopsproeier()
    if returnstatus:
        print('A: Klaar met sproeien '+ returnmessage )
    else:
        return(False, 'A: Foutje '+ returnmessage )

    print('Klaar')
