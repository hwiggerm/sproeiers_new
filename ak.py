#!/usr/bin/env python
import datetime
import time
from datetime import datetime as dt
from pyowm.owm import OWM

from library.timer import alarm
from library.valves import ctrlvalves
from library.valves import ctrlpump
from library.core import logger
from library.core import mysqldb
from library.sensors import getdht
from library.sensors import getowmweather
from library.sensors import get_tempsensor
from library.sensors import wfcst

import os

klepsysteem = os.environ.get('KLEPSYSTEEM')
owmkey =  os.environ.get('OWMAPI')

geolocation = os.environ.get('GEOLOC')
sproeiklep =  'http://192.168.1.141/'
zwembadsensor =  'http://192.168.1.142/'

ctrlpump.portinit()

#(re)set sproeiklep
print('Kleppen')
ctrlvalves.fixsproeiklep()
time.sleep(30)

sprinklersetup = False
sprinklerstart = False
sprinklerstop = False
sprinklermid = False
houraction = False

firstrun = True

sprinklersetuptime = dt.now()
sprinklerstarttime = dt.now()
sprinklermidtime = dt.now()
sprinklerstoptime = dt.now()

while True:

    if alarm.hoursign():
        if not houraction:
            print('hourcheck')
            now = datetime.datetime.now()
            nicetime = now.strftime("%Y-%m-%d %H:%M:%S")

            houraction = True

            tempin = 0
            tempsensor1 = 0

            logger.writeline('Get Weather at '+ nicetime)

            tempin = getdht.read_temp()
            # tempsensor1 = get_tempsensor.gettemp(zwembadsensor)

            oweer = getowmweather.read_weather()

            print(oweer)

            mysqldb.storedata(nicetime, tempin, oweer, tempsensor1)

            returnstatus, returnmessage = ctrlvalves.valvecheck(sproeiklep)
            logger.writeline('Valves status at '+ nicetime + ' ' + returnmessage)

    else:
        houraction = False



    #plan the sprinkler time
    if alarm.alarmclock(sprinklersetuptime):
        if not sprinklersetup:

            # what was the weather yesterday and is predicted for today

            weathersummary = wfcst.summarize()
            logger.writeline('Get weathersummary yesterday and forecast for '+str(weathersummary['logdate']))

            #timeshift for testing so that we 'see' the clicks in the morning.
            #will be 0 wne in production
            timedelta =  4   #in hours

            #delta between set time and start the sprinkler
            mindelta  =  0

            ysproeilist = mysqldb.getyesterdaysprinkler()
            ysproei = ysproeilist[0]

            logger.writeline('Sproeitijd Gisteren : ' + str(ysproei)  )

            waterunits = 0
            nieuwesproeitijd = 0

            #start met 60 minuten sproeitijd
            sproeitijd = 60

            logger.writeline('Verwachte temperatuur vandaag : '+ str(weathersummary['ttemp']) )

            #pas de sproeitijd aak op de temperatuur
            if weathersummary['ttemp'] < 20:
                sproeitijd = sproeitijd - 10

            if weathersummary['ttemp'] < 10:
                sproeitijd = sproeitijd - 50

            if weathersummary['ttemp'] > 20:
                sproeitijd  = sproeitijd + 10

            if weathersummary['ttemp'] > 25:
                sproeitijd  = sproeitijd + 30

            logger.writeline('Sproeitijd gebaseerd op de temperatuur : '+ str(sproeitijd))

            # neem de regen in de berekening#
            # 1mm regen = 20 min sproeien
            #

            logger.writeline('Yesterdays Rain : '+ str(weathersummary['yrain']))
            waterunits = weathersummary['yrain'] * 15


            logger.writeline('Waterunits : '+ str(waterunits))


            # we trekken nu de gevallen regen af van de geplande sproeitijd
            nieuwesproeitijd = sproeitijd - waterunits

            logger.writeline('Nieuwe sproeitijd : '+ str(nieuwesproeitijd))


            #als de sproitijd < 10 minuten is dan cancel
            if nieuwesproeitijd < 10:
                nieuwesproeitijd = 0

            logger.writeline('Nieuwe sproeitijd na 10min check : '+ str(nieuwesproeitijd))


            # we kennen de sproeitijd obv temperatuur en gevallen regen.
            # als er gisteren gesproeid is en het <25 graden is dan hoeft er vandaag niet gesproeid te worden

            if int(ysproei) != 0:
            #er is gisteren gesproeid dus vandaag hoeft niet tenzij de temp >25 graden is kies dan de berekende sproeitijd
                logger.writeline('looks like ysproei was <> 0')
                if weathersummary['ttemp'] >= 25:
                    sproeitijd = nieuwesproeitijd
                else:
                    sproeitijd = 0
            else:
                #ysproei was 0
                sproeitijd = nieuwesproeitijd

            logger.writeline('Finale sproeitijd : '+ str(sproeitijd))

            #debug only
            #sproeitijd = 30

            #get the sunrise
            sunrise_iso = getowmweather.getsunrise()

            #set next day setuptime
            sprinklersetuptime = sunrise_iso
            logger.writeline('Set sprinklersetup time to: ' + str(sprinklersetuptime) )

            #set sprinkeler start, swith and enddate
            logger.writeline('Set Sprinkler timing')
            sprinklerstarttime = ( sunrise_iso + datetime.timedelta(hours=timedelta, minutes=mindelta, seconds=0)).time()
            sprinklermidtime = (sunrise_iso + datetime.timedelta(hours=timedelta, minutes=mindelta + (sproeitijd/2), seconds=0)).time()
            sprinklerstoptime = (sunrise_iso + datetime.timedelta(hours=timedelta, minutes=mindelta + sproeitijd, seconds=0)).time()

            logger.writeline('Sprinkeler start time : ' + str(sprinklerstarttime) + ' - sproeitijd : ' + str(sproeitijd) )

            #update dict with new sproei/sunrise
            updweather = {
              "sproeitijd": sproeitijd,
              "sunrise": sunrise_iso  }
            weathersummary.update(updweather)

            #store the wether summary + forecast + spraytime
            logger.writeline('Store forecast for today : '+ weathersummary['logdate'])

            if not firstrun:
                mysqldb.storeweather(weathersummary)

            #pause for 60 seconds to avoid the forecast is triggered for a second time
            time.sleep(60)
            weathersummary.clear()

            #after the init set the flags the the following routines
            sprinklersetup = True
            sprinklerstart = False
            sprinklerstop = False
            sprinklermid = False
            firstrun = False
    else:
        sprinklersetup = False

    #start the sprinkler = start met de tuin
    if alarm.alarmclock(sprinklerstarttime) and sproeitijd>0:
        if not sprinklerstart:
            logger.writeline('Start Sprinkler')
            sprinklerstart = True
            returnstatus, returnmessage = ctrlpump.startsproeier()
            if returnstatus:
                logger.writeline('Started '+ returnmessage)
            else:
                logger.writeline('Error '+ returnmessage)
    else:
        prinklerstart = False

    #midtime the sprinkler = doe het zwembad
    if alarm.alarmclock(sprinklermidtime) and sproeitijd>0:
        if not sprinklermid:
            sprinklermid = True
            returnstatus, returnmessage = ctrlpump.sproeizwembad()
            if returnstatus:
                logger.writeline('Started '+ returnmessage)
            else:
                logger.writeline('Error '+ returnmessage)

    else:
        sprinklermid = False

    #we are ready
    if alarm.alarmclock(sprinklerstoptime):
        if not sprinklerstop:
            sprinklerstop = True
            returnstatus, returnmessage = ctrlpump.stopsproeier()
            if returnstatus:
                logger.writeline('Stopped '+ returnmessage)
            else:
                logger.writeline('Error '+ returnmessage)
    else:
        sprinklerstop = False

