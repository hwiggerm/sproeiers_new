from pyowm.owm import OWM

owm = OWM('8db099bc017e2ccd16cbbbacf0390e9f')
mgr = owm.weather_manager()

observation = mgr.weather_at_place('Wageningen,NL')  # the observation object is a box containing a weather object
weather = observation.weather

print('Weer')
print('status',weather.status)
print('details',weather.detailed_status)
print()

print('temperatuur')
temp_dict_celsius = weather.temperature('celsius') 
print('temperatuur overzicht',temp_dict_celsius)
print('buiten temperatuur', temp_dict_celsius['temp'])
print()

print('rain')
rain_dict = mgr.weather_at_place('Wageningen,NL').weather.rain
print('Rain next hour:',rain_dict.get('1h'))
print('Rain next 3 hours:',rain_dict.get('3h'))

