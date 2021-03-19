#!/usr/bin/env python
import os
import sys
import urllib.request

def connect(host):
	try:
		reply = 0
		fb = urllib.request.urlopen(host)
		reply = fb.getcode()
		return reply
	except:
        return 404

def openvalve(sproeiklep,klepstatus):
	
	# first check if the swithc can be reached
	alive = connect(sproeiklep + '/status') 
	if alive == 404:
		print('Connect Error')
		return(false)
	else:
		print('Connected and feeling fine, status ' + str(alive))
		time.sleep(5)

	print('set ' + sproeiklep )
	valve = connect(sproeiklep + klepstatus)
	print ("valve status :", str(valve))
	time.sleep(5)
	return(valve)