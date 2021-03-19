from library.valves import ctrlvalves
from library.core import logger

import time

if ctrlvalves.openvalve('http://10.0.0.141/','tuinon'):
        logger.writeline('Valve Switched tuin')
else:
	logger.writeline('Error in switching')

if ctrlvalves.openvalve('http://10.0.0.141/','zwembadon'):
	logger.writeline('Valve Switched zwembad')
else:
        logger.writeline('Error in switching')

time.sleep(5)

if ctrlvalves.openvalve('http://10.0.0.141/','poweroff'):
        logger.writeline('poweroff')
else:
        logger.writeline('Error in switching')

