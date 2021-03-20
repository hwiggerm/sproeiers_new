from  library.timer import alarm
import datetime
import time
from datetime import datetime as dt
from pyowm.owm import OWM

from library.valves import ctrlvalves
from library.valves import ctrlpump
from library.core import logger

klepsysteem = 'http://10.0.0.141/'


owm = OWM('8db099bc017e2ccd16cbbbacf0390e9f')
mgr = owm.weather_manager()
observation = mgr.weather_at_place('Wageningen,NL')

weather = observation.weather
sunrise_iso = weather.sunrise_time(timeformat='date') 
sunset_iso = weather.sunset_time(timeformat='date')

timedelta = -4    #in hours -=+

print('sunrise         :',sunrise_iso.time())

sprinklersetuptime = (sunrise_iso - datetime.timedelta(hours=timedelta, minutes=-20, seconds=0)).time()
print('plan sprinklers. :',sprinklersetuptime)

sprinklersetup = False
sprinklerstart = False
sprinklerstop = False
sprinklermid = False

sprinklerstarttime = dt.now()
sprinklermidtime = dt.now()
sprinklerstoptime =dt.now()

while True:
    #plan the sprinkler time
    if alarm.alarmclock(sprinklersetuptime):
        if not sprinklersetup:
            print('Setup Sprinkler timing')
            sprinklerstarttime = (sunrise_iso - datetime.timedelta(hours=timedelta, minutes=-45, seconds=0)).time()
            sprinklermidtime = (sunrise_iso - datetime.timedelta(hours=timedelta, minutes=-47, seconds=0)).time()
            sprinklerstoptime = (sunrise_iso - datetime.timedelta(hours=timedelta, minutes=-49, seconds=0)).time()

            print('sprinkeler start time :',sprinklerstarttime)
            print('sprinkeler mid time :',sprinklermidtime)
            print('sprinkeler stop time :',sprinklerstoptime)
            sprinklersetup = True
    else:
        sprinklersetup = False

    #start the sprinkler
    if alarm.alarmclock(sprinklerstarttime):
        if not sprinklerstart:
            print('Start Sprinkler')
            sprinklerstart = True

            if ctrlvalves.openvalve(klepsysteem,'tuinon'):
                logger.writeline('Valve Switched tuin')
                ctrlpump.pumpon()
            else:
                logger.writeline('Error in switching tuin')

    else:
        prinklerstart = False

    #midtime the sprinkler
    if alarm.alarmclock(sprinklermidtime):
        if not sprinklermid:
            print('Switch Sprinkler')
            sprinklermid = True

            if ctrlvalves.openvalve(klepsysteem,'zwembadon'):
                logger.writeline('Valve Switched zwembad')
            else:
                logger.writeline('Error in switching zwembad')

    else:
        sprinklermid = False

    #we are ready
    if alarm.alarmclock(sprinklerstoptime):
        if not sprinklerstop:
            print('Stop Sprinkler')
            ctrlpump.pumpoff()
            #stop pump
            #delay
            sprinklerstop = True

            if ctrlvalves.openvalve(klepsysteem,'poweroff'):
                logger.writeline('poweroff')
            else:
                logger.writeline('Error in switching')
    else:
        sprinklerstop = False

