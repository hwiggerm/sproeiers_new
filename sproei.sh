cd weatherenv
source bin/activate

export NETWORK='Dorskamp'
export NETWORKKEY='46498342'
export KLEPSYSTEEM='http://10.0.0.141/'
export OWMAPI='8db099bc017e2ccd16cbbbacf0390e9f'
export GEOLOC='Wageningen, NL'
export MYSQLUN='meteo'
export MYSQLPW='regendruppel'
export MYSQLDB='weather'


nohup python ak.py &
