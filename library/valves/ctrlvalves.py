#!/usr/bin/env python
import os
import sys
import urllib.request
import time

def connect(host):
	try:
		reply = 0
		fb = urllib.request.urlopen(host)
		reply = fb.getcode()
		return(reply)
	except:
		return('404')

def openvalve(sproeiklep,klepstatus):

	# first check if the swithc can be reached
	alive = connect(sproeiklep+ 'status') 

	if alive == '404':
		#print('Connect Error')
		return(False)
	else:
		#print('Connected and feeling fine, status ' + str(alive))
		commando = sproeiklep + klepstatus
		valve = connect(commando)
		return(valve)


def fixsproeiklep():
        try:
                print('uit')
                fb = urllib.request.urlopen('http://192.168.1.85:85/klik.php?status=0')
                time.sleep(5)
                print('aan')
                fb = urllib.request.urlopen('http://192.168.1.85:85/klik.php?status=1')
                return('Done')
        except:
                return('.')


def valvecheck(sproeiklep):
        valvecheckcode = connect(sproeiklep)
        checkresult = ''

        if valvecheckcode != '404':
            checkresult = 'Valves alive'

        else:

            #wait 30 seconds and then retry
            time.sleep(30)
            valvecheckcode = connect(sproeiklep)

            if valvecheckcode == '404':
                #fix klep
                fixsproeiklep()

                #wait till its restarted
                time.sleep(30)

                #was it fixed?
                valvecheckcode = connect(sproeiklep)
                if valvecheckcode != '404':
                    checkresult = 'Valves recovered 1x and alive'

                else:
                    #not solved lets wait a minute and retry the fix
                    fixsproeiklep()
                    time.sleep(30)

                    #does it work?
                    valvecheckcode = connect(sproeiklep)
                    if valvecheckcode != '404':
                        checkresult = 'Valves recovered 2x and alive'
                    else:
                        checkresult = 'Valves in error even after fixing'
            else:
                checkresult = 'Valves alive'

        return(checkresult)
