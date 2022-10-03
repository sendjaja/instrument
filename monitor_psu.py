#!/usr/bin/env python
import pyvisa
import time
import sys
import datetime

rm = pyvisa.ResourceManager('@py')
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
# print(psu.query('*IDN?'))

state = psu.query("OUTPUT:STATE?")

print(state)
# time.sleep(1)
psu.write("INSTRUMENT:SELECT OUTPUT1")
# psu.write("Apply 3.85,1.5")

error_count = 0

datetime.datetime.now().strftime('%H:%M:%S')

if int(state) == 1:
#    print("ON")
#    psu.write("OUTPUT ON")
    while True:
        current = psu.query("measure:current?")
        print(datetime.datetime.now().strftime('%H:%M:%S'), end = ' ')
        print("{:.3f}".format(float(current)), end = ' ')
        print(error_count, end = '\r')
        # print("\r")
        if float(current) > 0.3:
            error_count += 1
            print(datetime.datetime.now().strftime('%H:%M:%S'), end = ' ')
            print("{:.3f}".format(float(current)), end = ' ')
            print(error_count)
        else:
            error_count = 0
        time.sleep(1)
        if error_count > 5:
            print(datetime.datetime.now().strftime('%H:%M:%S'), end = ' ')
            print("{:.3f}".format(float(current)), end = ' ')
            print(error_count)
            break
    print("OVER CURRENT - OFF")
    sys.exit(0)
else:
    print("OFF")
    psu.write("OUTPUT OFF")
    sys.exit(-1)
