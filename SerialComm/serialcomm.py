# -*- coding: utf-8 -*-
"""
Created on Sun Apr 12 15:38:04 2020

@author: atlan
"""

#!/usr/bin/python
"""\
Simple g-code streaming script
"""
 
import serial
import time
import re

def parse(string):
    if (string.find('XTIME') != -1):
        timestamp = re.findall("\d+\.\d+", string[string.index(';'):])  #string[string.index(';'):] pulls out the part after the ';', i.e. the comment, then re.findall looks for number.number (\d+\.\d+). Returns a list with only one member
        end_time = start_time + float(timestamp[0])*60
        while time.time() < end_time:
            print(str((end_time-time.time())/60) + ' minutes left')
            time.sleep(10)
        return(' ')
    if (string.find(';')==-1):
        return string
    else:
        print(string[string.index(';'):])
        return string[:string.index(';')]
 
# Open serial port
#s = serial.Serial('/dev/ttyACM0',115200)
s = serial.Serial('COM3',115200)
print ('Opening Serial Port')
 
# Open g-code file
f = open('result.txt','r');
print ('Opening gcode file')

def serialwrite(string):
    s.write(str.encode(string))
 
# Wake up 
serialwrite('\r\n\r\n') # Hit enter a few times to wake the printer
time.sleep(10)   # Wait for Printrbot to initialize
s.flushInput()  # Flush startup text in serial input
while s.inWaiting():
    print (s.readline())
      
           
print ('Sending gcode') 
# Stream g-code
start_time = time.time()
for line in f:
    l = parse(line)
    l = l.strip() # Strip all EOL characters for streaming
    if  (l.isspace()==False and len(l)>0) :
        print ('Sending: ' + l)
        echo = 'null'
        serialwrite(l + '\n') # Send g-code block
        while (echo.find('ok') == -1) :
            echo_bytes = s.readline() # Wait for response with carriage return
            echo = echo_bytes.decode(encoding="utf-8")
            print (echo.strip())
 
# Wait here until printing is finished to close serial port and file.
print ('  Press <Enter> to exit.')
 
# Close file and serial port
f.close()
s.close()