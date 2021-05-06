#!/usr/bin/env python
import os
import sys
import urllib.request

from urllib.request import urlopen

meterstatus = 'status'
polltemp = 'temp'

def connect(host):
     try:
         reply = 0
         fb = urllib.request.urlopen(host)
         reply = fb.getcode()
         return reply

     except:
         return 404

def gettemp(sensor):
    alive = connect(sensor+meterstatus)
    if alive == 404:
        print('Connect Error')
        return(False)

    else:
        #print('Connected and feeling fine, status ' + str(alive))
        myURL = urlopen(sensor+polltemp)
        btemperature = myURL.read()
        temperature = btemperature.decode('UTF-8')
        #print ("Temperature :" + str(temperature))
        return(temperature)