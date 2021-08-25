##
## This file is part of the libsigrokdecode project.
##
## Copyright (C) 2018 Steve R <steversig@virginmedia.com>
##
## This program is free software; you can redistribute it and/or modify
## it under the terms of the GNU General Public License as published by
## the Free Software Foundation; either version 2 of the License, or
## (at your option) any later version.
##
## This program is distributed in the hope that it will be useful,
## but WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
## GNU General Public License for more details.
##
## You should have received a copy of the GNU General Public License
## along with this program; if not, see <http://www.gnu.org/licenses/>.
##
# Ref 1 http://www.osengr.org/WxShield/Downloads/Weather-Sensor-RF-Protocols.pdf
# Ref 2 https://github.com/robwlakes/Weather-Station-OS-Sensors/blob/master/DebugVersion_16_NextStep/DebugVersion_16_NextStep.ino
# Ref 3 https://loune.net/2018/01/decoding-the-oregon-scientific-temperature-sensor/
# Ref 4 RFLink development tree/Source Code. Plugin-48 Oregon V1/2/3 https://drive.google.com/open?id=0BwEYW5Q6bg_ZTDhKQXphN0ZxdEU 

# Ref 6 https://gist.github.com/RouquinBlanc/5cb6ff88cd02e68d48ea BTHR918N_ArduinoSender.ino


oregon_data = [
#   ['trace','explanation','version'], 
# version is one of 
#       v1, v2.1 or v3 (Hex nibbles in received from wire order)
#       Orv2.1 (v2.1 via Oregon.h library on an Arduino, pairs of nibbles are reversed, Sync pattern is in there)
#       OSV2 (v2 via orscV2.h library on an Arduino) 
#
# Oregon v1
# from ref 1 Version 1.0 Message Format - p23
#['8487101C','rolling code of “8” and the sensor is set to channel 2, reading 17.8 oC. checksum 0xC1.','v1'],
# from ref 1 Version 1.0 Message Format - p24
#['88190AAB','rolling code of “8”, is set to channel 3, reads -9.1 oC and has a low battery. checksum of 0xBA.','v1'],

# Oregon v2.1/3
# from ref 1 Examples - p29
#['1D20485C480882894','THGR122NX is set to channel 3 (1 << (3-1)) and has a rolling ID code of 0x85. The first flag nibble (0xC) contains the battery low flag bit (0x4). The temperature is -8.4 oC since nibbles 11..8 are “8084”. The first “8” indicates a negative temperature and the next three (“084”) represent the decimal value 8.4. Humidity is 28% and the checksum byte is 0x53 and is valid.','v2.1'],
#['1D2016B1091073A73','THGR122NX is set to channel 1 (1 << (1-1)) and has a rolling ID code of 0x6B, and the battery low bit is not set in the flag nibble (0x1). Temperature and humidity are 19.0 oC and 37%. Checksum is 0x41 and is valid.','v2.1'],

# from ref 2
#['291405093393331100802','PCR800 Rain Gauge Sample Data','v3'],
#['198408E000C70040034','WGR800 Av Speed 0.4m/s Gusts 0.7m/s  Direction: N ','v3'],
#['F8241CB894200488555','THGN800 Temperature and Humidity Sensor Temperature 24.9 degC Humidity 40 % rel','v3'],

# from ref 3
#['ACD39A718030C4670000','RTHR328N temp = +30.8 Checksum OK 4C','v2.1'],

# my sensors
#['1A2D02BBC64202507400','Virtual THGR228N Temperature and Humidity Sensor RollingCode BB temp +24.6 degC Hum 52%','v2.1'],
#['FA281496801190044459','','v3'],
#['1A89040180C03640043C','','v3'],
#['1984   F F   F  F    ','','v3'],

# from ref 4
#['EA4C20725C21D083','THN132N','OSV2'],
#['EA4C20809822D013','THN132N','OSV2'],
#['AACC13783419008250AD','RTGR328N Id:78 ,Channel:0 ,temp:19.30 ,hum:20 ,bat:10','OSV2'], # ???
#['1A2D40C4512170463EE6','[THGR228N,...] Id:C4 ,Channel:3 ,temp:21.50 ,hum:67 ,bat:90','OSV2'],
#['FA2814A93022304443BE','THGR810','OSV3'],
#['5A6D007A102330838631','BTHR918','OSV2'],
#['2A1D0065502735102063',' RGR126, RGR682, RGR918, RGR928, PCR122','OSV3'], # ???
#['2A19048E399393250010','PCR800','v3'],
#['3A0D006F400800000031','WGR918','v3'],

# from ref 5
#['1A2D10EC322750064425','THGN132N rcode EC. temp of +27.3°C, and humidity 65%','v2.1'],

# from ref 6
#['EA4C20CB2011B003','virtual THN132N EA4C20CB2011B003, Received sensorID is ec40 NOT EA4C ch: 2 temp: 11.20 batt: 90 Checksum is 0x0A too big','Orv2.1'],
['1A2D20CB201120053400','virtual THGR228N 1A2D20CB2011200534, Received sensorID is 1d20 NOT 1A2D ch: 2 temp: 11.20 hum: 52 batt: 90 Checksum is 0x0A too big','Orv2.1'],
#['5A6D20CB201120059DC05E','virtual BTHR918N 5A6D20CB201120059DC05E, Received sensorID is 5d60 NOT 5A6D ch: 2 temp: 11.20 hum: 52 pressure: 1013 batt: 90 Checksum is 0x0A too big','Orv2.1'],
]
