
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