#!/usr/bin/env python
import pyvisa
import time
import sys

# pyvisa.log_to_screen()
rm = pyvisa.ResourceManager('C:\\windows\\system32\\visa32.dll')
res = rm.list_resources('USB?*')
print(res)

# Find the serial number
str = str(res)
items = str.split('::')

psu = rm.open_resource('USB0::0x05E6::0x2280::' + items[3] +'::INSTR')
state = psu.query("OUTPUT:STATE?")
# psu.write(":OUTP OFF")
psu.write(":CURR 1")

volt  = 3.5
decrement = 0.0033 # per time unit
time_unit = 1 #seconds
stop_volt = 4

init_volt = "{:1.4f}".format(float(volt))
psu.write(":VOLT " + init_volt)
psu.write(":OUTP ON")

print("start")
while True:
    volt = volt + decrement

    print("{:1.4f}".format(float(volt)))
    temp = "{:1.4f}".format(float(volt))
    psu.write(":VOLT "+ temp)
    if(volt > stop_volt):
        break
    time.sleep(time_unit)

print("end")
sys.exit(0)
