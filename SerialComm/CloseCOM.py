# -*- coding: utf-8 -*-
"""
Created on Thu Apr 16 00:25:04 2020

@author: atlan
"""


import serial
s = serial.Serial('COM3',115200)
s.close()