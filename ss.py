import  valves
import time

if valves.openvalve('http://10.0.0.141/','tuinon'):
	print('Valve Switched')
else:
	print('Error in switching')


time.sleep(5)

if valves.openvalve('http://10.0.0.141/','zwembadon'):
        print('Valve Switched')
else:
        print('Error in switching')





