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

import telepot
from telepot.loop import MessageLoop

klepsysteem = os.environ.get('KLEPSYSTEEM')
owmkey =  os.environ.get('OWMAPI')
telegramkey = os.environ.get('TELEGRAMKEY')

geolocation = os.environ.get('GEOLOC')
sproeiklep =  'http://192.168.1.141/'
zwembadsensor =  'http://192.168.1.142/'

ctrlpump.portinit()

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

#(re)set sproeiklep
print('Kleppen')
ctrlvalves.fixsproeiklep()

def handle(msg):
    chat_id = msg['chat']['id']
    command = msg['text']

    if command == '/time':
        bot.sendMessage(chat_id, str(datetime.datetime.now()))
    elif command == '/temp':
        bot.sendMessage(chat_id, str(tempin))

bot = telepot.Bot(telegramkey)
MessageLoop(bot, handle).run_as_thread()
logger.writeline('I Am listening...')


while True:

    if alarm.hoursign():
        if not houraction:

            now = datetime.datetime.now()
            nicetime = now.strftime("%Y-%m-%d %H:%M:%S")
            time.sleep(1)

            houraction = True

            logger.writeline('Get Weather at '+ nicetime)
            tempin = getdht.read_temp()
            tempsensor1 = get_tempsensor.gettemp(zwembadsensor)

            oweer = getowmweather.read_weather()

            if oweer['sunrise'] == 0:
                logger.writeline('ow not found #1 ')
                time.sleep(5)

                oweer = getowmweather.read_weather()

                if oweer['sunrise'] == 0:
                    logger.writeline('ow not found #2')

                    time.sleep(5)
                    oweer = getowmweather.read_weather()

            mysqldb.storedata(nicetime, tempin, oweer, tempsensor1)

            valvecheckcode = ctrlvalves.valvecheck(sproeiklep)
            logger.writeline('Valves status at '+ nicetime + ' ' + valvecheckcode)

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
            timedelta =  3   #in hours

            #delta between set time and start the sprinkler
            mindelta  =  10

            ysproei = mysqldb.getyesterdaysprinkler()

            waterunits = 0
            nieuwesproeitijd = 0

            #start met 60 minuten sproeitijd
            sproeitijd = 60

            #pas de sproeitijd aak op de temperatuur
            if weathersummary['ttemp'] < 20:
                sproeitijd = sproeitijd - 10

            if weathersummary['ttemp'] < 10:
                sproeitijd = sproeitijd - 50

            if weathersummary['ttemp'] > 20:
                sproeitijd  = sproeitijd + 10

            if weathersummary['ttemp'] > 25:
                sproeitijd  = sproeitijd + 30

            # neem de regen in de berekening#
            # 1mm regen = 20 min sproeien
            #
            waterunits = weathersummary['yrain'] * 15

            # we trekken nu de gevallen regen af van de geplande sproeitijd
            nieuwesproeitijd = sproeitijd - waterunits

            #als de sproitijd < 10 minuten is dan cancel
            if nieuwesproeitijd < 10:
                nieuwesproeitijd = 0;

            # we kennen de sproeitijd obv temperatuur en gevallen regen.
            # als er gisteren gesproeid is en het <25 graden is dan hoeft er vandaag niet gesproeid te worden

            if ysproei != 0:
            #er is gisteren gesproeid dus vandaag hoeft niet tenzij de temp >25 graden is kies dan de berekende sproeitijd
                if weathersummary['ttemp'] >= 25:
                    sproeitijd = nieuwesproeitijd
                else:
                    sproeitijd = 0
            else:
                sproeitijd = nieuwesproeitijd

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

    #start the sprinkler
    if alarm.alarmclock(sprinklerstarttime) and sproeitijd>0:
        if not sprinklerstart:
            logger.writeline('Start Sprinkler')
            sprinklerstart = True

            if ctrlvalves.openvalve(klepsysteem,'tuinon'):
                logger.writeline('Valve Switched tuin')
                ctrlpump.pumpon()
                logger.writeline('Pump On')
            else:
                logger.writeline('Error in switching tuin')

    else:
        prinklerstart = False

    #midtime the sprinkler
    if alarm.alarmclock(sprinklermidtime) and sproeitijd>0:
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
            logger.writeline('Pump Off')
            ctrlpump.pumpoff()

            sprinklerstop = True
            if ctrlvalves.openvalve(klepsysteem,'poweroff'):
                logger.writeline('poweroff')
            else:
                logger.writeline('Error in switching')
    else:
        sprinklerstop = False
