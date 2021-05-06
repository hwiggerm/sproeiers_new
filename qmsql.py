import mysql.connector
import datetime
from datetime import date
from datetime import timedelta

mydb = mysql.connector.connect(
  host="localhost",
  user="meteo",
  password="regendruppel",
  database="weather"
)

mycursor = mydb.cursor()

mycursor.execute("SELECT * FROM logweather")
myresult = mycursor.fetchall()

today = date.today()
yesterday = today + timedelta(days = -1)
print('today: '+ str(today))
print('yesterday: ' + str(yesterday))


v=0
t=0
tout=0
h=0
r=0


for x in myresult:
    logdate = str(x[0])
    date_time_obj = datetime.datetime.strptime(logdate, '%Y-%m-%d %H:%M:%S')
    if date_time_obj.date() == yesterday:
        v = v + 1

        t = t + float(x[1])
        h = h + float(x[4])
        tout = tout + float(x[2])

        if x[5] != 'None':
            r = r + float(x[5])


print('Number of measurements :' + str(v) )
print('Average Tempin:' + str(t/v))
print('Average Tempout:' + str(tout/v))
print('Average Humidity :' + str(h/v))
print('Rain :' + str(r) )

