#!/usr/bin/env python
import pyvisa
import time
import sys
import random
import signal

#default
magnet_delay = 0
run_number = -1

def signal_handler(sig, frame):
    print("Ctrl+C is pressed, turning off PSU")
    psu.write(":OUTP OFF")
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

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
    print("Magnet ON")

    while run_number == -1:
        print(i, end="\r")

        if i == 0:
            break
        i = i - 1
        time.sleep(1)
        print("  ", end="\r")

    psu.write(":OUTP OFF")

    print("Magnet OFF")

def bla():
    print("toggle on for 0.5 seconds, then wait 6 seconds")
    iteration = 0
    psu.write(":OUTP OFF")
    while run_number == -1:
        iteration += 1
        psu.write(":OUTP ON")
        #a = random.randint(200, 500)
        a = 500
        f = a/1000
        time.sleep(f)
        psu.write(":OUTP OFF")
        #b = random.randint(1, 6)
        b = 6

        time.sleep(b)

        print(str(iteration).zfill(4) + " : button press of " + "{:1.3f}".format(f) + " milliseconds and delay of " +str(b) + " seconds")

def random_bla():
    print("Random")
    iteration = 0
    psu.write(":OUTP OFF")
    while run_number == -1:
        iteration += 1
        psu.write(":OUTP ON")
        a = random.randint(200, 500)
        f = a/1000
        time.sleep(f)
        psu.write(":OUTP OFF")
        b = random.randint(1, 6)

        time.sleep(b)

        print(str(iteration).zfill(4) + " : button press of " + "{:1.3f}".format(f) + " milliseconds and delay of " +str(b) + " seconds")

def open_psu():
    # visa.log_to_screen()
    rm = pyvisa.ResourceManager('@py')
    # rm = visa.ResourceManager('C:\Program Files\IVI Foundation\IVI\Lib_x64\msc')
    print(rm)
    res = rm.list_resources()
    print("Found following resources: ")
    print(res)

    # print("Opening " + res[-1])
    psu = rm.open_resource("ASRL/dev/ttyS13::INSTR")

    psu.baud_rate = 9600
    psu.data_bits = 8
    psu.write_termination="\n"
    psu.read_termination="\n"
    # psu.send_end=1
    psu.timeout = 2500 # timeout 2.5s

    print(psu.query('*IDN?'))

    return psu

def print_help():
    print("usage: psu.py [mode] ")
    print("mode: 0 - toggle")
    print("mode: 1 - button for 1 seconds")
    print("mode: 2 - button for 6 seconds ")
    print("mode: 3 - press button for 0.5 seconds then wait for 6 seconds")
    print("mode: 4 - random button press of 200-500 milli seconds then wait for 1-6 seconds, ")
    sys.exit(0)

n = len(sys.argv)
print("n = " + str(n))
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
        bla()
    elif int(sys.argv[1]) == 4:
        random_bla()
elif n == 1:
    #default, print help
    print_help()
    sys.exit(0)

sys.exit(0)