from library.valves import ctrlpump
from library.valves import ctrlvalves


import time
import sys

print('Init pump')
ctrlpump.portinit()
ctrlpump.pumpoff()

#reset kleppen on storing te voorkomen
ctrlvalves.fixsproeiklep()

#wacht tot de kleppen klaar zijn 
time.sleep(30)

print('Start')
sproeitijd = int(sys.argv[1])
print(sproeitijd)


returnstatus, returnmessage = ctrlpump.startsproeier()
if returnstatus:
    print('Gestart '+ returnmessage)
else:
    print('Foutje '+ returnmessage)
    exit()

print('Tuin aan het sproeien ...')
time.sleep((sproeitijd*60)/2)

print('Switch')

returnstatus, returnmessage = ctrlpump.sproeizwembad()
if returnstatus:
    print('Gestart '+ returnmessage)
else:
    print('Foutje '+ returnmessage)
    exit()

print('Zwembad aan het sproeien ...')
time.sleep((sproeitijd*60)/2)

returnstatus, returnmessage = ctrlpump.stopsproeier()
if returnstatus:
    print('Klaar '+ returnmessage)
else:
    print('Foutje '+ returnmessage)
    exit()

print('Done')

