from library.valves import ctrlvalves

import time

if ctrlvalves.openvalve('http://10.0.0.141/','tuinon'):
	print('Valve Switched')
else:
	print('Error in switching')
if ctrlvalves.openvalve('http://10.0.0.141/','zwembadon'):
        print('Valve Switched')
else:
        print('Error in switching')

time.sleep(5)

if ctrlvalves.openvalve('http://10.0.0.141/','poweroff'):
        print('poweroff')
else:
        print('Error in switching')








