# -*- coding: utf-8 -*-
"""
Created on Mon Apr 13 19:32:34 2020

@author: atlan
"""
import time

start_time = time.time()
print('a')
print
time.sleep(1)
end_time = start_time + 0.1*60
while time.time() < end_time:
    print(str((end_time-time.time())/60) + ' minutes left')
    time.sleep(1)
print('end')