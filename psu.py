#!/usr/bin/env python
import pyvisa as visa
import time
import sys
import signal
from datetime import datetime
import random

### DEBUG
#from visa import log_to_screen
#from pyvisa.ctwrapper.highlevel import NIVisaLibrary
#log_to_screen()
#NIVisaLibrary.get_library_paths()
#pyvisa.log_to_screen()

#default setting for this file
magnet_delay = 0
run_number = 72000

def timenow():
    now = datetime.now()
    dt_string = now.strftime("%m/%d/%Y %H:%M:%S")
    return dt_string

def signal_handler(sig, frame):
    print("Ctrl+C is pressed, turning off PSU")
    psu.write(":OUTP OFF")
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

def openVisaResourceManager():
    # visa.log_to_screen()
    # rm = pyvisa.ResourceManager('@py')
    # rm = visa.ResourceManager
    #   ('C:\Program Files\IVI Foundation\VISA\Win64\Lib_x64\msc\visa64.lib')
    rm = visa.ResourceManager('C:\\windows\\system32\\visa64.dll')
    print(rm)
    res = rm.list_resources()
    print("Found following resources: ")
    print(res)

    return rm
    
def open_psu():
    rm = openVisaResourceManager()

    # print("Opening " + res[-1])
    #SERIAL
    #psu = rm.open_resource("ASRL/dev/ttyS1::INSTR")
    #psu.baud_rate = 9600
    #psu.data_bits = 8
    #psu.write_termination="\n"
    #psu.read_termination="\n"
    ## psu.send_end=1
    #psu.timeout = 2500 # timeout 2.5s

    #USB
    # This might change, especially the "4441344"
    psu = rm.open_resource('USB0::0x05E6::0x2280::4441344::INSTR')

    print(psu.query('*IDN?'))

    return psu

def psu_set_volt_and_curr():
    # CAREFUL, MAGNET IS 12V OUTPUT for IPG
    volt = ":VOLT 4.0"
    curr = ":CURR 0.1"
    psu.write(volt)
    psu.write(curr)

def psu_toggle():
    state = psu.query("OUTPUT:STATE?")
    if int(state) == 0:
        print("ON")
        psu.write(":OUTP ON")
    else:
        print("OFF")
        psu.write(":OUTP OFF")

def psu_press_then_wait():
    psu.write(":OUTP OFF")

    ### This is for Charger
    i = magnet_delay

    psu.write(":OUTP ON")

    while True:
        print(i, end="\r")

        if i == 0:
            break
        i = i - 1
        time.sleep(1)
        print(str(i), end="\r")

    psu.write(":OUTP OFF")

def continuous(randomize):
    if randomize == 0:
        print("Toggle on for 0.5 seconds, then wait " + 
              str(magnet_delay) + " seconds")
    else:
        print("Random")
    iteration = 0
    psu.write(":OUTP OFF")
    while iteration < ( run_number * 2 ) :
        iteration += 1
        psu.write(":OUTP ON")
        a = 500
        if randomize != 0:
            a = random.randint(200, 500)
            f = a/1000
        time.sleep(f)
        psu.write(":OUTP OFF")
        b = magnet_delay
        if randomize != 0:
            b = random.randint(1000, 6000)
            g = b/1000
        # Print first, otherwise miss by 1
        now = datetime.now()
        print(timenow() + " " + str(iteration).zfill(4) + 
              " : button press of " + "{:1.3f}".format(f) + 
              " ms and delay of " + "{:1.3f}".format(g) + " ms")
        time.sleep(g)

def print_help():
    print("usage: psu.py [mode] ")
    print("mode: 0 - toggle")
    print("mode: 1 - button for 1 seconds")
    print("mode: 2 - button for 6 seconds ")
    print("mode: 3 - press button for 0.5 seconds then wait for \
          [magnet_delay] seconds")
    print("mode: 4 - random button press of 200-500 milli seconds \
          then wait for random 1-6 seconds, ")
    sys.exit(0)

# START HERE
n = len(sys.argv)
#print("n = " + str(n))
if n > 2:
    print_help()
    sys.exit(0)
elif n == 2:
    psu = open_psu()
    psu_set_volt_and_curr()
    #print("arg[0]: " + sys.argv[0])
    #print("arg[1]: " + str(int(sys.argv[1])))
    if int(sys.argv[1]) == 0:
        psu_toggle()
    elif int(sys.argv[1]) == 1:
        magnet_delay = 1
        psu_press_then_wait()
    elif int(sys.argv[1]) == 2:
        magnet_delay = 6
        psu_press_then_wait()
    elif int(sys.argv[1]) == 3:
        magnet_delay = 7
        continuous(0)
    elif int(sys.argv[1]) == 4:
        continuous(1)
elif n == 1:
    #default, print help
    print_help()
    sys.exit(0)

sys.exit(0)