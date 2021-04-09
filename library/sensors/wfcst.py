import mysql.connector
import datetime
import os 

from datetime import date
from datetime import timedelta
from pyowm.owm import OWM

#what is the weatherforecst

owmkey =  os.environ.get('OWMAPI')
geolocation = os.environ.get('GEOLOC')
geolat = os.environ.get('GEOLAT')
geolon = os.environ.get('GEOLON')

owm = OWM(owmkey)
mgr = owm.weather_manager()
one_call = mgr.one_call(lat=float(geolat), lon=float(geolon), exclude='minutely', units='metric')

def summarize():
  mysqlun = os.environ.get('MYSQLUN')
  mysqlpw = os.environ.get('MYSQLPW')
  mysqldb = os.environ.get('MYSQLDB')

  today = date.today()
  yesterday = today + timedelta(days = -1)

  hourcount = 0
  tt = 0
  ht = 0
  rt = 0
  rainvalue = 0

  while hourcount < 24:
    hourcount += 1

    #get forecast data from pypwm
    temp = one_call.forecast_hourly[hourcount].temperature()
    humid = one_call.forecast_hourly[hourcount].humidity
    rain = one_call.forecast_hourly[hourcount].rain

    if not rain:
      rainvalue = 0
    else:
      rainvalue = float(rain['1h'])

    tt = tt + float(temp['temp'])
    ht = ht + float(humid)
    rt = rt + rainvalue

  #what was the recorded weather yesterday
  mydb = mysql.connector.connect(
    host="localhost",
    user=mysqlun,
    password=mysqlpw,
    database=mysqldb
    )

  mycursor = mydb.cursor()
  mycursor.execute("SELECT * FROM logweather")
  myresult = mycursor.fetchall()
  
  v=0
  t=0
  h=0
  r=0
  hourcountdb = 0

  for x in myresult:
    logdate = str(x[0])
    date_time_obj = datetime.datetime.strptime(logdate, '%Y-%m-%d %H:%M:%S')
    if date_time_obj.date() == yesterday:
        hourcountdb = hourcountdb + 1

        t = t + float(x[2])
        h = h + float(x[4])

        if x[5] != 'None':
          r = r + float(x[5])

  weather = {
    "logdate": str(today),
    "ytemp": t/hourcountdb,
    "yhum": h/hourcountdb,
    "yrain": r,
    "ttemp": tt/hourcount,
    "thum": ht/hourcount,
    "train": rt,
    "sproeitijd": 60,
    "sunrise": '' }
    
  return(weather)
