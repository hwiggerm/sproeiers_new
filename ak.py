from  library.timer import alarm
import datetime
from datetime import datetime as dt
from pyowm.owm import OWM

owm = OWM('8db099bc017e2ccd16cbbbacf0390e9f')
mgr = owm.weather_manager()
observation = mgr.weather_at_place('Wageningen,NL')

weather = observation.weather
sunrise_iso = weather.sunrise_time(timeformat='date') 
sunset_iso = weather.sunset_time(timeformat='date')

timedelta = -2  #in hours -=+

print('sunrise         :',sunrise_iso.time())

sprinklersetuptime = (sunrise_iso - datetime.timedelta(hours=timedelta, minutes=1, seconds=0)).time()
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
			sprinklerstarttime = (sunrise_iso - datetime.timedelta(hours=timedelta, minutes=0, seconds=0)).time()
			sprinklermidtime = (sunrise_iso - datetime.timedelta(hours=timedelta, minutes=-10, seconds=0)).time()
			sprinklerstoptime = (sunrise_iso - datetime.timedelta(hours=timedelta, minutes=-15, seconds=0)).time()

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
	else:
		prinklerstart = False

	#midtime the sprinkler
	if alarm.alarmclock(sprinklermidtime):
		if not sprinklermid:
			print('Switch Sprinkler')
			sprinklermid = True
	else:
		sprinklermid = False

	#we are ready
	if alarm.alarmclock(sprinklerstoptime):
		if not sprinklerstop:
			print('Stop Sprinkler')
			sprinklerstop = True
	else:
		sprinklerstop = False

