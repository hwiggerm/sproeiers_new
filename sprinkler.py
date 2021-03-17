#!/usr/bin/env python
import os
import sys
import urllib.request
import time


from library.sensors import getdht
from library.sensors import getowmweather

sproeiklep =  'http://10.0.0.141/'
klepstatus = 'status'
tuinklep = 'zwembadon'
zwembklep = 'tuinon'

#
# check of er een verbinding is anders stoppen 
#

def connect(host):
	try:
		reply = 0
		fb = urllib.request.urlopen(host)
		reply = fb.getcode()
		return reply
	except:
        	return 404


alive = connect(sproeiklep+klepstatus) 
if alive == 404:
	print('Connect Error')
else:
	print('Connected and feeling fine, status ' + str(alive))
time.sleep(5)


print('set tuinklep = 201')
tk = connect(sproeiklep+tuinklep)
print ("klepcode :", str(tk))
time.sleep(5)

print('set zwembadklep = 202')
tk = connect(sproeiklep+zwembklep)
print ("klepcode :", str(tk))
time.sleep(5)


print('------')

tempin = getdht.read_temp()
o = getowmweather.read_weather()

print(tempin)
print('---')
print(o['weather'])

