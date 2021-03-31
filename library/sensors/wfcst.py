import mysql.connector
import datetime
from datetime import date
from datetime import timedelta
from pyowm.owm import OWM

#what is the weatherforecst

owmkey =  os.environ.get('OWMAPI')
geolocation = os.environ.get('GEOLOC')

owm = OWM(owmkey)
mgr = owm.weather_manager()
one_call = mgr.one_call(lat=51.970001, lon=5.66667, exclude='minutely', units='metric')

today = date.today()
yesterday = today + timedelta(days = -1)
print('today: '+ str(today))

def summarize:
  mysqlun = os.environ.get('MYSQLUN')
  mysqlpw = os.environ.get('MYSQLPW')
  mysqldb = os.environ.get('MYSQLDB')

  hourcount = 0

  tt = 0.0 
  ht = 0.0
  avgrain = 0
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
      rainvalue = rain

    tt = tt + int(temp['temp'])
    ht = ht + int(humid)
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
  
  #logdate, tempin, tempout, weather, humidity,

  v=0
  t=0
  h=0
  r=0
  
  for x in myresult:
    logdate = str(x[0])
    date_time_obj = datetime.datetime.strptime(logdate, '%Y-%m-%d %H:%M:%S')
    if date_time_obj.date() == yesterday:
        hourcount = hourcount + 1

        t = t + float(x[2])
        h = h + float(x[4])

        if x[5] != 'None':
          r = r + float(x[5])

  weather = {
    "logdate": str(today),
    "ytemp": t/v,
    "yhum": h/v,
    "yrain": r,
    "ttemp": tt/hourcount,
    "thum": ht/hourcount,
    "train": rt }

  return(weather)
