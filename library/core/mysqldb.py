import mysql.connector 
import datetime 
import os

mysqlun = os.environ.get('MYSQLUN')
mysqlpw = os.environ.get('MYSQLPW')
mysqldb = os.environ.get('MYSQLDB')

def storedata(timestamp,tempin, oweer):
    mydb = mysql.connector.connect(
    host="localhost",
    user=mysqlun,
    password=mysqlpw,
    database=mysqldb,
    )


    mycursor = mydb.cursor()

    query ="INSERT INTO logweather(logdate, tempin, tempout, weather, humidity, rain1h, rain3h) VALUES (%s, %s, %s, %s, %s, %s, %s)"
    values = (timestamp,str(tempin),oweer['outsidetemp'],oweer['weather'], oweer['humidity'], oweer['rain1h'], oweer['rain3h'])

    mycursor.execute(query, values)
    mydb.commit()


