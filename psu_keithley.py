#!/usr/bin/env python
import pyvisa
import time

# pyvisa.log_to_screen()
rm = pyvisa.ResourceManager('C:\\windows\\system32\\visa32.dll')
res = rm.list_resources('USB?*')
print(res)

# Find the serial number
str = str(res)
items = str.split('::')
# print(items[0])
# print(items[1])
# print(items[2])
# print(items[3])
# print(items[4])

# Using this, dev.iSerialNumber only show 1 digit
# dev = usb.core.find(idVendor=0x05e6, idProduct=0x2280)

# if dev is None:
#     raise ValueError('Device not found')
# else:
#     print(hex(dev.idVendor), hex(dev.idProduct), hex(dev.iSerialNumber), dev.bcdDevice, dev.iManufacturer, dev.bNumConfigurations, dev.bLength)

# psu = rm.open_resource('USB0::0x05E6::0x2280::4484051::INSTR')
psu = rm.open_resource('USB0::0x05E6::0x2280::' + items[3] +'::INSTR')

# print(psu.query("OUTPUT:STATE?"), end="\r")
psu.write(":OUTP OFF")
psu.write(":VOLT 12")
psu.write(":CURR 1")
# psu.write(":OUTP:DEL:STAT ON")

# Work too, but will not show on PSU front panel
# when output is still on. Might mislead user.
# Thus use time.sleep instead
#psu.write(":OUTP:DEL:FALL 8")

psu.write(":OUTP:DEL:FALL 0")
psu.write(":OUTP ON")
print("Magnet ON")
# print(psu.query("OUTPUT:STATE?"), end="\r")

i = 10

while True:
    print(i, end="\r")

    if i == 0:
        break
    i = i - 1
    time.sleep(1)
    print("  ", end="\r")

# time.sleep(10)

psu.write(":OUTP OFF")

print("Magnet OFF")
# print(psu.query("OUTPUT:STATE?"))
