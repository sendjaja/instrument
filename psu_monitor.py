#!/usr/bin/env python
import pyvisa as visa
import time
import sys
import signal
from datetime import datetime

# Run python -O <this file>
# to set __debug__ to False

### DEBUG
# from visa import log_to_screen
# from pyvisa.ctwrapper.highlevel import NIVisaLibrary
#log_to_screen()
#NIVisaLibrary.get_library_paths()
#pyvisa.log_to_screen()

# DEFAULT setting for this file
# Default current before device monitored is considered ON
curr_limit = 80 #mA

# Delay between each current measurement
delay_time = 1

# Counter for how many measurements
measure_count = 0

# Counter for how many times it powers up
count = 0

def timenow():
    now = datetime.now()
    dt_string = now.strftime("%m/%d/%Y %H:%M:%S")
    return dt_string

def signal_handler(sig, frame):
    if bool(__debug__) :
        print("Ctrl+C is pressed, turning off PSU")
        # psu.write(":OUTP OFF")
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

def openVisaResourceManager():
    # visa.log_to_screen()
    # DO NOT WORK - rm = visa.ResourceManager('@py')
    # DO NOT WORK - rm = visa.ResourceManager("/cygdrive/c/Program\ Files/IVI\ Foundation/VISA/Win64/Lib_x64/msc/visa64.lib")
    # DO NOT WORK - rm = visa.ResourceManager('C:\\Program Files\\IVI Foundation\\VISA\\Win64\\Lib_x64\\msc\\visa64.lib')
    # DO NOT WORK - rm = visa.ResourceManager('C:\\windows\\system32\\visa64.dll')
    rm = visa.ResourceManager('C:\\windows\\system32\\nivisa64.dll') # Testing nivisa instead of built-in windows visa64.dll
    # NEXT TO TRY - rm = visa.ResourceManager('C:\\windows\\system32\\visa32.dll')

    res = rm.list_resources()
    if bool(__debug__):    
        print(rm)
        print("Found following resources: ")
        print(res)

    return rm

def open_psu():
    rm = openVisaResourceManager()

    #print("Opening " + res[-1])
    # SERIAL
    #psu = rm.open_resource("ASRL/dev/ttyS1::INSTR")
    #psu.baud_rate = 9600
    #psu.data_bits = 8
    #psu.write_termination="\n"
    #psu.read_termination="\n"
    ## psu.send_end=1
    #psu.timeout = 2500 # timeout 2.5s
    
    # USB
    # This might change, especially the "4441344"
    #psu = rm.open_resource('USB0::0x05E6::0x2280::4441344::INSTR')

    # GPIB
    psu = rm.open_resource("GPIB0::5::INSTR")
    
    # Get ID
    if bool(__debug__): 
        print(psu.query('*IDN?'))

    return psu

def close_psu(psu_to_close):
    psu_to_close.close()
    
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

# START HERE
if bool(__debug__): print(timenow() + "#: " + '{:}'.format(count) + " ")

while True:
    time.sleep(delay_time)
    
    psu = open_psu()

    f = getCurr(psu)
    measure_count += 1
    
    if bool(__debug__): 
        print(timenow() + 
              ' {:5}'.format(measure_count) + 
              " #: " + '{:5}'.format(count) + 
              " current: " + '{0:>7.2f}'.format(f) + " mA")

    if(f > curr_limit):
        count+=1
        print(timenow() + 
              ' {:5}'.format(measure_count) + 
              " #: " + '{:5}'.format(count) + 
              " current: " + '{0:>7.2f}'.format(f) + " mA")

        while f > curr_limit:
            time.sleep(delay_time)
            f = getCurr(psu)
            
    close_psu(psu)

sys.exit(0)