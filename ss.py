from library.valves import ctrlvalves
from library.core import logger.py

import time

if ctrlvalves.openvalve('http://10.0.0.141/','tuinon'):
        logger.writeline('Valve Switched')
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








