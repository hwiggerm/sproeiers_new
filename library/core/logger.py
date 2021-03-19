
#Write to  text to logfle ~/sprinkler.log

def writeline(dtext):
    logfile = open("~/sprinkler.log","a")
    logfile.write(dtext)
    logfile.close()
