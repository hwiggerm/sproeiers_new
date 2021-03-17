#!/usr/bin/env python
# from g import mymodule

from library.sensors import getdht
from library.sensors import getowmweather
#
#	mymodule.greeting("Hans")
#
#	a = mymodule.person1["age"]
#	print(a)
#
#
#	b = mymodule.dicttest("1993")
#	print(b)
#	print(b['brand'])
#

tempin = getdht.read_temp()
o = getowmweather.read_weather()

print(tempin)
print('---')
print(o)
print(o['weather'])






