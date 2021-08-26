#!/usr/bin/env python
import os
import sys
import urllib.request

from urllib.request import urlopen

meterstatus = 'status'
polltemp = 'temp'

def gettemp(sensor):
    try:
        myURL = urlopen(sensor+polltemp)
        btemperature = myURL.read()
        temperature = btemperature.decode('UTF-8')
    except:
        temperature = 99

    return(temperature)
