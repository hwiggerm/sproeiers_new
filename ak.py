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

firstrun = True

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
            
            # what was the weather yesterday and is predicted for today
            weathersummary.clear()
            weathersummary = wfcst.summarize()
            logger.writeline('Get weathersummary yesterday and forecast for '+str(weathersummary['logdate']))
        
            #timeshift for testing so that we 'see' the clicks in the morning.
            #will be 0 wne in production
            timedelta =  3   #in hours
            
            #delta between set time and start the sprinkler
            mindelta  =  10

            # available data
            # ytemp yhum yrain ttemp thum train sproeitijd            
            
            #start with 60 minutes
            sproeitijd = 60

            #adjust minutes based on weather
            if weathersummary['ytemp'] < 20:
                sproeitijd = sproeitijd - 10
            if weathersummary['ytemp'] < 10:
                sproeitijd = sproeitijd - 50
            
            if weathersummary['ttemp'] > 20:
                sproeitijd  = sproeitijd + 10
            if weathersummary['ttemp'] > 25:
                sproeitijd  = sproeitijd + 30


            if sproeitijd == 0:
                logger.writeline('Today its too cold to sprinkle')


            #get the sunrise 
            owm = OWM(owmkey)
            mgr = owm.weather_manager()
            observation = mgr.weather_at_place(geolocation)

            weather = observation.weather
            sunrise_iso = weather.sunrise_time(timeformat='date')
            sunset_iso = weather.sunset_time(timeformat='date')

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

