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
export GEOLON='5.690168016538389'
export GEOLAT='51.97338909741969'

nohup python ak.py &
