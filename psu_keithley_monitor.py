#!/usr/bin/env python
import pyvisa
import time
import sys
from datetime import datetime
import re

curr_limit = 40 #mA

def getCurr(psu):
    value = psu.query(':MEAS1:CURR? 1,4')
    list = value.split(",")
    #print("output: " + list[0])
    s = list[0]
    s = s.rstrip(s[-1])
    f = float(s) * 1000 #convert to mA
    #print("float value: " + '{:.4}'.format(f))
    psu.write('*CLS')
    return f

def timenow():
    now = datetime.now()
    dt_string = now.strftime("%m/%d/%Y %H:%M:%S")
    return dt_string

# pyvisa.log_to_screen()
rm = pyvisa.ResourceManager('C:\\windows\\system32\\visa32.dll')
res = rm.list_resources('USB?*')
print(res)

# Find the serial number
str = str(res)
items = str.split('::')

psu = rm.open_resource('USB0::0x05E6::0x2280::' + items[3] +'::INSTR')
state = psu.query("OUTPUT:STATE?")
psu.write(":TRACe:FEED:CONTrol NEVer")
psu.write(":CONF1:CURR 1,4")

count = 0
measure_count = 0
#print(timenow() + "#: " + '{:}'.format(count) + " ")

while True:
    time.sleep(0.5)

    f = getCurr(psu)
    measure_count += 1
    #print(timenow() + ' {:5}'.format(measure_count) + " #: " + '{:}'.format(count) + " " + '{:0.2f}'.format(f))

    if(f > curr_limit):
        count+=1
        print(timenow() + ' {:5}'.format(measure_count) + " #: " + '{:}'.format(count) + " " + '{:0.2f}'.format(f))

        while f > curr_limit:
            time.sleep(0.5)
            f = getCurr(psu)

sys.exit(0)
