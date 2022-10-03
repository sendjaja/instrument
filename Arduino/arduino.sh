#!/bin/bash

# /cygdrive/c/SWTools/arduino-cli_0.21.1_Windows_64bit/arduino-cli.exe \
# compile \
# --fqbn arduino:avr:mega \
# ./sketch_jan17a.ino

# For time command to return only real time, no user, no sys
TIMEFORMAT=%R

time \
/cygdrive/c/SWTools/arduino-cli_0.21.1_Windows_64bit/arduino-cli.exe \
upload \
-p COM7 \
--fqbn arduino:avr:mega \
C:/projects/instrument/Arduino/sketch_jan17a/sketch_jan17a.ino

# It takes roughly ~1 seconds to run above command.
# Adjust as needed the sleep # below
sleep 1
secs=$((8))
while [ $secs -gt 0 ]; do
   echo -ne "$secs\033[0K\r"
   sleep 1
   : $((secs--))
done
echo -ne "done"

unset TIMEFORMAT
