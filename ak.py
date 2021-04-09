from  library.timer import alarm
import datetime
import time
from datetime import datetime as dt
from pyowm.owm import OWM

from library.valves import ctrlvalves
from library.valves import ctrlpump
from library.core import logger
from library.core import mysqldb
from library.sensors import getdht
from library.sensors import getowmweather
from library.sensors import wfcst
import os

#

klepsysteem = os.environ.get('KLEPSYSTEEM')
owmkey =  os.environ.get('OWMAPI')
geolocation = os.environ.get('GEOLOC')
sproeiklep =  'http://10.0.0.141/'

ctrlpump.portinit()

sprinklersetup = False
sprinklerstart = False
sprinklerstop = False
sprinklermid = False
houraction = False

sprinklersetuptime = dt.now()
sprinklerstarttime = dt.now()
sprinklermidtime = dt.now()
sprinklerstoptime = dt.now()

while True:
    if alarm.hoursign():
        if not houraction:

            now = datetime.datetime.now()
            nicetime = now.strftime("%Y-%m-%d %H:%M:%S")
            time.sleep(1)

            houraction = True
            logger.writeline('Get Weather at '+ nicetime)
            tempin = getdht.read_temp()
            
            oweer = getowmweather.read_weather()

            if oweer['sunrise'] == 0:
                logger.writeline('ow not found ')
                time.sleep(5)

                oweer = getowmweather.read_weather()                 

                if oweer['sunrise'] == 0:
                    logger.writeline('ow not found ')
                    
                    time.sleep(5)
                    oweer = getowmweather.read_weather()
        
            mysqldb.storedata(nicetime, tempin, oweer)

            valvecheck = ctrlvalves.connect(sproeiklep)
            if valvecheck != '404':
                    logger.writeline('Valves alive at '+ nicetime)
            else:
                    logger.writeline('Unable to access Valves at '+ nicetime)

    else:
        houraction=False


    #plan the sprinkler time
    if alarm.alarmclock(sprinklersetuptime):
        if not sprinklersetup:
            
            weathersummary = wfcst.summarize()
            logger.writeline('Get weathersummary and forecast for '+str(weathersummary['logdate']))
        
            timedelta =  3   #in hours -=+
            mindelta  =  10

            # what was the weather yesterday
            # ytemp yhum yrain ttemp thum train sproeitijd
            sproeitijd = 60

            if weathersummary['ytemp'] < 20:
                sproeitijd = sproeitijd - 10
            if weathersummary['ytemp'] < 10:
                sproeitijd = sproeitijd - 50
            
            if weathersummary['ttemp'] > 20:
                sproeitijd  = sproeitijd + 10
            if weathersummary['ttemp'] > 25:
                sproeitijd  = sproeitijd + 30


            owm = OWM(owmkey)
            mgr = owm.weather_manager()
            observation = mgr.weather_at_place(geolocation)

            weather = observation.weather
            sunrise_iso = weather.sunrise_time(timeformat='date')
            sunset_iso = weather.sunset_time(timeformat='date')

            sprinklersetuptime = sunrise_iso
            
            if sproeitijd == 0:
                logger.writeline('Today its too cold to sprinkle')

            logger.writeline('Set sprinklersetup time to: ' + str(sprinklersetuptime) )
           
            logger.writeline('Set Sprinkler timing')
            sprinklerstarttime = ( sunrise_iso + datetime.timedelta(hours=timedelta, minutes=mindelta, seconds=0)).time()
            sprinklermidtime = (sunrise_iso + datetime.timedelta(hours=timedelta, minutes=mindelta + (sproeitijd/2), seconds=0)).time()
            sprinklerstoptime = (sunrise_iso + datetime.timedelta(hours=timedelta, minutes=mindelta + sproeitijd, seconds=0)).time()

            logger.writeline('Sprinkeler start time : ' + str(sprinklerstarttime) + ' - sproeitijd : ' + str(sproeitijd) )

            updweather = {
              "sproeitijd": sproeitijd,
              "sunrise": sunrise_iso  }
        
            weathersummary.update(updweather)

            logger.writeline('Store forecast for today : '+ weathersummary['logdate'])
            mysqldb.storeweather(weathersummary)

            sprinklersetup = True
            sprinklerstart = False
            sprinklerstop = False
            sprinklermid = False

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
            #pause

            sprinklerstop = True
            if ctrlvalves.openvalve(klepsysteem,'poweroff'):
                logger.writeline('poweroff')
            else:
                logger.writeline('Error in switching')
    else:
        sprinklerstop = False

