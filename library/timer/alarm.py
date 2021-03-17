import datetime
from datetime import datetime as dt

def alarmclock(alarmtime):
	alarm = False
	shour = alarmtime.strftime("%I")
	smin = alarmtime.strftime("%M")

	ctime = dt.now()
	chour = ctime.strftime("%I")
	cmin = ctime.strftime("%M")

	if shour == chour:
		if smin == cmin:
			alarm = True
		else:
			alarm = False
	return(alarm)
