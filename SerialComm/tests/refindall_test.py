# -*- coding: utf-8 -*-
"""
Created on Wed Apr 15 23:59:28 2020

@author: atlan
"""
import re 

string = 'G4 S2700.0;wait until 60.0 minutes XTIME'
print(string[string.index(';'):])
timestamp = re.findall("\d+\.\d+", string[string.index(';'):]) 
print (timestamp[0])
