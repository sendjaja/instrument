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