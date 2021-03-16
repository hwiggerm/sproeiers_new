#!/usr/bin/env python

import glob
from pyowm.owm import OWM

def read_weather():
	owm = OWM('8db099bc017e2ccd16cbbbacf0390e9f')
	mgr = owm.weather_manager()
	observation = mgr.weather_at_place('Wageningen,NL')
	weather = observation.weather
	rain_dict = weather.rain
	temp_dict_celsius = weather.temperature('celsius')

	temp = str(temp_dict_celsius['temp'])
	rainh1 = str(rain_dict.get('1h'))
	rainh3 = str(rain_dict.get('3h'))
	weatherstatus = weather.status
	sunrise_iso = weather.sunrise_time(timeformat='iso')
	sunrset_iso = weather.sunset_time(timeformat='iso')

	weather = {
 		"outsidetemp": temp,
  		"rain1h": rainh1,
		"rain3h": rainh3,
  		"weather": weatherstatus,
		"sunset": sunrset_iso,
		"sunrise": sunrise_iso }

	return(weather)
