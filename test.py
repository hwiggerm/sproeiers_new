#!/usr/bin/env python

#import os
#import glob

import time
import datetime
from library.sensors import getdht
from library.sensors import getowmweather


tempin = getdht.read_temp()
oweer = getowmweather.read_weather()

now = datetime.datetime.now()
nicetime = now.strftime("%Y-%m-%d %H:%M:%S")

textline = nicetime + ";" + str(tempin) + oweer['outsidetemp'] + ";" + oweer['weather'] + ";" + oweer['rain1h'] + ";" + oweer['rain3h'] + "\n"
f = open("templogger.txt", "a")
f.write(textline)
f.close()



