#!/usr/bin/env python
import pyvisa as visa
import time
import sys
from datetime import datetime
import re

### DEBUG
#from visa import log_to_screen
#from pyvisa.ctwrapper.highlevel import NIVisaLibrary
#log_to_screen()
#NIVisaLibrary.get_library_paths()
#pyvisa.log_to_screen()

curr_limit = 40 #mA
sleep_time = 1

#curr = psu.query(':MEAS:CURR?')
#print(curr)

def getCurr(psu):
    value = psu.query(':MEAS:CURR?')
    
    list = value.split(",")
    #print("output: " + list[0])
    s = list[0]
    s = s.rstrip(s[-1])
    f = float(s) * 1000 #convert to mA
    #print("float value: " + '{:.4}'.format(f))
    #psu.write('*CLS')
    return f

def timenow():
    now = datetime.now()
    dt_string = now.strftime("%m/%d/%Y %H:%M:%S")
    return dt_string

# rm = visa.ResourceManager('@py')
rm = visa.ResourceManager('/cygdrive/c/Windows/System32/visa64.dll')
#print(rm)

psu = rm.open_resource("GPIB0::5::INSTR")
print(psu.query('*IDN?'))


count = 0
measure_count = 0
#print(timenow() + "#: " + '{:}'.format(count) + " ")

while True:
    time.sleep(sleep_time)

    f = getCurr(psu)
    measure_count += 1
    #print(timenow() + ' {:5}'.format(measure_count) + " #: " + '{:}'.format(count) + " " + '{:0.2f}'.format(f))

    if(f > curr_limit):
        count+=1
        print(timenow() + ' {:5}'.format(measure_count) + " #: " + '{:}'.format(count) + " " + '{:0.2f}'.format(f))

        while f > curr_limit:
            time.sleep(sleep_time)
            f = getCurr(psu)

sys.exit(0)