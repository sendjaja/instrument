#!/usr/bin/env python
import pyvisa as visa
import time
import sys
import signal
from datetime import datetime
import random

# Run python -O <this file>
# to set __debug__ to False

### DEBUG
# From visa import log_to_screen
# From pyvisa.ctwrapper.highlevel import NIVisaLibrary
#log_to_screen()
#NIVisaLibrary.get_library_paths()
#pyvisa.log_to_screen()

# DEFAULT setting for this file
# Default delay is 0, but will change if passed in argument is not 0.
magnet_delay = 0

# To keep track of how many toggles this script will do
run_number = 72000

# Voltage to set
output_volt = 4.0

# Current to set
output_current = 0.1

# Mode 1 delay
mode1_delay  = 1000

# Mode 2 delay - to simulate magnet for bonding
mode2_delay  = 6000

# Mode 3 - press button for x seconds then wait for y seconds
# Range for button press
mode3_button_press = 500
# Range for waiting delay
mode3_delay = 7000

# Mode 4 - press button for random x seconds then wait for random y seconds
# Range for button press
mode4_button_press_range_start = 200
mode4_button_press_range_end   = 500
# Range for waiting delay
mode4_delay_range_start = 1000
mode4_delay_range_end   = 7000

# Functions
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
    #visa.log_to_screen()
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
    psu = rm.open_resource('USB0::0x05E6::0x2280::4427814::INSTR')

    # GPIB
    #psu = rm.open_resource("GPIB0::5::INSTR")

    # Get ID
    if bool(__debug__):     
        print(psu.query('*IDN?'))

    return psu

def psu_set_volt_and_curr():
    # CAREFUL, MAGNET IS 12V OUTPUT for IPG
    volt = ":VOLT " + "{:1.1f}".format(output_volt)
    curr = ":CURR " + "{:1.1f}".format(output_current)
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

def psu_press_then_wait(delay):
    psu.write(":OUTP OFF")

    ### This is for Charger
    i = delay/1000

    psu.write(":OUTP ON")

    while True:
        print(i, end="\r")

        if i <= 0:
            break
        i = i - 1
        time.sleep(1)
        print(str(i), end="\r")

    psu.write(":OUTP OFF")

def continuous(randomize, press_start, press_end, delay_start, delay_end):
    # Just to print out what mode it is, random or fixed
    if randomize == 0:
        print("Fixed toggle on for " +
              "{:1.3f}".format(press_start/1000) + " seconds and wait " + 
              "{:1.3f}".format(delay_start/1000) + " seconds")
    else:
        print("Random toggle on for between " +
              "{:1.3f}".format(press_start/1000) + " seconds to " + 
              "{:1.3f}".format(press_end/1000)   + " and wait for between" +
              "{:1.3f}".format(delay_start/1000) + " seconds to " + 
              "{:1.3f}".format(delay_end/1000)
              )
        
    # To keep track how many toggles already
    iteration = 0

    psu.write(":OUTP OFF")
    while iteration < ( run_number * 2 ) :
        iteration += 1
        psu.write(":OUTP ON")
        
        if randomize != 0:
            a = random.randint(press_start, press_end)
        else:
            # If not random, takes only the start *start value. Ignore the end
            a = press_start
        f = a/1000
        time.sleep(f)
        psu.write(":OUTP OFF")
        
        if randomize != 0:
            b = random.randint(delay_start, delay_end)
        else:
            # If not random, takes only the start *start value. Ignore the end
            b = delay_start
        g = b/1000
        # Print first, otherwise miss by 1
        now = datetime.now()
        print(timenow() + " " + str(iteration).zfill(4) + 
              " : button press of " + "{:1.3f}".format(f) + 
              " s and delay of " + "{:1.3f}".format(g) + " s")
        time.sleep(g)

def print_help():
    print("usage: psu.py [mode] ")
    print("mode: 0 - toggle")
    print("mode: 1 - button for " + "{:1.3f}".format(mode1_delay/1000) + \
          " seconds")
    print("mode: 2 - button for " + "{:1.3f}".format(mode2_delay/1000) + \
          " seconds")
    print("mode: 3 - button press for " +
          "{:1.3f}".format(mode3_button_press/1000) + " seconds"
        "\n          then wait for " +
         "{:1.3f}".format(mode3_delay/1000) + " seconds")
    print("mode: 4 - random button press for " +
          "{:1.3f}".format(mode4_button_press_range_start/1000) + " - " +
          "{:1.3f}".format(mode4_button_press_range_end/1000) + " seconds" +
        "\n          then wait for random " +
          "{:1.3f}".format(mode4_delay_range_start/1000) + " - " +
          "{:1.3f}".format(mode4_delay_range_end/1000) + " seconds" +
          "seconds ")
    sys.exit(0)

# START HERE
n = len(sys.argv)
if bool(__debug__):
    print("# of arg = " + str(n))
if n > 2:
    print_help()
    sys.exit(0)
elif n == 2:
    if bool(__debug__):
        print("arg[0]: " + sys.argv[0])
        print("arg[1]: " + str(int(sys.argv[1])))
    
    psu = open_psu()
    psu_set_volt_and_curr()

    if int(sys.argv[1]) == 0:
        psu_toggle()
    elif int(sys.argv[1]) == 1:
        psu_press_then_wait(mode1_delay)
    elif int(sys.argv[1]) == 2:
        psu_press_then_wait(mode2_delay)
    elif int(sys.argv[1]) == 3:
        continuous(0, 
                   mode3_button_press, 
                   0, 
                   mode3_delay, 
                   0)
    elif int(sys.argv[1]) == 4:
        continuous(1, 
                   mode4_button_press_range_start,
                   mode4_button_press_range_end,
                   mode4_delay_range_start,
                   mode4_delay_range_end)
elif n == 1:
    # Default, print help
    print_help()
    sys.exit(0)

sys.exit(0)