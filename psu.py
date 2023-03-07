#!/usr/bin/env python
import pyvisa
import time
import sys

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

magnet = 1

if magnet == 1:
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
else:
    psu.write(":OUTP OFF")
    psu.write(":VOLT 3.8")
    psu.write(":CURR 1")
    if int(state) == 0:
        print("ON")
        psu.write("OUTPUT ON")
    else:
        print("OFF")
        psu.write("OUTPUT OFF")

    sys.exit(0)