from datetime import datetime


#Write to  text to logfle ~/sprinkler.log
def writeline(dtext):
	now = datetime.now()
	logfile = open("/home/pi/sprinkler.log","a")
	logfile.write(now.strftime("%d/%m/%Y %H:%M:%S")+' '+dtext+'\n')
	logfile.close()
