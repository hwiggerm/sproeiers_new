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

    print(oweer)
    print(tempin)
    print(tempsensor1)


    query ="INSERT INTO logweather(logdate, tempin, tempout, weather, humidity, rain1h, rain3h, tsensor1) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
    values = (timestamp,float(tempin),float(oweer['outsidetemp']),oweer['weather'], float(oweer['humidity']), float(oweer['rain1h']), float(oweer['rain3h']), float(tempsensor1))

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


def getyesterdaysprinkler():
    mydb = mysql.connector.connect(
    host="localhost",
    user=mysqlun,
    password=mysqlpw,
    database=mysqldb,
    )

    mycursor = mydb.cursor()

    query = 'select convert(sproeitijd,UNSIGNED INTEGER)  as sproeitijd from weerinfo order by timestamp desc LIMIT 1'

    mycursor.execute(query)
    return(mycursor.fetchone() )

def getyesterdaysforecast():
    mydb = mysql.connector.connect(
    host="localhost",
    user=mysqlun,
    password=mysqlpw,
    database=mysqldb,
    )

    mycursor = mydb.cursor()
    query = "select * from weerinfo order by timestamp desc LIMIT 1"

    mycursor.execute(query)
    return(mycursor.fetchone() )


def getlastweather():
    mydb = mysql.connector.connect(
    host="localhost",
    user=mysqlun,
    password=mysqlpw,
    database=mysqldb,
    )

    mycursor = mydb.cursor()
    query = "select * from logweather order by logdate desc LIMIT 1"

    mycursor.execute(query)
    return(mycursor.fetchone() )
