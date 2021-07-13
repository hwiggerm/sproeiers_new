import time
import os
import datetime
import telepot
from telepot.loop import MessageLoop

from library.sensors import get_tempsensor
from library.sensors import getdht
from library.core import mysqldb
from library.valves import ctrlpump


zwembadsensor = os.environ.get('ZWEMBADSYSTEEM')
botid = os.environ.get('TELEGRAMKEY')

def readtemperatuur():
    tempin = getdht.read_temp()
    tempsensor1 = get_tempsensor.gettemp(zwembadsensor)

    tempreading = {
        "binnen": tempin,
        "zwembad": tempsensor1
        }

    return(tempreading)

def handle(msg):
    chat_id = msg['chat']['id']
    command = msg['text']

    print('Got command: %s' % command)

    if command == '/time':
        bot.sendMessage(chat_id, str(datetime.datetime.now()))
    elif command == '/temp':
        temperatuurlijst = readtemperatuur()
        bot.sendMessage(chat_id, 'In Garage : ' + str(temperatuurlijst['binnen']) + '\n' +  'Bij Zwembad : ' + str(temperatuurlijst['zwembad']))
    elif command == '/fcst':
        weersummary = mysqldb.getyesterdaysforecast()
        bot.sendMessage(chat_id, 'Timestamp : ' + str(weersummary[0]) + '\n' +  'Ytemp: ' + str(weersummary[1]) + '\n' +  'Yhum : ' + str(weersummary[2]) + '\n' +  'yrain : ' + str(weersummary[3]) + '\n' + 'Sproeitijd : ' + str(weersummary[7]) )
    elif command == '/weer':
        weersummary = mysqldb.getlastweather()
        bot.sendMessage(chat_id, 'Timestamp : ' + str(weersummary[0]) + '\n' +  'Temp Schuur: ' + str(weersummary[1]) + '\n' +  'Temp buiten : ' + str(weersummary[2]) + '\n' +  'Het weer : ' + str(weersummary[3])  + '\n' + 'Vocht : ' + str(weersummary[4])  + '\n' + 'Regen komend uur : ' + str(weersummary[5])+ '\n' + 'Temp tuin : ' + str(weersummary[7]) )
    elif command == '/sproei':
        returnstatus, returnmessage = ctrlpump.adhocsproei(5)
        bot.sendMessage(chat_id, 'Sproeien!! ' + returnmessage )

bot = telepot.Bot(botid)

MessageLoop(bot, handle).run_as_thread()
print('I am listening ...')

while 1:
    time.sleep(10)
