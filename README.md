# PyVISA USB

Run pyvisa-info to check version of python used and whether pyVISA had been installed.
```
$ pyvisa-info
Machine Details:
   Platform ID:    CYGWIN_NT-10.0-19044-3.3.4-341.x86_64-x86_64-64bit-WindowsPE
   Processor:

Python:
   Implementation: CPython
   Executable:     /usr/bin/python3.8.exe
   Version:        3.8.12
   Compiler:       GCC 11.2.0
   Bits:           64bit
   Build:          Nov 23 2021 20:18:25 (#default)
   Unicode:        UCS4

PyVISA Version: 1.12.0

Backends:
   ivi:
      Version: 1.12.0 (bundled with PyVISA)
      Binary library: Not found
```

If using Cyqwin, need to install Libusb1 from Cygwin setup. Currently libusb1.0 is version 1.0.21-1. Its status is Unmaintained though.

Run Python3 -m visa info - make sure there is libusb1 on backend
```
$ /usr/bin/python3.9 -m visa info
/usr/local/lib/python3.9/site-packages/visa.py:13: FutureWarning: The visa module provided by PyVISA is being deprecated. You can replace `import visa` by `import pyvisa as visa` to achieve the same effect.

The reason for the deprecation is the possible conflict with the visa package provided by the https://github.com/visa-sdk/visa-python which can result in hard to debug situations.
  warnings.warn(
Machine Details:
   Platform ID:    CYGWIN_NT-10.0-19044-3.3.4-341.x86_64-x86_64-64bit-WindowsPE
   Processor:

Python:
   Implementation: CPython
   Executable:     /usr/bin/python3.9.exe
   Version:        3.9.10
   Compiler:       GCC 11.2.0
   Bits:           64bit
   Build:          Jan 20 2022 21:37:52 (#main)
   Unicode:        UCS4

PyVISA Version: 1.11.3

Backends:
   ivi:
      Version: 1.11.3 (bundled with PyVISA)
      Binary library: Not found
   py:
      Version: 0.5.2
      ASRL INSTR: Available via PySerial (3.5)
      USB INSTR: Available via PyUSB (1.2.1). Backend: libusb1
      USB RAW: Available via PyUSB (1.2.1). Backend: libusb1
      TCPIP INSTR: Available
      TCPIP SOCKET: Available
      GPIB INSTR:
         Please install linux-gpib (Linux) or gpib-ctypes (Windows, Linux) to use this resource type. Note that installing gpib-ctypes will give you access to a broader range of funcionality.
         No module named 'gpib'
```

# Power Supply E3648A
1. pip install pyvisa pyvisa-py pyserial
2. pip list
```
$ pip list
Package           Version
----------------- -------
pip               22.0.4
pyserial          3.5
PyVISA            1.11.3
PyVISA-py         0.5.2
setuptools        59.5.0
typing_extensions 4.1.1
```
3. if vscode complain it cannot find package, go to extension pylance settings, add C:\cygwin64\usr\local\lib\python3.9\site-packages to Extra Paths
4. Make sure in E3648A that RS232 is selected, Press IO Config button, check that "RS-232" is selected, then "9600 baud", then "none 8 bits"
5. In PSU.py file, replace line 10
```
psu = rm.open_resource("ASRL/dev/ttyS13::INSTR")
```
with the corresponding COM port in your PC. In this case, the USB to Serial port is COM14 on windows PC, which translates to /dev/ttyS13 in Cygwin (start from ttyS0)

# Arduino
arduino.sh is using arduino-cli to run the sketch. The sketch is to ground 2 analog input line (14 and 15) for 8 seconds. Somehow, the filename-instrument.ino has to match the directory name, which in this case is instrument. With this setup, the arduino-cli compile and upload does not even need the .ino file name

# Both
To tie them together, run the following
```
./psu.py && ./arduino.sh
```
which basically will toggle the Power supply E3648A, and then run the arduino

