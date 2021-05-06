import mysql.connector 
import datetime 
import os

mysqlun = os.environ.get('MYSQLUN')
mysqlpw = os.environ.get('MYSQLPW')
mysqldb = os.environ.get('MYSQLDB')

def storedata(timestamp,tempin, oweer, tempsensor1):
    mydb = mysql.connector.connect(
    host="localhost",
    user=mysqlun,
    password=mysqlpw,
    database=mysqldb,
    )

    mycursor = mydb.cursor()

    query ="INSERT INTO logweather(logdate, tempin, tempout, weather, humidity, rain1h, rain3h, tsensor1) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
    values = (timestamp,str(tempin),oweer['outsidetemp'],oweer['weather'], oweer['humidity'], oweer['rain1h'], oweer['rain3h'], str(tempsensor1))

    mycursor.execute(query, values)
    mydb.commit()

def storeweather(weer):
    mydb = mysql.connector.connect(
    host="localhost",
    user=mysqlun,
    password=mysqlpw,
    database=mysqldb,
    )


    mycursor = mydb.cursor()

    query ="INSERT INTO weerinfo(timestamp, ytemp, yhum, yrain, ttemp, thum, train, sproeitijd, sunrise) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
    values = (weer['logdate'],weer['ytemp'],weer['yhum'],weer['yrain'],weer['ttemp'],weer['thum'],weer['train'],weer['sproeitijd'],weer['sunrise'])

    mycursor.execute(query, values)
    mydb.commit()

