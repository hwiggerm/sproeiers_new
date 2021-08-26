#!/usr/bin/env python

import glob
import time
from pyowm.owm import OWM
import os

owmkey =  os.environ.get('OWMAPI')
geolocation = os.environ.get('GEOLOC')
geolat = os.environ.get('GEOLAT')
geolon = os.environ.get('GEOLON')
from datetime import datetime


def readowm():

    try:
        owm = OWM(owmkey)
        mgr = owm.weather_manager()
        observation = mgr.weather_at_place(geolocation)
        one_call = mgr.one_call(lat=float(geolat), lon=float(geolon))

        weather = observation.weather
        rain_dict = weather.rain
        temp_dict_celsius = weather.temperature('celsius')

        humidity = one_call.current.humidity
        weather = observation.weather
        rain_dict = weather.rain
        temp_dict_celsius = weather.temperature('celsius')

        temp = str(temp_dict_celsius['temp'])
        rainh1 = str(rain_dict.get('1h',0))
        rainh3 = str(rain_dict.get('3h',0))
        weatherstatus = weather.status
        sunrise_iso = weather.sunrise_time(timeformat='iso')
        sunrset_iso = weather.sunset_time(timeformat='iso')

        weatherreport = {
          "outsidetemp": temp,
          "rain1h": rainh1,
          "rain3h": rainh3,
          "weather": weatherstatus,
          "sunset": sunrset_iso,
          "sunrise": sunrise_iso,
          "humidity": humidity }

    except:
        weatherreport = {
          "outsidetemp": 0,
          "rain1h": 0,
          "rain3h": 0,
          "weather": 0,
          "sunset": 0,
          "sunrise": 0,
          "humidity": 0 }


    print('readowm')
    print(weatherreport)

    return(weatherreport)

def read_weather():

    oweer = readowm()
    print('1')
    print(oweer)

    if oweer['sunrise'] == 0:
        time.sleep(5)
        oweer = readowm()

        if oweer['sunrise'] == 0:
            time.sleep(5)
            oweer = readowm()

    return(oweer)



def getsunrise():
    try:
        owm = OWM(owmkey)
        mgr = owm.weather_manager()
        observation = mgr.weather_at_place(geolocation)

        weather = observation.weather
        sunrise = weather.sunrise_time(timeformat='date')
    except:
        date_time_str = '01/01/21 05:25:00'
        sunrise = datetime.strptime(date_time_str, '%d/%m/%y %H:%M:%S')

    return(sunrise)
