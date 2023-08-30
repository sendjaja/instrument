#!/usr/bin/env python
import pyvisa
import time
import sys
import random
import signal

def signal_handler(sig, frame):
    print("Ctrl+C is pressed, turning off PSU")
    psu.write("OUTPUT OFF")
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

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

# BEEP
# while 1:
    # psu.write("SYSTEM:BEEPER:IMMEDIATE")

# QUERY to make sure instrument exist
print(psu.query('*IDN?'))

# state = psu.query("OUTPUT:STATE?")

# print(state)
# # time.sleep(1)
# psu.write("INSTRUMENT:SELECT OUTPUT1")
# psu.write("Apply 3.85,1.5")

# if int(state) == 0:
#     print("ON")
#     psu.write("OUTPUT ON")
#     while True:
#         current = psu.query("measure:current?")
#         print(float(current))
#         if float(current) <= 0.008:
#             break
#         time.sleep(1)
#     sys.exit(0)
# else:
#     print("OFF")
#     psu.write("OUTPUT OFF")
#     sys.exit(-1)

state = psu.query("OUTPUT:STATE?")

magnet = 0
random_enable = 1
run_number = -1

if magnet == 1 and random_enable == 0:
    psu.write(":OUTP OFF")
    psu.write(":VOLT 12")
    psu.write(":CURR 1")

    # Work too, but will not show on PSU front panel
    # when output is still on. Might mislead user.
    # Thus use time.sleep instead
    #psu.write(":OUTP:DEL:FALL 8")

    psu.write(":OUTP:DEL:FALL 0")
    psu.write(":OUTP ON")
    print("Magnet ON")

    i = 10

    while True:
        print(i, end="\r")

        if i == 0:
            break
        i = i - 1
        time.sleep(1)
        print("  ", end="\r")

    psu.write(":OUTP OFF")

    print("Magnet OFF")
elif magnet == 0 and random_enable == 1:
    print("Random")
    iteration = 0

    # print("rng = " + str(random.randrange(0, 5, 0.2)))
    #values = range(6)
    #for x in values:
    psu.write(":OUTP OFF")
    psu.write(":VOLT 4.0")
    psu.write(":CURR 0.1")
    while run_number == -1:
        iteration += 1
        psu.write("OUTPUT ON")
        a = random.randint(200, 500)
        f = a/1000
        time.sleep(f)
        psu.write("OUTPUT OFF")
        b = random.randint(1, 6)

        time.sleep(b)

        print(str(iteration).zfill(4) + " : button press of " + "{:1.3f}".format(f) + " milliseconds and delay of " +str(b) + " seconds")
elif magnet == 0 and random_enable == 0:
    psu.write(":OUTP OFF")
    psu.write(":VOLT 3.8")
    psu.write(":CURR 1")
    if int(state) == 0:
        print("ON")
        psu.write("OUTPUT ON")
    else:
        print("OFF")
        psu.write("OUTPUT OFF")
else:
    print("Cannot have both magnet and random = 1")
    sys.exit(0)