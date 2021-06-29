#!/usr/bin/python
# -*- coding: utf-8 -*-
#  /home/pi/wiringPi/examples/lights
# 
# date 13-11-25
# version 1.0 hwi
#
#
import kaku_timer
import sys

if len(sys.argv) > 3:
	print ('Please use one DevId as argument, followed by a 1 or 0 to set the status')
	exit()


k=sys.argv[1]

#if k >= 99:
#	print 'sleep'
#else:
kaku_timer.switch_kaku( sys.argv[1], sys.argv[2],'B' )
