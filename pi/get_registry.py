#!/usr/bin/env python3
import serial
import time

ser = serial.Serial('/dev/ttyUSB0', 9600, timeout=1)
ser.reset_input_buffer()

time.sleep(2)

print('data gonderiliyor...')
ser.write('p'.encode('utf-8'))
print('data gonderildi.')

received_data = ser.read()              #read serial port
time.sleep(1)
data_left = ser.inWaiting()             #check for remaining byte
received_data += ser.read(data_left)
print (received_data)  

